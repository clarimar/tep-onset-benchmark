from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pandas as pd
import yaml
from sklearn.metrics import classification_report, confusion_matrix

from .core import (
    atomic_json,
    build_model,
    evaluate,
    identify_schema,
    read_split,
    serialized_size,
)


def main() -> int:
    p = argparse.ArgumentParser(
        description="WP1A: repeticoes finais em validacao; teste e opcional e explicito."
    )
    p.add_argument("--train", type=Path, required=True)
    p.add_argument("--validation", type=Path, required=True)
    p.add_argument("--selected", type=Path, required=True)
    p.add_argument("--test", type=Path)
    p.add_argument("--config", type=Path, default=Path("configs/protocol.yaml"))
    p.add_argument("--output", type=Path, default=Path("results/wp1a_definitive/final"))
    p.add_argument("--n-jobs", type=int, default=-1)
    args = p.parse_args()
    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    seeds = cfg["seeds"]["models"]
    out = args.output.resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"Saida ja existe: {out}")
    out.mkdir(parents=True)
    schema = identify_schema(args.train)
    selected = pd.read_csv(args.selected)
    Xtr, ytr, _ = read_split(
        args.train, schema, int(cfg["wp1a"]["final_runs_per_class"]), 42
    )
    Xv, yv, mv = read_split(args.validation, schema, 0, 42)
    test_data = read_split(args.test, schema, 0, 42) if args.test else None
    records = []
    for row in selected.itertuples(index=False):
        params = json.loads(row.params)
        for seed in seeds:
            model = build_model(row.model, params, int(seed), args.n_jobs)
            start = time.perf_counter()
            model.fit(Xtr, ytr)
            training = time.perf_counter() - start
            for split, data in (["validation", (Xv, yv, mv)], ["test", test_data]):
                if data is None:
                    continue
                X, y, meta = data
                metrics, pred = evaluate(model, X, y)
                records.append(
                    {
                        "model": row.model,
                        "seed": seed,
                        "split": split,
                        "training_seconds": training,
                        **metrics,
                    }
                )
                target = out / row.model / f"seed_{seed}" / split
                target.mkdir(parents=True, exist_ok=True)
                pd.DataFrame(confusion_matrix(y, pred)).to_csv(
                    target / "confusion_matrix.csv", index=False
                )
                pd.DataFrame(
                    classification_report(y, pred, output_dict=True, zero_division=0)
                ).T.to_csv(target / "classification_report.csv")
                meta.assign(y_true=y, y_pred=pred).to_parquet(
                    target / "predictions.parquet", index=False
                )
            serialized_size(model, out / row.model / f"seed_{seed}" / "model.joblib")
            pd.DataFrame(records).to_csv(out / "all_metrics.csv", index=False)
    summary = (
        pd.DataFrame(records)
        .groupby(["model", "split"])
        .agg(
            {
                "f1_macro": ["mean", "std"],
                "mcc": ["mean", "std"],
                "balanced_accuracy": ["mean", "std"],
                "training_seconds": ["mean", "std"],
                "inference_ms_per_sample": ["mean", "std"],
            }
        )
        .reset_index()
    )
    summary.columns = ["_".join(x).rstrip("_") for x in summary.columns]
    summary.to_csv(out / "aggregate_metrics.csv", index=False)
    atomic_json(
        out / "run_summary.json",
        {
            "status": "PASS",
            "seeds": seeds,
            "test_accessed": bool(args.test),
            "selection_source": str(args.selected.resolve()),
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
