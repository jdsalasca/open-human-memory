"""Run Prototype 002: label-free diagnostic with compositional transfer."""

from __future__ import annotations

import argparse
import json

from .v2_conditions import (
    Abstraction,
    CurrentSolver,
    NoMemory,
    Oracle,
    Procedure,
    Retrieval,
)
from .v2_tasks import apply_rule, make_splits


def run(seed: int = 0, n_train: int = 200, n_eval: int = 50) -> dict:
    splits = make_splits(seed=seed, n_train=n_train, n_eval=n_eval)
    train = splits["train"]
    conditions = [
        NoMemory(),
        CurrentSolver(),
        Retrieval(train),
        Oracle(),
        Procedure(),
        Abstraction(),
    ]
    rows = []
    for condition in conditions:
        for distribution in ("D1", "D2", "D3"):
            tasks = splits[distribution]
            correct = 0
            reads = 0
            verifications = 0
            context_values = 0
            for task in tasks:
                if isinstance(condition, Oracle):
                    prediction = condition.predict(task.observation, task.solution)
                else:
                    prediction = condition.predict(task.observation)
                reads += prediction.memory_reads
                verifications += prediction.verification_calls
                context_values += prediction.context_values
                produced = apply_rule(prediction.rule, task.observation.query)
                expected = apply_rule(task.solution.rule, task.observation.query)
                if produced == expected:
                    correct += 1
            rows.append(
                {
                    "condition": condition.name,
                    "distribution": distribution,
                    "accuracy": round(correct / len(tasks), 4),
                    "cost": {
                        "memory_reads": reads,
                        "verification_calls": verifications,
                        "context_values": context_values,
                    },
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
    print(f"{'condition':<28} {'dist':<4} {'acc':>6} {'reads':>6} {'verify':>6}")
    for row in result["rows"]:
        cost = row["cost"]
        print(
            f"{row['condition']:<28} {row['distribution']:<4} "
            f"{row['accuracy']:>6.3f} {cost['memory_reads']:>6} "
            f"{cost['verification_calls']:>6}"
        )


if __name__ == "__main__":
    main()
