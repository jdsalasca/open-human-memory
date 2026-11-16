"""Reproduce Prototype 002 (label-free diagnostic) and write raw results."""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v2_experiment import run  # noqa: E402
from ohmem.v2_longitudinal import run_curve  # noqa: E402


def main() -> None:
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    seeds = (0, 1, 2)
    all_rows = []
    for seed in seeds:
        result = run(seed=seed, n_train=200, n_eval=50)
        (out_dir / f"seed-{seed}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        all_rows.extend(result["rows"])
        print(f"wrote seed-{seed}.json")

    keys = sorted({(r["condition"], r["distribution"]) for r in all_rows})
    summary = []
    for condition, distribution in keys:
        values = [
            r["accuracy"]
            for r in all_rows
            if r["condition"] == condition and r["distribution"] == distribution
        ]
        summary.append(
            {
                "condition": condition,
                "distribution": distribution,
                "mean_accuracy": round(sum(values) / len(values), 4),
                "min": min(values),
                "max": max(values),
                "n": len(values),
            }
        )
    (out_dir / "summary.json").write_text(
        json.dumps({"seeds": seeds, "rows": summary}, indent=2), encoding="utf-8"
    )
    print("wrote summary.json")

    for seed in seeds:
        curve = run_curve(seed=seed, n_values=(50, 100, 200, 400), n_eval=50)
        (out_dir / f"longitudinal-seed-{seed}.json").write_text(
            json.dumps(curve, indent=2), encoding="utf-8"
        )
        print(f"wrote longitudinal-seed-{seed}.json")


if __name__ == "__main__":
    main()
