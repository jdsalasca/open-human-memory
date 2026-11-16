"""Prototype 005: memory under a compute budget, with drift and continuity.

The audit of 004-A left three questions this module answers:

1. How much of the "64 programs" grid is really 64 *behaviours*?
2. When does a learned library pay for itself as a function of how much the
   future resembles the past (continuity)?
3. Does an agent that learns *online* and keeps a bounded, utility-evicted
   library beat one that learns once and freezes?

Every cost here is `executed_steps`: primitive applications actually run before
the first counterexample stops the check. The 004-A upper bound is kept separate.
"""

from __future__ import annotations

from collections import Counter
import random

from .v3_library import Library, Macro, _name, same_language_libraries
from .v3_solver import solve
from .v3_tasks import (
    D2_PROGRAMS,
    DEPTH3_GRID,
    PRIMITIVES,
    TRAIN_PROGRAMS,
    apply_program,
    make_depth3_grid,
    make_task,
)
from .v4_experiment import train

PROBES = tuple(
    tuple(random.Random(f"probe:{i}").randint(1, 9) for _ in range(4))
    for i in range(40)
)
BUDGET_STEPS = 120
TASKS_PER_PHASE = 24

STREAM_PHASES = (
    ("P1", TRAIN_PROGRAMS),
    ("P2", D2_PROGRAMS),
    ("P3", TRAIN_PROGRAMS),
    ("P4", (("sort_asc", "add_one"), ("sort_desc", "add_one"), ("double", "double"))),
)


def behavior(program: tuple[str, ...]) -> tuple:
    return tuple(apply_program(program, probe) for probe in PROBES)


def behavioral_classes() -> tuple[list[tuple[str, ...]], int]:
    seen = set()
    reps = []
    for program in DEPTH3_GRID:
        signature = behavior(program)
        if signature not in seen:
            seen.add(signature)
            reps.append(program)
    return reps, len(seen)


def contains_motif(program: tuple[str, ...], motifs) -> bool:
    return any(tuple(program[i : i + 2]) in motifs for i in range(len(program) - 1))


def continuity_tasks(seed: int, level: float, n: int = 16, motifs=TRAIN_PROGRAMS):
    rng = random.Random(f"continuity:{seed}:{level}")
    with_m = [p for p in DEPTH3_GRID if contains_motif(p, motifs)]
    without = [p for p in DEPTH3_GRID if not contains_motif(p, motifs)]
    k = round(level * n)
    chosen = rng.sample(with_m, min(k, len(with_m)))
    chosen += rng.sample(without, min(n - k, len(without)))
    rng.shuffle(chosen)
    actual = sum(1 for p in chosen if contains_motif(p, motifs)) / len(chosen)
    tasks = [
        make_task(seed, "delta", 1000 + i, program, f"c{int(level * 100)}")
        for i, program in enumerate(chosen)
    ]
    return tasks, round(actual, 3)


def evaluate(
    tasks, library: Library, max_steps: int, budget_steps=None, macro_first=False
) -> dict:
    correct = 0
    executed = 0
    candidates = 0
    macro_tasks = 0
    for task in tasks:
        result = solve(
            task.observation,
            library,
            max_steps,
            budget_steps=budget_steps,
            macro_first=macro_first,
        )
        executed += result.executed_steps
        candidates += result.candidates
        if result.program is None:
            continue
        if result.macros:
            macro_tasks += 1
        if apply_program(result.program, task.observation.query) == apply_program(
            task.solution.program, task.observation.query
        ):
            correct += 1
    return {
        "accuracy": round(correct / len(tasks), 4),
        "correct": correct,
        "n": len(tasks),
        "executed_steps": executed,
        "candidates": candidates,
        "macro_tasks": macro_tasks,
        "library_size": library.size(),
    }


