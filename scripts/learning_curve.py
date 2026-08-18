#!/usr/bin/env python3
r"""
learning_curve.py -- macro-F1 on the validation partition as a function of the
number of complete simulation runs per class used for training.

Answers the question left open in the manuscript: whether the 840,000
observations used to fit the frozen model (40 runs per class from training plus
40 from validation) sit on the plateau of the learning curve or below it.

The frozen XGBoost hyperparameters are used unchanged. Runs are sampled at the
run level, never at the observation level, so the leakage control of the main
protocol is preserved. The validation partition is scored in full.

Both labeling protocols are reported: literal (L), and post-onset (P, dropping
samples 1-20 of faulty development runs), so that the shape of the curve can be
checked to be independent of the convention.

Usage (from artigos_mestrado/):

    python3 scripts/learning_curve.py \
        --train data/processed/train.parquet \
        --validation data/processed/validation.parquet \
        --out results/wp1a_learning_curve \
        --n-jobs 24

    # quick check before committing to the full run
    python3 scripts/learning_curve.py --sizes 5,10 --n-jobs 24

Runtime: roughly two hours for the default sizes on 24 threads. Results are
written after each size, so an interrupted run is not lost.
"""

import argparse
import json
import os
import time

import numpy as np
import pandas as pd

# Frozen configuration reported in the manuscript.
FROZEN_PARAMS = dict(
    n_estimators=250,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
)
ID_COLS = ["sourceFile", "faultNumber", "simulationRun", "sample"]
ONSET_DEV = 21          # first post-onset sample in a 500-sample development run
N_CLASSES = 21


def metrics(y_true, y_pred):
    from sklearn.metrics import f1_score, accuracy_score, matthews_corrcoef
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/processed/train.parquet")
    ap.add_argument("--validation", default="data/processed/validation.parquet")
    ap.add_argument("--out", default="results/wp1a_learning_curve")
    ap.add_argument("--sizes", default="10,20,40,80,160",
                    help="complete runs per class, comma separated")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--n-jobs", type=int, default=8,
                    help="RECORD THIS VALUE: timings are meaningless without it")
    args = ap.parse_args()

    sizes = [int(x) for x in args.sizes.split(",")]
    os.makedirs(args.out, exist_ok=True)

    from xgboost import XGBClassifier

    print("Loading data ...")
    tr = pd.read_parquet(args.train)
    va = pd.read_parquet(args.validation)
    feats = [c for c in tr.columns if c not in ID_COLS]
    print(f"  train      : {tr.shape[0]:,} rows, {len(feats)} features")
    print(f"  validation : {va.shape[0]:,} rows")

    runs_available = tr.groupby("faultNumber")["simulationRun"].nunique()
    print(f"  runs per class in train: {runs_available.min()}"
          f"-{runs_available.max()}")

    Xva = va[feats]
    yva = va["faultNumber"].to_numpy()
    # post-onset mask: drop pre-injection samples of faulty runs
    keep = ~((va["faultNumber"].to_numpy() != 0)
             & (va["sample"].to_numpy() < ONSET_DEV))
    print(f"  validation pre-onset rows: {(~keep).sum():,} "
          f"({100 * (~keep).mean():.2f}%)")

    rng = np.random.default_rng(args.seed)
    rows = []

    for n in sizes:
        if n > runs_available.min():
            print(f"\n[{n} runs/class] SKIPPED: only "
                  f"{runs_available.min()} runs available in the smallest class")
            continue

        # sample complete runs, independently per class
        picked = []
        for cls, grp in tr.groupby("faultNumber"):
            ids = grp["simulationRun"].unique()
            picked.append(pd.DataFrame(
                {"faultNumber": cls,
                 "simulationRun": rng.choice(ids, size=n, replace=False)}))
        picked = pd.concat(picked)
        sub = tr.merge(picked, on=["faultNumber", "simulationRun"], how="inner")

        print(f"\n[{n} runs/class] {len(sub):,} training observations")
        model = XGBClassifier(**FROZEN_PARAMS, objective="multi:softprob",
                              num_class=N_CLASSES, eval_metric="mlogloss",
                              random_state=args.seed, n_jobs=args.n_jobs,
                              tree_method="hist")
        t0 = time.time()
        model.fit(sub[feats], sub["faultNumber"])
        fit_s = time.time() - t0

        pred = model.predict(Xva)
        mL = metrics(yva, pred)
        mP = metrics(yva[keep], pred[keep])
        row = {"runs_per_class": n, "train_rows": len(sub),
               "train_seconds": fit_s, "n_jobs": args.n_jobs,
               **{f"L_{k}": v for k, v in mL.items()},
               **{f"P_{k}": v for k, v in mP.items()}}
        rows.append(row)
        print(f"  fit {fit_s:8.1f} s | macro-F1  L={mL['macro_f1']:.4f}"
              f"  P={mP['macro_f1']:.4f}")

        # write after every size: an interrupted run keeps its partial results
        pd.DataFrame(rows).to_csv(f"{args.out}/learning_curve.csv", index=False)

    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No size could be evaluated.")

    print("\n" + "=" * 64)
    print(df[["runs_per_class", "train_rows", "L_macro_f1",
              "P_macro_f1", "train_seconds"]].to_string(index=False))
    print("=" * 64)

    # marginal gain between consecutive sizes, used to state saturation
    df = df.sort_values("runs_per_class").reset_index(drop=True)
    df["delta_L"] = df["L_macro_f1"].diff()
    df["delta_P"] = df["P_macro_f1"].diff()
    df.to_csv(f"{args.out}/learning_curve.csv", index=False)

    with open(f"{args.out}/learning_curve.tex", "w") as fh:
        fh.write("% Generated by learning_curve.py\n")
        fh.write(f"% n_jobs = {args.n_jobs}, seed = {args.seed}\n\n")
        fh.write("\\begin{tabular}{rrrr}\n\\toprule\n")
        fh.write("Runs/class & Observations & Macro-F1 (L) & Macro-F1 (P)\\\\\n")
        fh.write("\\midrule\n")
        for _, r in df.iterrows():
            fh.write(f"{int(r.runs_per_class)} & {int(r.train_rows):,} & "
                     f"{r.L_macro_f1:.4f} & {r.P_macro_f1:.4f}\\\\\n")
        fh.write("\\bottomrule\n\\end{tabular}\n\n")
        last = df.iloc[-1]
        fh.write(f"% largest marginal gain after 40 runs/class: "
                 f"{df[df.runs_per_class > 40]['delta_L'].max():.4f}\n")
        fh.write(f"% macro-F1 at 40 runs/class vs largest size: "
                 f"{df[df.runs_per_class == 40]['L_macro_f1'].values}"
                 f" vs {last.L_macro_f1:.4f}\n")

    json.dump({"sizes": sizes, "seed": args.seed, "n_jobs": args.n_jobs,
               "frozen_params": FROZEN_PARAMS},
              open(f"{args.out}/learning_curve_manifest.json", "w"), indent=2)

    print(f"\nWrote {args.out}/learning_curve.csv, .tex and manifest")


if __name__ == "__main__":
    main()
