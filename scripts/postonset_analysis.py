#!/usr/bin/env python3
"""
postonset_analysis.py
=====================

Recomputes every value marked \\TBD{...} in the revised manuscript, starting
from the predictions that were already saved by the frozen evaluation. No model
is refitted: the same predictions are scored under two label conventions.

Background
----------
In the expanded TEP data (Rieth et al., 2017) the fault is injected after a
fixed warm-up interval:

    faulty *development* runs : 500 samples, fault active from sample  21
    faulty *test*        runs : 960 samples, fault active from sample 161
    fault-free runs           : no injection

Samples before the injection therefore carry a fault label while describing
nominal operation. Under literal labels this imposes a recall ceiling of
800/960 = 0.8333 on every fault class in the official test partition.

    Literal  (L): keep every observation as distributed.
    Post-onset (P): drop pre-onset observations of faulty runs.

Input
-----
A CSV (or Parquet) of the frozen test predictions with at least:

    faultNumber     true class, 0..20
    simulationRun   run identifier within the class
    sample          1-based sample index inside the run
    prediction      predicted class, 0..20

Column names are auto-detected from common aliases; override with --cols.

Usage
-----
    python postonset_analysis.py predictions.csv --out results/
    python postonset_analysis.py predictions.csv --bootstrap 1000 --seed 2026
    python postonset_analysis.py predictions.csv --cols faultNumber,simulationRun,sample,y_pred

Outputs (in --out)
------------------
    metrics_literal.csv        global + per-class metrics, protocol L
    metrics_postonset.csv      global + per-class metrics, protocol P
    preonset_destinations.csv  where pre-onset observations are sent
    bootstrap_summary.csv      run-level 95% intervals, both protocols
    tbd_values.tex             LaTeX fragment with every \\TBD{} filled in
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

N_CLASSES = 21
ONSET_TEST = 161          # first post-onset sample index in a faulty test run
ONSET_DEV = 21            # first post-onset sample index in a faulty dev run
RUN_LEN_TEST = 960

ALIASES = {
    "true": ["faultNumber", "fault_number", "y_true", "true", "label", "target"],
    "run": ["simulationRun", "simulation_run", "run", "run_id"],
    "sample": ["sample", "sample_index", "t", "timestep"],
    "pred": ["prediction", "y_pred", "pred", "predicted", "yhat"],
}


# --------------------------------------------------------------------------- io
def resolve_columns(df, override=None):
    if override:
        parts = [c.strip() for c in override.split(",")]
        if len(parts) != 4:
            sys.exit("--cols needs 4 names: true,run,sample,pred")
        return dict(zip(["true", "run", "sample", "pred"], parts))
    out = {}
    lower = {c.lower(): c for c in df.columns}
    for key, names in ALIASES.items():
        for n in names:
            if n.lower() in lower:
                out[key] = lower[n.lower()]
                break
        if key not in out:
            sys.exit(
                f"Could not find a column for '{key}'. Columns present: "
                f"{list(df.columns)}. Use --cols to specify them explicitly."
            )
    return out


def load(path, cols_override):
    if path.endswith((".parquet", ".pq")):
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)
    cols = resolve_columns(df, cols_override)
    df = df[[cols["true"], cols["run"], cols["sample"], cols["pred"]]].copy()
    df.columns = ["true", "run", "sample", "pred"]
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], downcast="integer")
    return df


# ---------------------------------------------------------------------- metrics
def confusion(true, pred, k=N_CLASSES):
    """Rows = true class, columns = predicted class."""
    idx = true.astype(np.int64) * k + pred.astype(np.int64)
    return np.bincount(idx, minlength=k * k).reshape(k, k)


def metrics_from_cm(cm):
    """Global and per-class metrics computed directly from a confusion matrix."""
    n = cm.sum()
    if n == 0:
        return {}, pd.DataFrame()
    tp = np.diag(cm).astype(float)
    t = cm.sum(axis=1).astype(float)          # true support per class
    p = cm.sum(axis=0).astype(float)          # predicted count per class

    with np.errstate(divide="ignore", invalid="ignore"):
        precision = np.where(p > 0, tp / p, 0.0)
        recall = np.where(t > 0, tp / t, 0.0)
        denom = precision + recall
        f1 = np.where(denom > 0, 2 * precision * recall / denom, 0.0)

    present = t > 0
    accuracy = tp.sum() / n
    balanced = recall[present].mean() if present.any() else 0.0
    macro_f1 = f1[present].mean() if present.any() else 0.0
    weighted_f1 = float((f1 * t).sum() / t.sum()) if t.sum() else 0.0

    # multiclass MCC in closed form (Gorodkin / Matthews generalization)
    num = n * tp.sum() - float((p * t).sum())
    den = np.sqrt((n**2 - float((p**2).sum())) * (n**2 - float((t**2).sum())))
    mcc = num / den if den > 0 else 0.0

    glob = {
        "n_observations": int(n),
        "accuracy": accuracy,
        "balanced_accuracy": balanced,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "mcc": mcc,
    }
    per = pd.DataFrame(
        {
            "class": np.arange(len(tp)),
            "support": t.astype(int),
            "predicted_count": p.astype(int),
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }
    )
    return glob, per


# ----------------------------------------------------------------- run-level cm
def per_run_confusions(df, mask=None):
    """One 21x21 confusion matrix per run. Returns (array[n_runs,21,21], keys)."""
    d = df if mask is None else df[mask]
    keys = d.groupby(["true", "run"], sort=True).ngroup()
    n_runs = int(keys.max()) + 1 if len(keys) else 0
    flat = (
        keys.to_numpy() * (N_CLASSES * N_CLASSES)
        + d["true"].to_numpy(np.int64) * N_CLASSES
        + d["pred"].to_numpy(np.int64)
    )
    cms = np.bincount(flat, minlength=n_runs * N_CLASSES * N_CLASSES)
    return cms.reshape(n_runs, N_CLASSES, N_CLASSES), n_runs


def bootstrap_ci(run_cms, n_boot, seed):
    rng = np.random.default_rng(seed)
    n_runs = run_cms.shape[0]
    flat = run_cms.reshape(n_runs, -1).astype(np.int64)
    stats = {"accuracy": [], "balanced_accuracy": [], "macro_f1": [], "mcc": []}
    for _ in range(n_boot):
        pick = rng.integers(0, n_runs, n_runs)
        cm = flat[pick].sum(axis=0).reshape(N_CLASSES, N_CLASSES)
        g, _ = metrics_from_cm(cm)
        for k in stats:
            stats[k].append(g[k])
    rows = []
    for k, v in stats.items():
        v = np.asarray(v)
        rows.append(
            {
                "metric": k,
                "mean": v.mean(),
                "ci_low": np.percentile(v, 2.5),
                "ci_high": np.percentile(v, 97.5),
            }
        )
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("predictions")
    ap.add_argument("--out", default="onset_analysis")
    ap.add_argument("--onset", type=int, default=ONSET_TEST,
                    help=f"first post-onset sample index (default {ONSET_TEST} "
                         f"for official test runs; use {ONSET_DEV} for dev runs)")
    ap.add_argument("--bootstrap", type=int, default=1000,
                    help="run-level bootstrap replicates (0 to skip)")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--cols", default=None,
                    help="explicit column names: true,run,sample,pred")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    df = load(args.predictions, args.cols)

    # --- structural audit -------------------------------------------------
    print("Loaded", f"{len(df):,}", "observations,",
          df["true"].nunique(), "classes")
    lens = df.groupby(["true", "run"]).size()
    print("Run lengths observed:", sorted(lens.unique().tolist())[:5],
          "| number of runs:", f"{len(lens):,}")
    if RUN_LEN_TEST not in lens.unique() and args.onset == ONSET_TEST:
        print("WARNING: no run of length 960 found. Is --onset correct for "
              "this partition?")

    is_faulty = df["true"].to_numpy() != 0
    is_preonset = is_faulty & (df["sample"].to_numpy() < args.onset)
    print(f"Pre-onset observations (faulty runs, sample < {args.onset}): "
          f"{is_preonset.sum():,} "
          f"({100 * is_preonset.mean():.2f}% of the partition)")

    # --- protocol L -------------------------------------------------------
    cm_L = confusion(df["true"].to_numpy(), df["pred"].to_numpy())
    glob_L, per_L = metrics_from_cm(cm_L)

    # --- protocol P -------------------------------------------------------
    keep = ~is_preonset
    cm_P = confusion(df["true"].to_numpy()[keep], df["pred"].to_numpy()[keep])
    glob_P, per_P = metrics_from_cm(cm_P)

    # --- where do pre-onset observations go? ------------------------------
    pre = df[is_preonset]
    dest = (
        pre.groupby("pred").size().rename("count").reset_index()
        .assign(share=lambda d: d["count"] / d["count"].sum())
        .sort_values("share", ascending=False)
    )
    share_normal = float(dest.loc[dest["pred"] == 0, "share"].sum())
    share_ambig = float(dest.loc[dest["pred"].isin([3, 9, 15]), "share"].sum())
    share_correct = float((pre["pred"].to_numpy() == pre["true"].to_numpy()).mean())

    # --- write tables -----------------------------------------------------
    pd.DataFrame([glob_L]).to_csv(f"{args.out}/global_literal.csv", index=False)
    pd.DataFrame([glob_P]).to_csv(f"{args.out}/global_postonset.csv", index=False)
    per_L.to_csv(f"{args.out}/metrics_literal.csv", index=False)
    per_P.to_csv(f"{args.out}/metrics_postonset.csv", index=False)
    dest.to_csv(f"{args.out}/preonset_destinations.csv", index=False)

    # --- bootstrap --------------------------------------------------------
    boot_L = boot_P = None
    if args.bootstrap > 0:
        print(f"Bootstrapping {args.bootstrap} run-level replicates ...")
        runs_L, n_L = per_run_confusions(df)
        boot_L = bootstrap_ci(runs_L, args.bootstrap, args.seed)
        boot_L.insert(0, "protocol", "literal")
        runs_P, n_P = per_run_confusions(df, mask=keep)
        boot_P = bootstrap_ci(runs_P, args.bootstrap, args.seed)
        boot_P.insert(0, "protocol", "post-onset")
        pd.concat([boot_L, boot_P]).to_csv(
            f"{args.out}/bootstrap_summary.csv", index=False)
        print(f"  runs resampled: literal={n_L:,}  post-onset={n_P:,}")

    # --- console summary --------------------------------------------------
    def line(name, a, b):
        print(f"  {name:<20s} {a:>10.4f}  ->  {b:>10.4f}   ({b - a:+.4f})")

    print("\n" + "=" * 62)
    print("  metric                literal      post-onset      delta")
    print("=" * 62)
    for k in ["accuracy", "balanced_accuracy", "macro_f1", "weighted_f1", "mcc"]:
        line(k, glob_L[k], glob_P[k])
    print("=" * 62)
    print(f"Pre-onset observations sent to class 0        : {share_normal:.4f}")
    print(f"Pre-onset observations sent to classes 3/9/15 : {share_ambig:.4f}")
    print(f"Pre-onset observations 'correct' under labels : {share_correct:.4f}")

    gap_L = 0.7683 - glob_L["macro_f1"]
    gap_P = 0.7683 - glob_P["macro_f1"]
    if abs(gap_L) > 1e-9:
        print(f"\nValidation macro-F1 (0.7683) minus test macro-F1:")
        print(f"  literal    gap = {gap_L:+.4f}")
        print(f"  post-onset gap = {gap_P:+.4f}")
        if gap_L > 0 and gap_P >= 0:
            print(f"  share of the gap removed by the onset correction: "
                  f"{1 - gap_P / gap_L:.1%}")
        elif gap_L > 0:
            print("  the onset correction more than closes the gap: the "
                  "post-onset test score exceeds the validation score")

    # --- LaTeX fragment ---------------------------------------------------
    ceiling = (RUN_LEN_TEST - (args.onset - 1)) / RUN_LEN_TEST
    good = per_P[~per_P["class"].isin([0, 3, 9, 15])]
    ambig = per_P[per_P["class"].isin([0, 3, 9, 15])]
    with open(f"{args.out}/tbd_values.tex", "w") as fh:
        fh.write("% Generated by postonset_analysis.py -- paste into main.tex\n")
        fh.write(f"% structural recall ceiling: {ceiling:.4f}\n\n")
        for k, v in glob_P.items():
            fh.write(f"% post-onset {k}: {v}\n")
        fh.write(f"\n% pre-onset -> class 0            : {share_normal * 100:.2f}\\%\n")
        fh.write(f"% pre-onset -> classes 3, 9, 15    : {share_ambig * 100:.2f}\\%\n")
        if len(good):
            fh.write(f"% post-onset recall, 17 separable  : "
                     f"{good['recall'].min():.4f}--{good['recall'].max():.4f}\n")
        if len(ambig):
            vals = ", ".join(f"{c}:{r:.4f}" for c, r in
                             zip(ambig['class'], ambig['f1']))
            fh.write(f"% post-onset F1, ambiguity group   : {vals}\n")
        fh.write("\n\\begin{tabular}{lcc}\n\\toprule\n")
        fh.write("Metric & Literal (L) & Post-onset (P)\\\\\n\\midrule\n")
        for label, key in [("Accuracy", "accuracy"),
                           ("Balanced accuracy", "balanced_accuracy"),
                           ("Macro-F1", "macro_f1"),
                           ("MCC", "mcc")]:
            fh.write(f"{label} & {glob_L[key]:.4f} & {glob_P[key]:.4f}\\\\\n")
        fh.write(f"Observations & {glob_L['n_observations']:,} & "
                 f"{glob_P['n_observations']:,}\\\\\n")
        fh.write("\\bottomrule\n\\end{tabular}\n")

    print(f"\nWrote outputs to {args.out}/  (see tbd_values.tex)")


if __name__ == "__main__":
    main()
