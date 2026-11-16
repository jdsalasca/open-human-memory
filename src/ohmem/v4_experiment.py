"""Prototype 004-A: does macro learning beat plain deeper search?

The external audit of Prototype 003 asked for eight validity controls. This
module implements them on the same solver and the same task generator:

1. A no-memory depth-3 baseline (the arbitrary depth-2 limit was ours).
2. Same-language, same-cardinality random libraries (all 560 of them).
3. The full 64-program depth-3 lattice instead of three chosen programs.
4. An acquisition curve from 0 to N experiences.
5. Shared vs incremental cost.
6. Which macro was used, and when it was harmful.
7. An honesty note about ablation (macros, not raw history).
8. A budget-matched comparison.

The confirmatory protocol is frozen in
`resources/investigation/prototipo-004-validez/protocolo-congelado.md`.
"""

from __future__ import annotations

import json
import random

from .v3_library import (
    Library,
    Macro,
    PAIRS,
    _name,
    learn_macros,
    same_language_libraries,
)
from .v3_solver import solve
from .v3_tasks import apply_program, make_depth3_grid, make_splits

CONDITIONS = {
    "A0-nolearn-d2": (Library([]), 2),
    "A1-nolearn-d3": (Library([]), 3),
    "A3-learned-d2": (None, 2),  # library filled from the training run
    "A4-learned-d3": (None, 3),
}


def train(seed: int, n_train: int) -> tuple[Library, dict]:
    splits = make_splits(seed=seed, n_train=n_train, n_eval=1)
    solved = []
    candidates = 0
    primitive_ops = 0
    for task in splits["train"]:
        result = solve(task.observation, Library([]), max_steps=2)
        candidates += result.candidates
        primitive_ops += result.primitive_ops
        if result.program is not None:
            solved.append(result.program)
    return learn_macros(solved), {
        "n_train": n_train,
        "solved": len(solved),
        "cost": {"candidates": candidates, "primitive_ops": primitive_ops},
    }


def evaluate(
    library: Library, max_steps: int, tasks, budget: int | None = None
) -> dict:
    correct = 0
    candidates = 0
    primitive_ops = 0
    macro_tasks = 0
    harmful = 0
    abstained = 0
    for task in tasks:
        result = solve(task.observation, library, max_steps, budget=budget)
        candidates += result.candidates
        primitive_ops += result.primitive_ops
        if result.program is None:
            abstained += 1
            continue
        produced = apply_program(result.program, task.observation.query)
        expected = apply_program(task.solution.program, task.observation.query)
        if produced == expected:
            correct += 1
        elif result.macros:
            harmful += 1
        if result.macros:
            macro_tasks += 1
    return {
        "accuracy": round(correct / len(tasks), 4),
        "correct": correct,
        "n": len(tasks),
        "macro_tasks": macro_tasks,
        "harmful_macro_tasks": harmful,
        "abstained": abstained,
        "cost": {"candidates": candidates, "primitive_ops": primitive_ops},
    }


def sweep(seed: int, tasks, limit: int | None = None) -> dict:
    """Every library of three macros drawn from the generator's own 16 pairs."""
    libraries = same_language_libraries(3)
    if limit is not None:
        libraries = libraries[:limit]
    rows = []
    for library in libraries:
        result = evaluate(library, 2, tasks)
        rows.append(
            {
                "macros": [list(m.body) for m in library.macros],
                "accuracy": result["accuracy"],
                "correct": result["correct"],
                "harmful_macro_tasks": result["harmful_macro_tasks"],
            }
        )
    accuracies = [r["accuracy"] for r in rows]
    ordered = sorted(accuracies)
    mid = len(ordered) // 2
    median = (
        ordered[mid]
        if len(ordered) % 2
        else round((ordered[mid - 1] + ordered[mid]) / 2, 4)
    )
    return {
        "n_libraries": len(rows),
        "mean_accuracy": round(sum(accuracies) / len(accuracies), 4),
        "median_accuracy": median,
        "max_accuracy": max(accuracies),
        "min_accuracy": min(accuracies),
        "perfect": sum(1 for a in accuracies if a == 1.0),
        "zero": sum(1 for a in accuracies if a == 0.0),
        "rows": rows,
    }


