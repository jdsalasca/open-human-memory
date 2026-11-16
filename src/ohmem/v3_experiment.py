"""Prototype 003: measure whether learned macros improve future tasks."""

from __future__ import annotations

import argparse
import json

from .v3_library import Library, learn_macros, random_library
from .v3_solver import solve
from .v3_tasks import TRAIN_PROGRAMS, apply_program, make_splits


def train_library(seed: int, n_train: int) -> tuple[Library, int]:
    splits = make_splits(seed=seed, n_train=n_train, n_eval=1)
    solved = []
    for task in splits["train"]:
        result = solve(task.observation, Library([]), max_steps=2)
        if result.program is not None:
            solved.append(result.program)
    return learn_macros(solved, min_count=2), len(solved)


def run(seed: int = 0, n_train: int = 60, n_eval: int = 30) -> dict:
    splits = make_splits(seed=seed, n_train=n_train, n_eval=n_eval)
    learned, n_solved = train_library(seed, n_train)
    random_lib = random_library(
        len(learned.macros), seed=seed, exclude=set(TRAIN_PROGRAMS)
    )
    conditions = {
        "NOLEARN": Library([]),
        "RANDOM": random_lib,
        "LEARNED": learned,
        "ABLATED": Library([]),
    }
    rows = []
    for name, library in conditions.items():
        for distribution in ("D1", "D2", "D3"):
            tasks = splits[distribution]
            correct = 0
            candidates = 0
            primitive_ops = 0
            for task in tasks:
                result = solve(task.observation, library, max_steps=2)
                candidates += result.candidates
                primitive_ops += result.primitive_ops
                if result.program is not None:
                    produced = apply_program(result.program, task.observation.query)
                    expected = apply_program(
                        task.solution.program, task.observation.query
                    )
                    if produced == expected:
                        correct += 1
            rows.append(
                {
                    "condition": name,
                    "distribution": distribution,
                    "accuracy": round(correct / len(tasks), 4),
                    "library_size": library.size(),
                    "cost": {"candidates": candidates, "primitive_ops": primitive_ops},
                }
            )
    return {
        "seed": seed,
        "n_train": n_train,
        "n_eval": n_eval,
        "solved_train": n_solved,
        "learned_macros": [m.body for m in learned.macros],
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--train", type=int, default=60)
    parser.add_argument("--eval", type=int, default=30)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run(args.seed, args.train, args.eval)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(
        f"seed={result['seed']} train={result['n_train']} "
        f"solved={result['solved_train']} macros={len(result['learned_macros'])}"
    )
    print(f"{'condition':<10} {'dist':<4} {'acc':>6} {'lib':>4} {'cand':>6} {'ops':>6}")
    for row in result["rows"]:
        print(
            f"{row['condition']:<10} {row['distribution']:<4} "
            f"{row['accuracy']:>6.3f} {row['library_size']:>4} "
            f"{row['cost']['candidates']:>6} {row['cost']['primitive_ops']:>6}"
        )


if __name__ == "__main__":
    main()
