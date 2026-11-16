"""Measure how far the step budget can be exceeded (audit finding P0-4).

The solver checks the budget *before* evaluating a candidate, so an accepted
candidate can push `executed_steps` past the limit. This script quantifies the
overshoot on the 006-A conditions; it does not change any result.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v3_solver import solve  # noqa: E402
from ohmem.v6_policy import NO_MEMORY, build_library, novel_tasks, similar_tasks  # noqa: E402

SEEDS = (1, 2)
BUDGET = 120
ACTIONS = ("memory", "memory_first", "search")


def main() -> None:
    rows = []
    for seed in SEEDS:
        library = build_library(seed)
        sets = {
            "similar": similar_tasks(seed),
            "novel": novel_tasks(seed, library),
        }
        for set_name, tasks in sets.items():
            for action in ACTIONS:
                overshoots = []
                executed = []
                for task in tasks:
                    result = solve(
                        task.observation,
                        NO_MEMORY if action == "search" else library,
                        3 if action == "search" else 2,
                        budget_steps=BUDGET,
                        macro_first=action == "memory_first",
                    )
                    overshoots.append(max(0, result.executed_steps - BUDGET))
                    executed.append(result.executed_steps)
                rows.append(
                    {
                        "seed": seed,
                        "set": set_name,
                        "action": action,
                        "n": len(tasks),
                        "mean_executed": round(sum(executed) / len(executed), 1),
                        "mean_overshoot": round(sum(overshoots) / len(overshoots), 2),
                        "max_overshoot": max(overshoots),
                        "tasks_over_budget": sum(1 for o in overshoots if o > 0),
                    }
                )
    out = HERE / "results" / "budget-overshoot.json"
    out.write_text(
        json.dumps({"budget": BUDGET, "rows": rows}, indent=2), encoding="utf-8"
    )
    for row in rows:
        print(
            f"seed={row['seed']} {row['set']:<8} {row['action']:<13} "
            f"exec={row['mean_executed']:>6} over_mean={row['mean_overshoot']:>5} "
            f"over_max={row['max_overshoot']:>2} tasks={row['tasks_over_budget']}/{row['n']}"
        )


if __name__ == "__main__":
    main()