def continuity_sweep(
    seed: int, levels=(0.0, 0.25, 0.5, 0.75, 1.0), draws: int = 5
) -> list:
    learned, _ = train(seed, 60)
    conditions = (
        ("no-memory-d3-budget", Library([]), 3, False),
        ("learned-d2-budget", learned, 2, False),
        ("learned-d2-macrofirst-budget", learned, 2, True),
        ("no-memory-d3-uncapped", Library([]), 3, False),
        ("learned-d2-uncapped", learned, 2, False),
    )
    rows = []
    for level in levels:
        for name, library, max_steps, first in conditions:
            capped = name.endswith("budget")
            correct = 0
            executed = 0
            total = 0
            actual_levels = []
            for draw in range(draws):
                tasks, actual = continuity_tasks(seed + draw, level)
                actual_levels.append(actual)
                result = evaluate(
                    tasks,
                    library,
                    max_steps,
                    budget_steps=BUDGET_STEPS if capped else None,
                    macro_first=first,
                )
                correct += result["correct"]
                executed += result["executed_steps"]
                total += result["n"]
            rows.append(
                {
                    "level": level,
                    "actual_level": round(sum(actual_levels) / len(actual_levels), 3),
                    "condition": name,
                    "accuracy": round(correct / total, 4),
                    "mean_executed_steps": round(executed / total, 1),
                }
            )
    return rows


def oracle_gap(seed: int) -> dict:
    tasks = make_depth3_grid(seed)
    dev, test = tasks[0::2], tasks[1::2]
    scored = [
        (evaluate(dev, library, 2)["accuracy"], library)
        for library in same_language_libraries(3)
    ]
    scored.sort(key=lambda item: -item[0])
    top = scored[:5]
    learned, _ = train(seed, 60)
    return {
        "n_libraries": len(scored),
        "best_dev_accuracy": top[0][0],
        "test_mean_of_top5": round(
            sum(evaluate(test, lib, 2)["accuracy"] for _, lib in top) / len(top), 4
        ),
        "test_learned": evaluate(test, learned, 2)["accuracy"],
        "test_random_same_lang": round(
            sum(evaluate(test, lib, 2)["accuracy"] for _, lib in scored[-5:]) / 5, 4
        ),
    }


class Agent:
    """Bounded library: learns on frequency, keeps what it uses, evicts the rest."""

    def __init__(
        self, learn: bool = True, cap: int | None = None, macro_first: bool = False
    ):
        self.learn = learn
        self.cap = cap
        self.macro_first = macro_first
        self.macros: list[Macro] = []
        self.counts: Counter = Counter()
        self.uses: Counter = Counter()
        self.t = 0

    @property
    def library(self) -> Library:
        return Library(list(self.macros))

    def _add(self, body: tuple[str, ...]) -> None:
        if any(macro.body == body for macro in self.macros):
            return
        if self.cap is not None and len(self.macros) >= self.cap:
            victim = min(
                self.macros, key=lambda m: (self.uses[m.name], self.macros.index(m))
            )
            self.macros.remove(victim)
        self.macros.append(Macro(_name(body), body))

    def step(self, task, max_steps: int, budget_steps: int):
        result = solve(
            task.observation,
            self.library,
            max_steps,
            budget_steps=budget_steps,
            macro_first=self.macro_first,
        )
        correct = result.program is not None and apply_program(
            result.program, task.observation.query
        ) == apply_program(task.solution.program, task.observation.query)
        for name in result.macros:
            self.uses[name] += 1
        if self.learn and result.program is not None:
            for i in range(len(result.program) - 1):
                pair = (result.program[i], result.program[i + 1])
                self.counts[pair] += 1
                if self.counts[pair] >= 2:
                    self._add(pair)
        self.t += 1
        return correct, result.executed_steps


