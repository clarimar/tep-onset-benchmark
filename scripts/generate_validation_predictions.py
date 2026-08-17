#!/usr/bin/env python3
"""
generate_validation_predictions.py
==================================

Produces a predictions parquet for the validation partition from an already
saved model, so that postonset_analysis.py can be run with --onset 21.

No training happens here.

Usage
-----
    python3 generate_validation_predictions.py \
        --model results/wp1a_definitive/tuning_v2/candidates/xgboost_1.joblib \
        --data  data/processed/validation.parquet \
        --out   results/wp1a_onset_validation/validation_predictions.parquet

Then:
    python3 scripts/postonset_analysis.py \
        results/wp1a_onset_validation/validation_predictions.parquet \
        --cols faultNumber,simulationRun,sample,predicted_class \
        --onset 21 --out results/wp1a_onset_validation

Note the --onset 21: development runs are 500 samples long with the fault
injected after one hour, i.e. from sample 21. Using the test default of 161
here would be wrong.
"""

import argparse
import os
import time

import joblib
import numpy as np
import pandas as pd

ID_COLS = ["sourceFile", "faultNumber", "simulationRun", "sample"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--chunk", type=int, default=250_000,
                    help="rows per prediction batch (memory control)")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    print("Loading model  :", args.model)
    model = joblib.load(args.model)
    print("  type:", type(model).__name__)

    print("Loading data   :", args.data)
    df = pd.read_parquet(args.data)
    print("  shape:", df.shape)

    ids = [c for c in ID_COLS if c in df.columns]
    for required in ("faultNumber", "simulationRun", "sample"):
        if required not in ids:
            raise SystemExit(f"Missing identifier column '{required}'.")

    feature_cols = [c for c in df.columns if c not in ID_COLS]

    # Respect the feature order the model was fitted with, when recorded.
    expected = getattr(model, "feature_names_in_", None)
    if expected is None:  # e.g. a Pipeline wrapping the estimator
        last = getattr(model, "steps", None)
        if last:
            expected = getattr(last[-1][1], "feature_names_in_", None)
    if expected is not None:
        expected = list(expected)
        missing = set(expected) - set(feature_cols)
        if missing:
            raise SystemExit(f"Model expects columns absent from the data: "
                             f"{sorted(missing)[:5]}")
        if expected != feature_cols:
            print("  reordering features to match the fitted model")
        feature_cols = expected
    else:
        print("  model records no feature names; using column order as-is")

    print(f"  features: {len(feature_cols)} "
          f"({feature_cols[0]} ... {feature_cols[-1]})")
    if len(feature_cols) != 52:
        print(f"  WARNING: expected 52 predictors, found {len(feature_cols)}")

    # Keep a DataFrame so that column names are validated by the estimator
    # rather than silently relying on positional order.
    X = df[feature_cols]
    n = len(X)
    preds = np.empty(n, dtype=np.int16)

    t0 = time.time()
    for start in range(0, n, args.chunk):
        stop = min(start + args.chunk, n)
        preds[start:stop] = model.predict(X.iloc[start:stop]).astype(np.int16)
        print(f"  predicted {stop:,}/{n:,}", end="\r")
    elapsed = time.time() - t0
    print(f"\nInference: {elapsed:.1f} s "
          f"({1000 * elapsed / n:.6f} ms per observation)")

    out = df[ids].copy()
    out["predicted_class"] = preds

    # Sanity check before writing: accuracy under literal labels.
    acc = float((out["predicted_class"] == out["faultNumber"]).mean())
    print(f"Literal-label accuracy on this partition: {acc:.4f}")
    if acc < 0.2:
        print("  WARNING: accuracy near chance (1/21 = 0.048). Check that the "
              "feature order and the standardization match those used in "
              "fitting before trusting any downstream analysis.")

    out.to_parquet(args.out, index=False)
    print("Wrote", args.out, f"({len(out):,} rows)")


if __name__ == "__main__":
    main()
