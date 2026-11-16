"""Upper bound on the applicability probe's cost (SUPERSEDED).

The corrected `v6_policy.probe` counts executed primitive applications with
short-circuit; that is the measurement of record (`results/corrected/`). This
script is kept only because the frozen addendum cites it, and it reports the
bound, not the measurement.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v3_tasks import PRIMITIVES, apply_program  # noqa: E402
from ohmem.v6_policy import build_library, novel_tasks, similar_tasks  # noqa: E402

SEEDS = (1, 2)


def probe_cost(obs, library) -> int:
    steps = 0
    for macro in library.macros:
        for primitive in PRIMITIVES:
            for body in (macro.body + (primitive,), (primitive,) + macro.body):
                steps += len(body) * len(obs.support_inputs)
                if all(
                    apply_program(body, x) == y
                    for x, y in zip(obs.support_inputs, obs.support_outputs)
                ):
                    return steps
    return steps


def main() -> None:
    rows = {}
    for seed in SEEDS:
        library = build_library(seed)
        sets = {
            "similar": similar_tasks(seed),
            "novel": novel_tasks(seed, library),
        }
        for name, tasks in sets.items():
            costs = [probe_cost(task.observation, library) for task in tasks]
            rows.setdefault(name, []).extend(costs)
    summary = {
        name: {
            "mean_probe_steps": round(sum(values) / len(values), 1),
            "max_probe_steps": max(values),
            "n": len(values),
        }
        for name, values in rows.items()
    }
    out = HERE / "results" / "probe-cost.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
