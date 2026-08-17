"""Final, locked evaluation of the frozen WP1A XGBoost on official TEP test.

Version 2 fixes split-specific run lengths: development runs contain 500 rows,
whereas official test runs contain 960 rows. Two prior attempts were aborted
before model fitting/prediction while this structural assumption was corrected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn import __version__ as sklearn_version
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_recall_fscore_support,
)

FEATURES = [
    *(f"xmeas_{i}" for i in range(1, 42)),
    *(f"xmv_{i}" for i in range(1, 12)),
]
ID_COLUMNS = ["faultNumber", "simulationRun", "sample"]
LABELS = np.arange(21)
FINAL_SEED = 2026
RUNS_PER_CLASS_PER_DEVELOPMENT_SPLIT = 40
DEVELOPMENT_RUN_SIZE = 500
TEST_RUN_SIZE = 960
EXPECTED_TRAIN_SHA256 = (
    "db0afe5f31511196788916e063a7bf6ed496f0c8c3b7f02ae05250846ed0203d"
)
EXPECTED_VALIDATION_SHA256 = (
    "9d6237e3f9c3db5b8548f757698478b9ec4caa7f85b1d106d163807488694a82"
)
FROZEN_PARAMS = {
    "n_estimators": 250,
    "max_depth": 6,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    os.replace(temporary, path)


def read_dataset(path: Path) -> pd.DataFrame:
    frame = pd.read_parquet(path, columns=ID_COLUMNS + FEATURES)
    missing = set(ID_COLUMNS + FEATURES) - set(frame.columns)
    if missing:
        raise ValueError(f"Colunas ausentes em {path}: {sorted(missing)}")
    observed_labels = set(frame["faultNumber"].unique())
    if observed_labels != set(LABELS):
        raise ValueError(
            f"Classes inesperadas em {path}: {sorted(observed_labels)}"
        )
    if frame[ID_COLUMNS].isna().any().any():
        raise ValueError(f"Identificadores ausentes em {path}")
    return frame


def assert_complete_runs(
    frame: pd.DataFrame,
    name: str,
    expected_size: int,
) -> None:
    sizes = frame.groupby(
        ["faultNumber", "simulationRun"], sort=False
    ).size()
    if sizes.empty:
        raise ValueError(f"{name}: nenhuma run encontrada")
    invalid = sizes[sizes != expected_size]
    if not invalid.empty:
        raise ValueError(
            f"{name}: tamanho esperado={expected_size}; "
            f"runs incompatíveis; exemplos={invalid.head().to_dict()}"
        )


def sample_complete_runs(
    frame: pd.DataFrame,
    runs_per_class: int,
    seed: int,
    expected_run_size: int,
) -> pd.DataFrame:
    assert_complete_runs(frame, "partição de desenvolvimento", expected_run_size)
    rng = np.random.default_rng(seed)
    selected: list[pd.DataFrame] = []
    for label, group in frame.groupby("faultNumber", sort=True):
        runs = np.sort(group["simulationRun"].unique())
        if len(runs) < runs_per_class:
            raise ValueError(
                f"Classe {label}: somente {len(runs)} runs; "
                f"necessárias={runs_per_class}"
            )
        chosen = rng.choice(runs, size=runs_per_class, replace=False)
        selected.append(group[group["simulationRun"].isin(chosen)])
    result = pd.concat(selected, ignore_index=True)
    assert_complete_runs(
        result, "amostra de desenvolvimento", expected_run_size
    )
    expected_rows = len(LABELS) * runs_per_class * expected_run_size
    if len(result) != expected_rows:
        raise ValueError(
            f"Amostra de desenvolvimento: esperado={expected_rows}, "
            f"observado={len(result)}"
        )
    return result


def evaluate(y_true: np.ndarray, y_pred: np.ndarray):
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS, zero_division=0
    )
    overall = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
    }
    by_class = pd.DataFrame(
        {
            "class": LABELS,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": support,
        }
    )
    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)
    return overall, by_class, matrix


def build_model(n_jobs: int):
    try:
        from xgboost import XGBClassifier
    except ImportError as exc:
        raise RuntimeError('Execute: uv pip install -e ".[wp1a]"') from exc
    return XGBClassifier(
        **FROZEN_PARAMS,
        objective="multi:softprob",
        num_class=21,
        eval_metric="mlogloss",
        random_state=FINAL_SEED,
        n_jobs=n_jobs,
        tree_method="hist",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Avaliação oficial retomada do XGBoost congelado no teste TEP."
    )
    parser.add_argument("--train", required=True, type=Path)
    parser.add_argument("--validation", required=True, type=Path)
    parser.add_argument("--test", required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/wp1a_definitive/final_test_v2"),
    )
    parser.add_argument("--n-jobs", type=int, default=-1)
    parser.add_argument(
        "--confirm-final-test",
        required=True,
        choices=["YES"],
        help="Confirma a avaliação final congelada",
    )
    parser.add_argument(
        "--confirm-resume-after-structural-abort",
        required=True,
        choices=["YES"],
        help="Confirma retomada após duas falhas estruturais sem predições",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [args.train.resolve(), args.validation.resolve(), args.test.resolve()]
    if len(set(paths)) != 3:
        raise ValueError("Treino, validação e teste devem ser arquivos distintos")
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)

    try:
        args.output.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise FileExistsError(
            "A saída v2 já existe; os dados de teste não serão acessados "
            f"novamente: {args.output}"
        ) from exc

    manifest_path = args.output / "final_test_manifest.json"
    manifest = {
        "status": "TEST_EVALUATION_RESUMED",
        "test_accessed": True,
        "started_at_utc": utc_now(),
        "protocol_version": "wp1a_final_test_v2",
        "resume_reason": (
            "Two prior attempts stopped during structural validation before "
            "model fitting, prediction, metric calculation, or result inspection."
        ),
        "prior_structural_aborts": 2,
        "train": str(paths[0]),
        "validation": str(paths[1]),
        "test": str(paths[2]),
        "model": "xgboost",
        "candidate": 1,
        "parameters": FROZEN_PARAMS,
        "final_seed": FINAL_SEED,
        "runs_per_class_per_development_split": (
            RUNS_PER_CLASS_PER_DEVELOPMENT_SPLIT
        ),
        "development_run_size": DEVELOPMENT_RUN_SIZE,
        "test_run_size": TEST_RUN_SIZE,
        "test_sampling": "none_full_official_test",
        "python": sys.version,
        "platform": platform.platform(),
        "scikit_learn": sklearn_version,
    }
    write_json(manifest_path, manifest)

    try:
        print("RETOMADA FINAL REGISTRADA. Calculando hashes...", flush=True)
        hashes = {
            "train_sha256": sha256(paths[0]),
            "validation_sha256": sha256(paths[1]),
            "test_sha256": sha256(paths[2]),
        }
        manifest.update(hashes)
        write_json(manifest_path, manifest)
        if hashes["train_sha256"] != EXPECTED_TRAIN_SHA256:
            raise ValueError("Hash do treino difere do conjunto auditado")
        if hashes["validation_sha256"] != EXPECTED_VALIDATION_SHA256:
            raise ValueError("Hash da validação difere do conjunto auditado")

        print("Lendo treino, validação e teste oficial...", flush=True)
        train = read_dataset(paths[0])
        validation = read_dataset(paths[1])
        test = read_dataset(paths[2])
        assert_complete_runs(train, "treino", DEVELOPMENT_RUN_SIZE)
        assert_complete_runs(validation, "validação", DEVELOPMENT_RUN_SIZE)
        assert_complete_runs(test, "teste oficial", TEST_RUN_SIZE)

        train_selected = sample_complete_runs(
            train,
            RUNS_PER_CLASS_PER_DEVELOPMENT_SPLIT,
            FINAL_SEED,
            DEVELOPMENT_RUN_SIZE,
        )
        validation_selected = sample_complete_runs(
            validation,
            RUNS_PER_CLASS_PER_DEVELOPMENT_SPLIT,
            FINAL_SEED + 10000,
            DEVELOPMENT_RUN_SIZE,
        )
        development = pd.concat(
            [train_selected, validation_selected], ignore_index=True
        )

        X_dev = development[FEATURES].to_numpy(dtype=np.float32, copy=False)
        y_dev = development["faultNumber"].to_numpy(
            dtype=np.int16, copy=False
        )
        X_test = test[FEATURES].to_numpy(dtype=np.float32, copy=False)
        y_test = test["faultNumber"].to_numpy(dtype=np.int16, copy=False)

        model = build_model(args.n_jobs)
        print(
            f"Ajustando XGBoost congelado em {len(y_dev):,} observações...",
            flush=True,
        )
        started = time.perf_counter()
        model.fit(X_dev, y_dev)
        training_seconds = time.perf_counter() - started

        print(
            f"Avaliando todas as {len(y_test):,} observações do teste...",
            flush=True,
        )
        started = time.perf_counter()
        predictions = model.predict(X_test)
        inference_seconds = time.perf_counter() - started

        metrics, by_class, matrix = evaluate(y_test, predictions)
        metrics.update(
            {
                "training_seconds": training_seconds,
                "inference_seconds": inference_seconds,
                "inference_ms_per_sample": (
                    1000 * inference_seconds / len(y_test)
                ),
                "n_development_rows": int(len(y_dev)),
                "n_test_rows": int(len(y_test)),
                "n_train_runs_per_class": (
                    RUNS_PER_CLASS_PER_DEVELOPMENT_SPLIT
                ),
                "n_validation_runs_per_class": (
                    RUNS_PER_CLASS_PER_DEVELOPMENT_SPLIT
                ),
                "development_run_size": DEVELOPMENT_RUN_SIZE,
                "test_run_size": TEST_RUN_SIZE,
            }
        )
        write_json(args.output / "final_test_metrics.json", metrics)
        pd.DataFrame([metrics]).to_csv(
            args.output / "final_test_metrics.csv", index=False
        )
        by_class.to_csv(args.output / "final_test_by_class.csv", index=False)
        pd.DataFrame(matrix, index=LABELS, columns=LABELS).to_csv(
            args.output / "final_test_confusion_matrix.csv",
            index_label="true_class",
        )
        prediction_frame = test[ID_COLUMNS].copy()
        prediction_frame["predicted_class"] = predictions.astype(np.int16)
        prediction_frame.to_parquet(
            args.output / "final_test_predictions.parquet", index=False
        )
        joblib.dump(
            model, args.output / "xgboost_frozen_final.joblib", compress=3
        )

        manifest.update(
            {
                "status": "PASS",
                "completed_at_utc": utc_now(),
                "metrics": metrics,
                "artifacts": sorted(p.name for p in args.output.iterdir()),
            }
        )
        write_json(manifest_path, manifest)
        (args.output / "FINAL_TEST_COMPLETE.lock").write_text(
            f"completed_at_utc={manifest['completed_at_utc']}\n",
            encoding="utf-8",
        )
        print("\nRESULTADO FINAL OFICIAL", flush=True)
        print(
            pd.DataFrame([metrics])[
                [
                    "accuracy",
                    "balanced_accuracy",
                    "f1_macro",
                    "f1_weighted",
                    "mcc",
                ]
            ].to_string(index=False),
            flush=True,
        )
        return 0
    except Exception as exc:
        manifest.update(
            {
                "status": "FAILED_AFTER_TEST_ACCESS",
                "failed_at_utc": utc_now(),
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )
        write_json(manifest_path, manifest)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
