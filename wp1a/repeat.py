"""WP1A: repeated validation of the six frozen classical models.

This module never accepts or accesses a test dataset. It samples complete TEP
runs from the already frozen train and validation Parquets, fits each selected
model for five seeds, and aggregates validation metrics with 95% t intervals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from scipy.stats import t
from sklearn import __version__ as sklearn_version
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import (accuracy_score, balanced_accuracy_score,
                             confusion_matrix, f1_score,
                             matthews_corrcoef, precision_recall_fscore_support)
from sklearn.tree import DecisionTreeClassifier

FEATURES = [*(f"xmeas_{i}" for i in range(1, 42)),
            *(f"xmv_{i}" for i in range(1, 12))]
ID_COLUMNS = ["faultNumber", "simulationRun", "sample"]
SEEDS = [2026, 2027, 2028, 2029, 2030]
PARAMS = {
    "logistic_regression": {"C": 1.0},
    "decision_tree": {"max_depth": None, "min_samples_leaf": 1},
    "random_forest": {"n_estimators": 400, "max_depth": None,
                      "max_features": 0.5, "min_samples_leaf": 1},
    "hist_gradient_boosting": {"learning_rate": 0.05, "max_iter": 350,
                               "max_leaf_nodes": 31},
    "linear_svm": {"alpha": 1e-5},
    "xgboost": {"n_estimators": 250, "max_depth": 6,
                "learning_rate": 0.1, "subsample": 0.8,
                "colsample_bytree": 0.8},
}
MODELS = list(PARAMS)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def build_model(name: str, seed: int, n_jobs: int):
    p = PARAMS[name]
    if name == "logistic_regression":
        return LogisticRegression(**p, max_iter=1000, random_state=seed)
    if name == "decision_tree":
        return DecisionTreeClassifier(**p, random_state=seed)
    if name == "random_forest":
        return RandomForestClassifier(**p, random_state=seed, n_jobs=n_jobs)
    if name == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(**p, random_state=seed)
    if name == "linear_svm":
        return SGDClassifier(loss="hinge", **p, max_iter=2000, tol=1e-3,
                             random_state=seed, n_jobs=n_jobs)
    if name == "xgboost":
        try:
            from xgboost import XGBClassifier
        except ImportError as exc:
            raise RuntimeError('Execute: uv pip install -e ".[wp1a]"') from exc
        return XGBClassifier(**p, objective="multi:softprob", num_class=21,
                             eval_metric="mlogloss", random_state=seed,
                             n_jobs=n_jobs, tree_method="hist")
    raise ValueError(name)


def read_dataset(path: Path) -> pd.DataFrame:
    frame = pd.read_parquet(path, columns=ID_COLUMNS + FEATURES)
    missing = set(ID_COLUMNS + FEATURES) - set(frame.columns)
    if missing:
        raise ValueError(f"Colunas ausentes em {path}: {sorted(missing)}")
    return frame


def sample_complete_runs(frame: pd.DataFrame, runs_per_class: int,
                         seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    chosen = []
    for label, group in frame.groupby("faultNumber", sort=True):
        runs = np.sort(group["simulationRun"].unique())
        if len(runs) < runs_per_class:
            raise ValueError(f"Classe {label}: somente {len(runs)} runs")
        take = rng.choice(runs, size=runs_per_class, replace=False)
        chosen.append(group[group["simulationRun"].isin(take)])
    result = pd.concat(chosen, ignore_index=True)
    counts = result.groupby(["faultNumber", "simulationRun"]).size()
    if counts.nunique() != 1 or int(counts.iloc[0]) != 500:
        raise ValueError("A amostragem não preservou runs completos de 500 linhas")
    return result


def evaluate(y_true, y_pred) -> tuple[dict, pd.DataFrame, np.ndarray]:
    labels = np.arange(21)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0)
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "f1_macro": f1_score(y_true, y_pred, average="macro"),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted"),
        "mcc": matthews_corrcoef(y_true, y_pred),
    }
    by_class = pd.DataFrame({"class": labels, "precision": precision,
                             "recall": recall, "f1": f1, "support": support})
    return metrics, by_class, confusion_matrix(y_true, y_pred, labels=labels)


def aggregate(rows: pd.DataFrame) -> pd.DataFrame:
    measures = ["accuracy", "balanced_accuracy", "f1_macro", "f1_weighted",
                "mcc", "training_seconds", "inference_seconds",
                "inference_ms_per_sample", "model_size_bytes"]
    output = []
    for model, group in rows.groupby("model", sort=False):
        record = {"model": model, "n": len(group)}
        for col in measures:
            values = group[col].astype(float)
            mean, sd = values.mean(), values.std(ddof=1)
            half = t.ppf(0.975, len(values) - 1) * sd / np.sqrt(len(values))
            record.update({f"{col}_mean": mean, f"{col}_sd": sd,
                           f"{col}_ci95_low": mean - half,
                           f"{col}_ci95_high": mean + half})
        output.append(record)
    return pd.DataFrame(output).sort_values(
        ["f1_macro_mean", "mcc_mean"], ascending=False).reset_index(drop=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True, type=Path)
    parser.add_argument("--validation", required=True, type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path("results/wp1a_definitive/repeated_validation_v1"))
    parser.add_argument("--runs-per-class", type=int, default=40)
    parser.add_argument("--n-jobs", type=int, default=-1)
    args = parser.parse_args()
    if args.train.resolve() == args.validation.resolve():
        raise ValueError("Treino e validação apontam para o mesmo arquivo")
    args.output.mkdir(parents=True, exist_ok=True)
    tasks = args.output / "tasks"
    tasks.mkdir(exist_ok=True)

    manifest_path = args.output / "run_manifest.json"
    if not manifest_path.exists():
        manifest = {"status": "RUNNING", "test_accessed": False,
                    "train": str(args.train.resolve()),
                    "validation": str(args.validation.resolve()),
                    "train_sha256": sha256(args.train),
                    "validation_sha256": sha256(args.validation),
                    "runs_per_class": args.runs_per_class, "seeds": SEEDS,
                    "models": MODELS, "parameters": PARAMS,
                    "python": sys.version, "platform": platform.platform(),
                    "scikit_learn": sklearn_version}
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Lendo treino e validação (o teste não é aceito por este programa)...", flush=True)
    train, validation = read_dataset(args.train), read_dataset(args.validation)
    all_rows = []
    for seed in SEEDS:
        train_seed = sample_complete_runs(train, args.runs_per_class, seed)
        val_seed = sample_complete_runs(validation, args.runs_per_class, seed + 10000)
        if set(map(tuple, train_seed[["faultNumber", "simulationRun"]].drop_duplicates().values)) & set(map(tuple, val_seed[["faultNumber", "simulationRun"]].drop_duplicates().values)):
            raise ValueError("Sobreposição de identificadores entre treino e validação")
        X_train = train_seed[FEATURES].to_numpy(dtype=np.float32, copy=False)
        y_train = train_seed["faultNumber"].to_numpy(dtype=np.int16, copy=False)
        X_val = val_seed[FEATURES].to_numpy(dtype=np.float32, copy=False)
        y_val = val_seed["faultNumber"].to_numpy(dtype=np.int16, copy=False)
        for name in MODELS:
            task = tasks / f"{name}_seed_{seed}.json"
            class_file = tasks / f"{name}_seed_{seed}_by_class.csv"
            cm_file = tasks / f"{name}_seed_{seed}_confusion.csv"
            if task.exists() and class_file.exists() and cm_file.exists():
                print(f"SKIP {name} seed={seed}", flush=True)
                all_rows.append(json.loads(task.read_text(encoding="utf-8")))
                continue
            print(f"RUN  {name} seed={seed}", flush=True)
            model = build_model(name, seed, args.n_jobs)
            start = time.perf_counter(); model.fit(X_train, y_train)
            training_seconds = time.perf_counter() - start
            start = time.perf_counter(); pred = model.predict(X_val)
            inference_seconds = time.perf_counter() - start
            metrics, by_class, cm = evaluate(y_val, pred)
            # Measure the serialized artifact without retaining a potentially
            # gigabyte-sized pickle buffer in memory (notably for Random Forest).
            with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as tmp:
                temporary_model = Path(tmp.name)
            try:
                joblib.dump(model, temporary_model, compress=0)
                model_size = temporary_model.stat().st_size
            finally:
                temporary_model.unlink(missing_ok=True)
            row = {"model": name, "seed": seed, "candidate":
                   {"logistic_regression": 2, "decision_tree": 3,
                    "random_forest": 3, "hist_gradient_boosting": 2,
                    "linear_svm": 3, "xgboost": 1}[name], **metrics,
                   "training_seconds": training_seconds,
                   "inference_seconds": inference_seconds,
                   "inference_ms_per_sample": 1000 * inference_seconds / len(y_val),
                   "model_size_bytes": model_size,
                   "n_train_rows": len(y_train), "n_validation_rows": len(y_val),
                   "test_accessed": False}
            by_class.to_csv(class_file, index=False)
            pd.DataFrame(cm, index=np.arange(21), columns=np.arange(21)).to_csv(cm_file)
            task.write_text(json.dumps(row, indent=2), encoding="utf-8")
            all_rows.append(row)
            print(f"DONE {name} seed={seed} F1={metrics['f1_macro']:.6f}", flush=True)
    rows = pd.DataFrame(all_rows)
    rows.to_csv(args.output / "repetition_metrics.csv", index=False)
    ranking = aggregate(rows)
    ranking.insert(0, "rank", np.arange(1, len(ranking) + 1))
    ranking.to_csv(args.output / "aggregate_metrics_95ci.csv", index=False)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({"status": "PASS", "test_accessed": False,
                     "completed_tasks": len(rows),
                     "best_model_validation": ranking.iloc[0]["model"]})
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(ranking[["rank", "model", "f1_macro_mean", "f1_macro_sd",
                   "mcc_mean"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
