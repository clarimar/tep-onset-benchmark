from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pandas as pd
import yaml

from .core import (
    GRIDS,
    atomic_json,
    build_model,
    evaluate,
    file_sha256,
    identify_schema,
    read_split,
    serialized_size,
)


def arguments():
    parser = argparse.ArgumentParser(
        description="WP1A: tuning cego ao teste, por execucoes completas."
    )
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/protocol.yaml"))
    parser.add_argument(
        "--output", type=Path, default=Path("results/wp1a_definitive/tuning")
    )
    parser.add_argument("--models", nargs="*", choices=sorted(GRIDS))
    parser.add_argument("--runs-per-class", type=int)
    parser.add_argument("--quick-check", action="store_true")
    parser.add_argument("--n-jobs", type=int, default=-1)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    wp = config["wp1a"]
    models = args.models or wp["models"]
    runs = (
        args.runs_per_class
        if args.runs_per_class is not None
        else int(wp["tuning_runs_per_class"])
    )
    if args.quick_check:
        models, runs = ["decision_tree"], 1
    out = args.output.resolve()
    if out.exists() and any(out.iterdir()):
        raise FileExistsError(f"Saida ja existe e nao sera sobrescrita: {out}")
    out.mkdir(parents=True)
    schema = identify_schema(args.train)
    if identify_schema(args.validation) != schema:
        raise ValueError("Esquemas de treino e validacao incompativeis.")
    seed = int(wp["tuning_seed"])
    X_train, y_train, meta_train = read_split(args.train, schema, runs, seed)
    X_val, y_val, meta_val = read_split(args.validation, schema, runs, seed)
    train_runs = set(
        map(tuple, meta_train[[schema.label, schema.run]].drop_duplicates().to_numpy())
    )
    val_runs = set(
        map(tuple, meta_val[[schema.label, schema.run]].drop_duplicates().to_numpy())
    )
    if train_runs & val_runs:
        raise RuntimeError(
            "Vazamento: execucoes compartilhadas entre treino e validacao."
        )
    manifest = {
        "train": str(args.train.resolve()),
        "validation": str(args.validation.resolve()),
        "train_sha256": file_sha256(args.train),
        "validation_sha256": file_sha256(args.validation),
        "features": list(schema.features),
        "n_train_rows": len(y_train),
        "n_validation_rows": len(y_val),
        "n_train_runs": len(train_runs),
        "n_validation_runs": len(val_runs),
        "runs_per_class": runs,
        "test_accessed": False,
    }
    atomic_json(out / "data_manifest.json", manifest)
    rows = []
    for name in models:
        grid = GRIDS[name][:1] if args.quick_check else GRIDS[name]
        for candidate, params in enumerate(grid, start=1):
            model = build_model(name, params, seed, args.n_jobs)
            start = time.perf_counter()
            model.fit(X_train, y_train)
            train_seconds = time.perf_counter() - start
            scores, _ = evaluate(model, X_val, y_val)
            size = serialized_size(
                model, out / "candidates" / f"{name}_{candidate}.joblib"
            )
            rows.append(
                {
                    "model": name,
                    "candidate": candidate,
                    "params": json.dumps(params, sort_keys=True),
                    "training_seconds": train_seconds,
                    "model_size_bytes": size,
                    **scores,
                }
            )
            pd.DataFrame(rows).to_csv(out / "validation_candidates.csv", index=False)
    table = pd.DataFrame(rows)
    table = table.sort_values(
        ["f1_macro", "mcc", "inference_ms_per_sample", "model_size_bytes"],
        ascending=[False, False, True, True],
    ).reset_index(drop=True)
    table.insert(0, "global_rank", range(1, len(table) + 1))
    winners = (
        table.sort_values(
            ["model", "f1_macro", "mcc", "inference_ms_per_sample", "model_size_bytes"],
            ascending=[True, False, False, True, True],
        )
        .groupby("model", as_index=False)
        .first()
    )
    table.to_csv(out / "validation_ranking.csv", index=False)
    winners.to_csv(out / "selected_hyperparameters.csv", index=False)
    atomic_json(
        out / "run_summary.json",
        {
            "status": "PASS",
            "models": models,
            "test_accessed": False,
            "best_model_validation": table.iloc[0]["model"],
            "quick_check": args.quick_check,
        },
    )
    print(
        table[["global_rank", "model", "candidate", "f1_macro", "mcc"]].to_string(
            index=False
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
