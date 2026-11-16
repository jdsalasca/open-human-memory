"""Run the diagnostic: memory vs selection vs procedure vs abstraction."""

from __future__ import annotations

import argparse
import json

from .conditions import build_conditions
from .tasks import apply_rule, make_splits


def run(seed: int = 0, n_train: int = 200, n_eval: int = 50) -> dict:
    splits = make_splits(seed=seed, n_train=n_train, n_eval=n_eval)
    conditions = build_conditions(splits["train"])
    rows = []
    for condition in conditions:
        for distribution in ("D1", "D2", "D3"):
            tasks = splits[distribution]
            correct = 0
            reads = 0
            for task in tasks:
                prediction = condition.predict(task)
                reads += prediction.memory_reads
                if apply_rule(prediction.rule, task.numbers) == task.expected:
                    correct += 1
            rows.append(
                {
                    "condition": condition.name,
                    "distribution": distribution,
                    "accuracy": round(correct / len(tasks), 4),
                    "memory_reads": reads,
                }
            )
    return {"seed": seed, "n_train": n_train, "n_eval": n_eval, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--train", type=int, default=200)
    parser.add_argument("--eval", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run(args.seed, args.train, args.eval)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"seed={result['seed']} train={result['n_train']} eval={result['n_eval']}")
    print(f"{'condition':<16} {'dist':<4} {'acc':>6} {'reads':>6}")
    for row in result["rows"]:
        print(
            f"{row['condition']:<16} {row['distribution']:<4} "
            f"{row['accuracy']:>6.3f} {row['memory_reads']:>6}"
        )


if __name__ == "__main__":
    main()
