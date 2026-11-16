"""Reproduce Prototype 003 (learned macros) and write raw results."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v3_experiment import run  # noqa: E402


def main() -> None:
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    seeds = (0, 1, 2)
    all_rows = []
    for seed in seeds:
        result = run(seed=seed, n_train=60, n_eval=30)
        (out_dir / f"seed-{seed}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        all_rows.extend(result["rows"])
        print(f"wrote seed-{seed}.json")

    keys = sorted({(r["condition"], r["distribution"]) for r in all_rows})
    summary = []
    for condition, distribution in keys:
        selected = [
            r
            for r in all_rows
            if r["condition"] == condition and r["distribution"] == distribution
        ]
        summary.append(
            {
                "condition": condition,
                "distribution": distribution,
                "mean_accuracy": round(
                    sum(r["accuracy"] for r in selected) / len(selected), 4
                ),
                "mean_candidates": round(
                    sum(r["cost"]["candidates"] for r in selected) / len(selected), 1
                ),
                "mean_primitive_ops": round(
                    sum(r["cost"]["primitive_ops"] for r in selected) / len(selected), 1
                ),
                "n": len(selected),
            }
        )
    (out_dir / "summary.json").write_text(
        json.dumps({"seeds": seeds, "rows": summary}, indent=2), encoding="utf-8"
    )
    print("wrote summary.json")


if __name__ == "__main__":
    main()
