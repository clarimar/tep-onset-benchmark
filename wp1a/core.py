from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    matthews_corrcoef,
)
from sklearn.tree import DecisionTreeClassifier

META_CANDIDATES = {
    "label": ("faultNumber", "fault_number", "fault", "label", "target", "class"),
    "run": ("simulationRun", "simulation_run", "run", "run_id"),
    "time": ("sample", "time", "timestamp", "time_step"),
}

GRIDS: dict[str, list[dict[str, Any]]] = {
    "logistic_regression": [
        {"C": 0.1},
        {"C": 1.0},
        {"C": 10.0},
    ],
    "decision_tree": [
        {"max_depth": 12, "min_samples_leaf": 5},
        {"max_depth": 24, "min_samples_leaf": 2},
        {"max_depth": None, "min_samples_leaf": 1},
    ],
    "random_forest": [
        {
            "n_estimators": 250,
            "max_depth": None,
            "max_features": "sqrt",
            "min_samples_leaf": 1,
        },
        {
            "n_estimators": 400,
            "max_depth": 24,
            "max_features": "sqrt",
            "min_samples_leaf": 2,
        },
        {
            "n_estimators": 400,
            "max_depth": None,
            "max_features": 0.5,
            "min_samples_leaf": 1,
        },
    ],
    "hist_gradient_boosting": [
        {"learning_rate": 0.1, "max_iter": 200, "max_leaf_nodes": 31},
        {"learning_rate": 0.05, "max_iter": 350, "max_leaf_nodes": 31},
        {"learning_rate": 0.1, "max_iter": 250, "max_leaf_nodes": 63},
    ],
    "linear_svm": [
        {"alpha": 1e-3},
        {"alpha": 1e-4},
        {"alpha": 1e-5},
    ],
    "xgboost": [
        {
            "n_estimators": 250,
            "max_depth": 6,
            "learning_rate": 0.1,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
        },
        {
            "n_estimators": 400,
            "max_depth": 8,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
        },
        {
            "n_estimators": 300,
            "max_depth": 10,
            "learning_rate": 0.1,
            "subsample": 1.0,
            "colsample_bytree": 0.8,
        },
    ],
}


@dataclass(frozen=True)
class Schema:
    label: str
    run: str
    time: str | None
    features: tuple[str, ...]


def identify_schema(path: Path) -> Schema:
    schema = pq.ParquetFile(path).schema_arrow
    names = schema.names
    lower = {x.lower(): x for x in names}
    found: dict[str, str | None] = {}
    for role, candidates in META_CANDIDATES.items():
        found[role] = next(
            (lower[x.lower()] for x in candidates if x.lower() in lower), None
        )
    if not found["label"] or not found["run"]:
        raise ValueError("As colunas de classe e execucao sao obrigatorias.")
    excluded = {x for x in found.values() if x}
    numeric = {f.name for f in schema if pa_numeric(f.type)}
    features = tuple(x for x in names if x in numeric and x not in excluded)
    if len(features) != 52:
        raise ValueError(
            f"Esperadas 52 variaveis numericas; encontradas {len(features)}."
        )
    return Schema(str(found["label"]), str(found["run"]), found["time"], features)


def pa_numeric(dtype: Any) -> bool:
    import pyarrow as pa

    return (
        pa.types.is_integer(dtype)
        or pa.types.is_floating(dtype)
        or pa.types.is_boolean(dtype)
    )


def select_complete_runs(
    frame: pd.DataFrame, schema: Schema, runs_per_class: int, seed: int
) -> pd.DataFrame:
    """Choose whole runs, preserving time dependence and preventing pseudo-replication."""
    if runs_per_class <= 0:
        return frame
    keys = frame[[schema.label, schema.run]].drop_duplicates()
    chosen = []
    for _, group in keys.groupby(schema.label, sort=True):
        chosen.append(
            group.sample(n=min(runs_per_class, len(group)), random_state=seed)
        )
    selected = pd.concat(chosen, ignore_index=True).assign(_keep=1)
    return frame.merge(selected, on=[schema.label, schema.run], how="inner").drop(
        columns="_keep"
    )


def read_split(
    path: Path, schema: Schema, runs_per_class: int, seed: int
) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    columns = [*schema.features, schema.label, schema.run] + (
        [schema.time] if schema.time else []
    )
    frame = pd.read_parquet(path, columns=columns, engine="pyarrow")
    frame = select_complete_runs(frame, schema, runs_per_class, seed)
    sort_cols = [schema.label, schema.run] + ([schema.time] if schema.time else [])
    frame = frame.sort_values(sort_cols, kind="stable").reset_index(drop=True)
    X = frame.loc[:, schema.features].to_numpy(dtype=np.float32, copy=True)
    y = frame[schema.label].to_numpy(copy=True)
    if not np.isfinite(X).all() or pd.isna(y).any():
        raise ValueError(f"NaN ou infinito em {path}.")
    return (
        X,
        y,
        frame[[schema.label, schema.run] + ([schema.time] if schema.time else [])],
    )


def build_model(name: str, params: dict[str, Any], seed: int, jobs: int):
    if name == "logistic_regression":
        return LogisticRegression(
            max_iter=1000, solver="lbfgs", random_state=seed, n_jobs=jobs, **params
        )
    if name == "decision_tree":
        return DecisionTreeClassifier(random_state=seed, **params)
    if name == "random_forest":
        return RandomForestClassifier(random_state=seed, n_jobs=jobs, **params)
    if name == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(random_state=seed, **params)
    if name == "linear_svm":
        return SGDClassifier(
            loss="hinge",
            max_iter=3000,
            tol=1e-3,
            random_state=seed,
            n_jobs=jobs,
            **params,
        )
    if name == "xgboost":
        try:
            from xgboost import XGBClassifier
        except ImportError as exc:
            raise RuntimeError("Instale o extra wp1a para executar XGBoost.") from exc
        return XGBClassifier(
            objective="multi:softprob",
            eval_metric="mlogloss",
            tree_method="hist",
            random_state=seed,
            n_jobs=jobs,
            **params,
        )
    raise ValueError(f"Modelo desconhecido: {name}")


def evaluate(
    model, X: np.ndarray, y: np.ndarray
) -> tuple[dict[str, float], np.ndarray]:
    start = time.perf_counter()
    pred = np.asarray(model.predict(X))
    elapsed = time.perf_counter() - start
    return {
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "f1_macro": float(f1_score(y, pred, average="macro", zero_division=0)),
        "f1_weighted": float(f1_score(y, pred, average="weighted", zero_division=0)),
        "mcc": float(matthews_corrcoef(y, pred)),
        "inference_seconds": elapsed,
        "inference_ms_per_sample": 1000 * elapsed / max(len(y), 1),
    }, pred


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    os.replace(temp, path)


def serialized_size(model, destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, destination, compress=3)
    return destination.stat().st_size
