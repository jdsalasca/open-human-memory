"""Reproduce Prototype 005 and write raw results.

Three questions: how many behaviours the grid really contains, how the value of a
learned library depends on continuity, and what an online bounded agent does.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v5_experiment import run  # noqa: E402

SEEDS = (0, 1, 2)


def mean(values):
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return round(sum(clean) / len(clean), 4)


def main() -> None:
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    results = []
    for seed in SEEDS:
        result = run(seed)
        results.append(result)
        (out_dir / f"seed-{seed}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        print(f"wrote seed-{seed}.json")

    coverage = {
        "syntactic": results[0]["coverage"]["syntactic"],
        "behavioral": results[0]["coverage"]["behavioral"],
        "learned_d2_on_representatives": mean(
            [r["coverage"]["learned_d2_on_representatives"] for r in results]
        ),
        "no_memory_d3_on_representatives": mean(
            [r["coverage"]["no_memory_d3_on_representatives"] for r in results]
        ),
    }

    keys = sorted(
        {(r["level"], r["condition"]) for r in results[0]["continuity"]},
        key=lambda k: (k[0], k[1]),
    )
    continuity = []
    for level, condition in keys:
        rows = [
            row
            for r in results
            for row in r["continuity"]
            if row["level"] == level and row["condition"] == condition
        ]
        continuity.append(
            {
                "level": level,
                "condition": condition,
                "accuracy": mean([r["accuracy"] for r in rows]),
                "mean_executed_steps": mean([r["mean_executed_steps"] for r in rows]),
            }
        )

    by_level = {}
    for row in continuity:
        by_level.setdefault(row["level"], {})[row["condition"]] = row
    derived = {
        "zero_continuity_accuracy_gap": round(
            by_level[0.0]["no-memory-d3-uncapped"]["accuracy"]
            - by_level[0.0]["learned-d2-uncapped"]["accuracy"],
            4,
        ),
        "full_continuity_work_saving": round(
            1
            - by_level[1.0]["learned-d2-uncapped"]["mean_executed_steps"]
            / by_level[1.0]["no-memory-d3-uncapped"]["mean_executed_steps"],
            4,
        ),
        "budgeted_macrofirst_at_full_continuity": by_level[1.0][
            "learned-d2-macrofirst-budget"
        ]["accuracy"],
        "budgeted_primitives_first_at_full_continuity": by_level[1.0][
            "learned-d2-budget"
        ]["accuracy"],
    }

    oracle = {
        key: mean([r["oracle"][key] for r in results]) for key in results[0]["oracle"]
    }

    policies = []
    for name in [p["policy"] for p in results[0]["stream"]["policies"]]:
        rows = [
            p for r in results for p in r["stream"]["policies"] if p["policy"] == name
        ]
        phases = results[0]["stream"]["phases"]
        policies.append(
            {
                "policy": name,
                "per_phase_accuracy": [
                    mean([p["per_phase"][i]["accuracy"] for p in rows])
                    for i in range(len(phases))
                ],
                "per_phase_steps": [
                    mean([p["per_phase"][i]["mean_executed_steps"] for p in rows])
                    for i in range(len(phases))
                ],
                "overall_accuracy": mean([p["overall_accuracy"] for p in rows]),
                "total_executed_steps": mean([p["total_executed_steps"] for p in rows]),
                "tasks_to_competence": mean([p["tasks_to_competence"] for p in rows]),
                "final_library_size": mean(
                    [p["per_phase"][-1]["library_size"] for p in rows]
                ),
            }
        )

    by_policy = {p["policy"]: p for p in policies}
    stream_derived = {
        "frozen_work_saving_vs_nolearn": round(
            1
            - by_policy["FROZEN"]["total_executed_steps"]
            / by_policy["NOLEARN"]["total_executed_steps"],
            4,
        ),
        "frozen_accuracy_gap_vs_nolearn": round(
            by_policy["FROZEN"]["overall_accuracy"]
            - by_policy["NOLEARN"]["overall_accuracy"],
            4,
        ),
        "online_accuracy_gap_vs_frozen": round(
            by_policy["ONLINE"]["overall_accuracy"]
            - by_policy["FROZEN"]["overall_accuracy"],
            4,
        ),
        "gated_accuracy_gap_vs_frozen": round(
            by_policy["GATED"]["overall_accuracy"]
            - by_policy["FROZEN"]["overall_accuracy"],
            4,
        ),
    }

    summary = {
        "seeds": list(SEEDS),
        "budget_steps": results[0]["budget_steps"],
        "coverage": coverage,
        "continuity": continuity,
        "continuity_derived": derived,
        "oracle": oracle,
        "stream": {"phases": results[0]["stream"]["phases"], "policies": policies},
        "stream_derived": stream_derived,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("wrote summary.json")
    print(json.dumps(derived, indent=2))
    print(json.dumps(stream_derived, indent=2))


if __name__ == "__main__":
    main()
