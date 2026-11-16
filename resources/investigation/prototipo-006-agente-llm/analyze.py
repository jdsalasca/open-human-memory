"""Paired analysis of the LLM diagnostic conditions (Prototype 006-B)."""

from __future__ import annotations

import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
CONDITIONS = ("base", "more_examples", "vocabulary", "retrieved", "tool_forced")
BOOTSTRAP = 2000


def load(condition: str) -> list[dict]:
    path = RESULTS / f"{condition.replace('_', '-')}-24.json"
    return json.loads(path.read_text(encoding="utf-8"))["rows"]


def mean(values):
    return sum(values) / len(values)


def paired(rows_a, rows_b, seed: int) -> dict:
    a = [row["correct"] for row in rows_a]
    b = [row["correct"] for row in rows_b]
    diffs = [x - y for x, y in zip(a, b)]
    rng = random.Random(seed)
    n = len(diffs)
    boots = sorted(
        mean([diffs[rng.randrange(n)] for _ in range(n)]) for _ in range(BOOTSTRAP)
    )
    return {
        "diff": round(mean(diffs), 4),
        "ci_low": round(boots[int(0.025 * BOOTSTRAP)], 4),
        "ci_high": round(boots[int(0.975 * BOOTSTRAP) - 1], 4),
        "both_correct": sum(1 for x, y in zip(a, b) if x and y),
        "a_only": sum(1 for x, y in zip(a, b) if x and not y),
        "b_only": sum(1 for x, y in zip(a, b) if y and not x),
        "neither": sum(1 for x, y in zip(a, b) if not x and not y),
        "n": n,
    }


def main() -> None:
    data = {condition: load(condition) for condition in CONDITIONS}
    summary = {"conditions": {}, "paired_vs_base": {}}
    for condition, rows in data.items():
        summary["conditions"][condition] = {
            "accuracy": round(mean([r["correct"] for r in rows]), 4),
            "correct": sum(1 for r in rows if r["correct"]),
            "parsed": sum(1 for r in rows if r["parsed"]),
            "mean_seconds": round(mean([r["seconds"] for r in rows]), 2),
            "n": len(rows),
        }
    for index, condition in enumerate(CONDITIONS[1:]):
        summary["paired_vs_base"][condition] = paired(
            data[condition], data["base"], seed=index
        )
    (RESULTS / "diagnostic-summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