def stream_tasks(seed: int):
    phases = []
    for pi, (name, motifs) in enumerate(STREAM_PHASES):
        tasks = []
        for i in range(TASKS_PER_PHASE):
            if i % 3 == 0:
                program = DEPTH3_GRID[(pi * 7 + i * 5) % len(DEPTH3_GRID)]
            else:
                motif = motifs[i % len(motifs)]
                program = (motif[0], motif[1], PRIMITIVES[(i // len(motifs)) % 4])
            tasks.append(make_task(seed, "delta", pi * 100 + i, program, f"stream{pi}"))
        phases.append((name, tasks))
    return phases


def tasks_to_competence(
    correctness: list[bool], window: int = 8, target: float = 0.875
):
    for i in range(len(correctness) - window + 1):
        if sum(correctness[i : i + window]) / window >= target:
            return i + window
    return None


def run_stream(seed: int, budget_steps: int = BUDGET_STEPS) -> dict:
    policies = (
        ("NOLEARN", {"learn": False, "cap": 0}, 3),
        ("FROZEN", {"learn": True, "cap": None}, 2),
        ("ONLINE", {"learn": True, "cap": None}, 2),
        ("GATED", {"learn": True, "cap": 5, "macro_first": True}, 2),
    )
    phases = stream_tasks(seed)
    rows = []
    for name, kwargs, max_steps in policies:
        agent = Agent(**kwargs)
        correctness: list[bool] = []
        per_phase = []
        for index, (phase, tasks) in enumerate(phases):
            if name == "FROZEN" and index == 1:
                agent.learn = False
            correct = 0
            executed = 0
            for task in tasks:
                ok, steps = agent.step(task, max_steps, budget_steps)
                correctness.append(ok)
                correct += ok
                executed += steps
            per_phase.append(
                {
                    "phase": phase,
                    "accuracy": round(correct / len(tasks), 4),
                    "mean_executed_steps": round(executed / len(tasks), 1),
                    "library_size": agent.library.size(),
                }
            )
        rows.append(
            {
                "policy": name,
                "max_steps": max_steps,
                "per_phase": per_phase,
                "total_executed_steps": sum(
                    p["mean_executed_steps"] * TASKS_PER_PHASE for p in per_phase
                ),
                "overall_accuracy": round(sum(correctness) / len(correctness), 4),
                "tasks_to_competence": tasks_to_competence(correctness),
                "final_library": [list(m.body) for m in agent.macros],
            }
        )
    return {
        "budget_steps": budget_steps,
        "phases": [p for p, _ in phases],
        "policies": rows,
    }


def run(seed: int = 0) -> dict:
    reps, n_classes = behavioral_classes()
    learned, _ = train(seed, 60)
    rep_tasks = [
        make_task(seed, "delta", 2000 + i, program, "rep")
        for i, program in enumerate(reps)
    ]
    return {
        "seed": seed,
        "budget_steps": BUDGET_STEPS,
        "coverage": {
            "syntactic": len(DEPTH3_GRID),
            "behavioral": n_classes,
            "learned_d2_on_representatives": evaluate(rep_tasks, learned, 2)[
                "accuracy"
            ],
            "no_memory_d3_on_representatives": evaluate(rep_tasks, Library([]), 3)[
                "accuracy"
            ],
        },
        "continuity": continuity_sweep(seed),
        "oracle": oracle_gap(seed),
        "stream": run_stream(seed),
    }


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run(args.seed)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    cov = result["coverage"]
    print(f"syntactic={cov['syntactic']} behavioral={cov['behavioral']}")
    print(
        f"coverage on behaviours: learned-d2={cov['learned_d2_on_representatives']} "
        f"no-memory-d3={cov['no_memory_d3_on_representatives']}"
    )
    print(f"{'level':>5} {'cond':<32} {'acc':>6} {'steps':>7}")
    for row in result["continuity"]:
        print(
            f"{row['actual_level']:>5} {row['condition']:<32} "
            f"{row['accuracy']:>6.3f} {row['mean_executed_steps']:>7.1f}"
        )
    print("oracle:", result["oracle"])
    print(f"stream budget={result['stream']['budget_steps']}")
    for row in result["stream"]["policies"]:
        accs = " ".join(f"{p['accuracy']:.2f}" for p in row["per_phase"])
        print(
            f"{row['policy']:<8} acc={accs} overall={row['overall_accuracy']:.3f} "
            f"steps={row['total_executed_steps']:.0f} "
            f"competence@{row['tasks_to_competence']} lib={row['per_phase'][-1]['library_size']}"
        )


if __name__ == "__main__":
    main()
