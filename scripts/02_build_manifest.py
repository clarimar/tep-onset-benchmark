from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from tep_research.protocol import assert_disjoint_splits, load_protocol


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construcao do manifesto por execucao")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/protocol.yaml"))
    parser.add_argument("--output", type=Path, default=Path("results/common/tep_run_manifest.csv"))
    parser.add_argument("--seed", type=int)
    return parser.parse_args()


def collect_runs(path: Path, protocol, source_group: str) -> pd.DataFrame:
    usecols = [protocol.class_col, protocol.run_col]
    pieces = []
    for chunk in pd.read_csv(path, usecols=usecols, chunksize=500_000):
        pieces.append(chunk.drop_duplicates())
    result = pd.concat(pieces, ignore_index=True).drop_duplicates()
    return result.rename(columns={protocol.class_col: "class_id", protocol.run_col: "run_id"}).assign(
        source_file=path.name, source_group=source_group
    )


def main() -> None:
    args = parse_args()
    protocol = load_protocol(args.config)
    seed = protocol.seed if args.seed is None else args.seed
    frames = []
    for filename in protocol.files:
        group = "test" if "testing" in filename else "development"
        frames.append(collect_runs(args.data_dir / filename, protocol, group))
    runs = pd.concat(frames, ignore_index=True)

    official_test = runs[runs["source_group"] == "test"].copy()
    official_test["split"] = "test"
    development = runs[runs["source_group"] == "development"].copy()
    rng = np.random.default_rng(seed)
    assigned = []
    for class_id, group in development.groupby("class_id", sort=True):
        group = group.sort_values(["source_file", "run_id"]).copy()
        order = rng.permutation(len(group))
        n_validation = max(1, int(round(len(group) * protocol.validation_fraction)))
        group["split"] = "train"
        group.iloc[order[:n_validation], group.columns.get_loc("split")] = "validation"
        assigned.append(group)

    manifest = pd.concat([*assigned, official_test], ignore_index=True)
    manifest["seed"] = seed
    manifest = manifest.sort_values(["split", "class_id", "run_id"]).reset_index(drop=True)
    assert_disjoint_splits(manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(args.output, index=False)
    print(manifest.groupby(["split", "class_id"]).size().unstack(fill_value=0))
    print("\nExecucoes por conjunto:")
    print(manifest["split"].value_counts())


if __name__ == "__main__":
    main()

