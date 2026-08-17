from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from tep_research.protocol import (
    environment_metadata,
    feature_columns,
    file_sha256,
    load_protocol,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auditoria em streaming da base TEP")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/protocol.yaml"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/common/audit"))
    parser.add_argument("--chunksize", type=int, default=200_000)
    return parser.parse_args()


def audit_file(path: Path, protocol, chunksize: int) -> tuple[dict, pd.DataFrame]:
    rows = 0
    missing = 0
    infinite = 0
    class_counts: dict[int, int] = {}
    run_pairs: set[tuple[int, int]] = set()
    columns: list[str] | None = None

    for chunk in pd.read_csv(path, chunksize=chunksize):
        if columns is None:
            columns = chunk.columns.tolist()
        rows += len(chunk)
        missing += int(chunk.isna().sum().sum())
        numeric = chunk.select_dtypes(include=[np.number])
        infinite += int(np.isinf(numeric.to_numpy(copy=False)).sum())
        counts = chunk[protocol.class_col].value_counts()
        for class_id, count in counts.items():
            class_counts[int(class_id)] = class_counts.get(int(class_id), 0) + int(count)
        run_pairs.update(
            (int(c), int(r))
            for c, r in chunk[[protocol.class_col, protocol.run_col]].drop_duplicates().itertuples(index=False)
        )

    columns = columns or []
    features = feature_columns(columns, protocol)
    summary = {
        "file": path.name,
        "sha256": file_sha256(path),
        "rows": rows,
        "columns": len(columns),
        "feature_columns": len(features),
        "runs": len(run_pairs),
        "missing_values": missing,
        "infinite_values": infinite,
        "class_ids": sorted(class_counts),
    }
    class_table = pd.DataFrame(
        [{"file": path.name, "class_id": key, "rows": value} for key, value in sorted(class_counts.items())]
    )
    return summary, class_table


def main() -> None:
    args = parse_args()
    protocol = load_protocol(args.config)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    class_tables = []
    for filename in protocol.files:
        path = args.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Arquivo obrigatorio ausente: {path}")
        summary, table = audit_file(path, protocol, args.chunksize)
        summaries.append(summary)
        class_tables.append(table)

    audit = pd.DataFrame(summaries)
    audit.to_csv(args.output_dir / "tep_file_audit.csv", index=False)
    pd.concat(class_tables, ignore_index=True).to_csv(
        args.output_dir / "tep_class_distribution.csv", index=False
    )
    total_rows = int(audit["rows"].sum())
    observed_classes = sorted(
        set().union(*(set(item["class_ids"]) for item in summaries))
    )
    checks = {
        "total_rows": total_rows,
        "expected_features": protocol.expected_features,
        "all_files_have_expected_features": bool(
            (audit["feature_columns"] == protocol.expected_features).all()
        ),
        "observed_classes": observed_classes,
        "classes_match_protocol": observed_classes == list(protocol.expected_classes),
        "missing_values": int(audit["missing_values"].sum()),
        "infinite_values": int(audit["infinite_values"].sum()),
        "environment": environment_metadata(),
    }
    write_json(checks, args.output_dir / "tep_metadata.json")
    print(json.dumps(checks, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

