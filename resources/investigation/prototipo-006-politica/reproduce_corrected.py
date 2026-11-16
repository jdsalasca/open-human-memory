"""Reproduce the corrected Prototype 006-A'.

Not confirmatory: it corrects five implementation faults found by the direction
audit after the frozen run. The frozen run is archived in `results/`; this one
writes to `results/corrected/`. Comparisons are paired by task, and the reported
intervals are bootstrap resamples over tasks.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v6_policy import run  # noqa: E402

SEEDS = (1, 2)
BOOTSTRAP = 2000


def mean(values):
    return sum(values) / len(values) if values else 0.0


def paired_diff(a_flags, b_flags, seed: int = 0) -> dict:
    diffs = [a - b for a, b in zip(a_flags, b_flags)]
    rng = random.Random(seed)
    n = len(diffs)
    boots = sorted(
        mean([diffs[rng.randrange(n)] for _ in range(n)]) for _ in range(BOOTSTRAP)
    )
    return {
        "diff": round(mean(diffs), 4),
        "ci_low": round(boots[int(0.025 * BOOTSTRAP)], 4),
        "ci_high": round(boots[int(0.975 * BOOTSTRAP) - 1], 4),
        "n": n,
    }


def main() -> None:
    out_dir = HERE / "results" / "corrected"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for seed in SEEDS:
        result = run(seed)
        results.append(result)
        (out_dir / f"seed-{seed}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        print(f"wrote seed-{seed}.json")

    summary = {"seeds": list(SEEDS), "policies": {}, "paired": {}, "probe": {}}
    for label in ("policy-applicability", "policy-blind"):
        block = {"sets": {}}
        for set_name in ("similar", "novel", "mixed"):
            conditions = {}
            for condition in results[0]["policies"][label]["conditions"][set_name]:
                rows = [
                    r["policies"][label]["conditions"][set_name][condition]
                    for r in results
                ]
                conditions[condition] = {
                    "accuracy": round(mean([r["accuracy"] for r in rows]), 4),
                    "mean_steps": round(mean([r["mean_steps"] for r in rows]), 1),
                    "mean_probe_steps": round(
                        mean([r["mean_probe_steps"] for r in rows]), 1
                    ),
                    "total_steps": round(
                        mean([r.get("total_steps", r["mean_steps"]) for r in rows]),
                        1,
                    ),
                }
            block["sets"][set_name] = conditions
        block["weights"] = results[0]["policies"][label]["weights"]
        summary["policies"][label] = block

    app = "policy-applicability"
    for set_name in ("similar", "novel", "mixed"):
        conds = results[0]["policies"][app]["conditions"][set_name]
        policy_flags = [
            f
            for r in results
            for f in r["policies"][app]["conditions"][set_name]["learned-policy"][
                "correct_flags"
            ]
        ]
        for other in ("memory_first", "search", "probe-rule", "shuffled-policy"):
            other_flags = [
                f
                for r in results
                for f in r["policies"][app]["conditions"][set_name][other][
                    "correct_flags"
                ]
            ]
            summary["paired"][f"{set_name}:policy_vs_{other}"] = paired_diff(
                policy_flags, other_flags, seed=hash(set_name + other) % 1000
            )

    for set_name in ("similar", "novel", "mixed"):
        rows = [
            r["policies"][app]["conditions"][set_name]["learned-policy"]
            for r in results
        ]
        summary["probe"][set_name] = {
            "mean_probe_steps": round(mean([r["mean_probe_steps"] for r in rows]), 1),
            "mean_search_steps": round(mean([r["mean_steps"] for r in rows]), 1),
            "mean_total_steps": round(mean([r["total_steps"] for r in rows]), 1),
        }

    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("wrote summary.json")
    for key, value in summary["paired"].items():
        print(f"{key}: {value}")
    print(json.dumps(summary["probe"], indent=2))


if __name__ == "__main__":
    main()
