from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from tep_research.protocol import assert_disjoint_splits, load_protocol


def main() -> None:
    parser = argparse.ArgumentParser(description="Validacao metodologica do manifesto")
    parser.add_argument("--manifest", type=Path, default=Path("results/common/tep_run_manifest.csv"))
    parser.add_argument("--config", type=Path, default=Path("configs/protocol.yaml"))
    args = parser.parse_args()
    protocol = load_protocol(args.config)
    manifest = pd.read_csv(args.manifest)
    assert_disjoint_splits(manifest)
    observed = tuple(sorted(manifest["class_id"].unique().tolist()))
    if observed != protocol.expected_classes:
        raise ValueError(f"Classes observadas {observed}; esperadas {protocol.expected_classes}")
    coverage = manifest.groupby(["class_id", "split"]).size().unstack(fill_value=0)
    if (coverage == 0).any().any():
        raise ValueError(f"Ha classes sem execucoes em algum conjunto:\n{coverage}")
    print("Manifesto valido: nenhuma execucao atravessa conjuntos.")
    print(coverage)


if __name__ == "__main__":
    main()