def acquisition(
    seed: int, tasks, n_values=(0, 1, 2, 3, 4, 5, 6, 8, 10, 20, 60)
) -> dict:
    rows = []
    for n in n_values:
        library, _ = train(seed, n)
        result = evaluate(library, 2, tasks)
        rows.append(
            {
                "n_train": n,
                "n_macros": len(library.macros),
                "accuracy": result["accuracy"],
                "cost": result["cost"],
            }
        )
    return {"rows": rows}


def budget_curve(tasks, library: Library, max_steps: int, budgets) -> list[dict]:
    rows = []
    for budget in budgets:
        result = evaluate(library, max_steps, tasks, budget=budget)
        rows.append(
            {
                "budget": budget,
                "accuracy": result["accuracy"],
                "correct": result["correct"],
            }
        )
    return rows


def run(seed: int = 0, n_train: int = 60, sweep_limit: int | None = None) -> dict:
    tasks = make_depth3_grid(seed)
    learned, training = train(seed, n_train)
    rng = random.Random(seed)
    draw = rng.sample(list(PAIRS), 3)
    random_lib = Library([Macro(_name(b), b) for b in draw])

    libraries = {
        "A0-nolearn-d2": (Library([]), 2),
        "A1-nolearn-d3": (Library([]), 3),
        "A2-random-same-lang-d2": (random_lib, 2),
        "A3-learned-d2": (learned, 2),
        "A4-learned-d3": (learned, 3),
    }
    conditions = []
    for name, (library, max_steps) in libraries.items():
        result = evaluate(library, max_steps, tasks)
        conditions.append(
            {
                "condition": name,
                "max_steps": max_steps,
                "library_size": library.size(),
                "macros": [list(m.body) for m in library.macros],
                **result,
            }
        )

    return {
        "seed": seed,
        "n_train": n_train,
        "n_tasks": len(tasks),
        "learned_macros": [list(m.body) for m in learned.macros],
        "random_macros": [list(b) for b in draw],
        "training": training,
        "conditions": conditions,
        "sweep_grid": sweep(seed, tasks, limit=sweep_limit),
        # The audit's 250/560 came from the three hand-picked programs; reproduced
        # here so the two baselines can be compared on identical code.
        "sweep_selected_d3": sweep(
            seed, make_splits(seed=seed, n_train=1, n_eval=30)["D3"], limit=sweep_limit
        ),
        "acquisition": acquisition(seed, tasks),
        "budget": {
            "A1-nolearn-d3": budget_curve(tasks, Library([]), 3, (20, 40, 60, 80, 84)),
            "A3-learned-d2": budget_curve(tasks, learned, 2, (20, 40, 60, 80, 84)),
        },
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--train", type=int, default=60)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run(seed=args.seed, n_train=args.train)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"seed={result['seed']} train={result['n_train']} tasks={result['n_tasks']}")
    print(f"learned={result['learned_macros']}")
    print(f"{'condition':<26} {'acc':>6} {'corr':>5} {'cand':>6} {'ops':>7}")
    for row in result["conditions"]:
        print(
            f"{row['condition']:<26} {row['accuracy']:>6.3f} {row['correct']:>5} "
            f"{row['cost']['candidates']:>6} {row['cost']['primitive_ops']:>7}"
        )
    sw = result["sweep_grid"]
    print(
        f"sweep grid: {sw['n_libraries']} libraries, mean={sw['mean_accuracy']} "
        f"median={sw['median_accuracy']} max={sw['max_accuracy']} "
        f"perfect={sw['perfect']} zero={sw['zero']}"
    )
    s3 = result["sweep_selected_d3"]
    print(
        f"sweep 3-program D3: mean={s3['mean_accuracy']} "
        f"perfect={s3['perfect']}/{s3['n_libraries']}"
    )
    print(
        "acquisition: "
        + ", ".join(
            f"n={r['n_train']}:{r['accuracy']}" for r in result["acquisition"]["rows"]
        )
    )


if __name__ == "__main__":
    main()
