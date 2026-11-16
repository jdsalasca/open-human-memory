"""Prototype 006-A': activation policy, corrected after the direction audit.

Corrections over the frozen 006-A:

1. The applicability probe counts primitive applications actually executed
   (short-circuit inside each check), not an upper bound.
2. `uniform-random` and `shuffled-policy` replace the misnamed `random-action`.
   The second keeps the learned policy's action frequencies but ignores the task.
3. Every condition starts from a fresh evaluation state.
4. The hand-written probe rule passes `macro_first=True`, like the action it picks.
5. The mixed set interleaves similar and novel tasks instead of concatenating them.
6. Every condition returns per-task outcomes, so results are compared paired.

The design otherwise stays as frozen: library learned from family A and frozen,
two actions (library-first vs search), 120 executed steps of budget.
"""

from __future__ import annotations

from collections import Counter, deque
import random

from .v3_library import Library
from .v3_solver import solve
from .v3_tasks import (
    DEPTH3_GRID,
    PRIMITIVES,
    TRAIN_PROGRAMS,
    apply_program,
    make_task,
)
from .v4_experiment import train

ACTIONS = ("memory_first", "search")
FIXED_ACTIONS = ("memory", "memory_first", "search")
BUDGET_STEPS = 120
CAP = 4
TRAIN_FAMILY = TRAIN_PROGRAMS
NO_MEMORY = Library([])


def _fits_cost(obs, body: tuple[str, ...]) -> tuple[bool, int]:
    steps = 0
    for x, y in zip(obs.support_inputs, obs.support_outputs):
        steps += len(body)
        if apply_program(body, x) != y:
            return False, steps
    return True, steps


def probe(obs, library: Library) -> tuple[float, int]:
    """(does any macro fit as prefix or suffix, primitive applications executed)."""
    steps = 0
    for macro in library.macros:
        for primitive in PRIMITIVES:
            for body in (macro.body + (primitive,), (primitive,) + macro.body):
                ok, cost = _fits_cost(obs, body)
                steps += cost
                if ok:
                    return 1.0, steps
    return 0.0, steps


def macro_any_fit(obs, library: Library) -> float:
    return probe(obs, library)[0]


def reward(correct: bool, solved: bool, steps: int, probe_steps: int = 0) -> float:
    if correct:
        return 1.0 - 0.3 * (steps + probe_steps) / BUDGET_STEPS
    return -0.5 if solved else -0.2


class Policy:
    def __init__(
        self,
        use_applicability: bool = True,
        lr: float = 0.1,
        epsilon: float = 0.15,
        seed: int = 0,
    ):
        self.use_applicability = use_applicability
        self.lr = lr
        self.epsilon = epsilon
        self.weights = {action: [0.0, 0.0, 0.0] for action in ACTIONS}
        self.rng = random.Random(seed)
        self.baseline = 0.0
        self.n_updates = 0

    def vector(self, probe_value: float, recent_success: float) -> tuple[float, ...]:
        feature = 2.0 * probe_value - 1.0
        if not self.use_applicability:
            feature = 0.0
        return (1.0, feature, recent_success)

    def scores(self, vector) -> dict[str, float]:
        return {
            action: sum(w * f for w, f in zip(self.weights[action], vector))
            for action in ACTIONS
        }

    def choose(self, vector, explore: bool = True) -> str:
        if explore and self.rng.random() < self.epsilon:
            return self.rng.choice(ACTIONS)
        scores = self.scores(vector)
        return max(ACTIONS, key=lambda action: scores[action])

    def update(self, vector, action: str, value: float) -> None:
        self.n_updates += 1
        self.baseline += (value - self.baseline) / self.n_updates
        delta = value - self.baseline
        for i, f in enumerate(vector):
            self.weights[action][i] += self.lr * delta * f


def build_library(seed: int, n: int = 60) -> Library:
    library, _ = train(seed, n)
    return Library(library.macros[:CAP])


def similar_tasks(seed: int, n: int = 24):
    return [
        make_task(
            seed + 100,
            "delta",
            10_000 + i,
            TRAIN_FAMILY[i % len(TRAIN_FAMILY)]
            + (PRIMITIVES[(i // len(TRAIN_FAMILY)) % len(PRIMITIVES)],),
            "similar",
        )
        for i in range(n)
    ]


def novel_tasks(seed: int, library: Library, n: int = 24):
    pairs = {macro.body for macro in library.macros}
    rng = random.Random(f"novel:{seed}")
    pool = [
        program
        for program in DEPTH3_GRID
        if not any(tuple(program[i : i + 2]) in pairs for i in range(len(program) - 1))
    ]
    rng.shuffle(pool)
    return [
        make_task(seed + 200, "delta", 20_000 + i, program, "novel")
        for i, program in enumerate(pool[:n])
    ]


class Agent:
    def __init__(self, policy: Policy, library: Library):
        self.policy = policy
        self.library = library
        self.recent: deque = deque(maxlen=8)

    def reset(self) -> None:
        self.recent.clear()

    def recent_success(self) -> float:
        return sum(self.recent) / len(self.recent) if self.recent else 0.5

    def run_action(self, task, action: str):
        return solve(
            task.observation,
            NO_MEMORY if action == "search" else self.library,
            3 if action == "search" else 2,
            budget_steps=BUDGET_STEPS,
            macro_first=action == "memory_first",
        )

    def step(self, task, explore: bool = True, learn: bool = True) -> dict:
        probe_value, probe_steps = probe(task.observation, self.library)
        vector = self.policy.vector(probe_value, self.recent_success())
        action = self.policy.choose(vector, explore=explore)
        result = self.run_action(task, action)
        correct = result.program is not None and apply_program(
            result.program, task.observation.query
        ) == apply_program(task.solution.program, task.observation.query)
        value = reward(
            correct, result.program is not None, result.executed_steps, probe_steps
        )
        if learn:
            self.policy.update(vector, action, value)
        if action != "search":
            self.recent.append(1.0 if correct else 0.0)
        return {
            "action": action,
            "correct": correct,
            "steps": result.executed_steps,
            "probe_steps": probe_steps,
            "reward": value,
        }


def training_stream(seed: int, library: Library, per_set: int = 16):
    tasks = similar_tasks(seed, per_set) + novel_tasks(seed, library, per_set)
    order = list(range(len(tasks)))
    random.Random(f"order:{seed}").shuffle(order)
    return [tasks[i] for i in order]


def _run_fixed(task, library: Library, action: str):
    result = solve(
        task.observation,
        NO_MEMORY if action == "search" else library,
        3 if action == "search" else 2,
        budget_steps=BUDGET_STEPS,
        macro_first=action == "memory_first",
    )
    correct = result.program is not None and apply_program(
        result.program, task.observation.query
    ) == apply_program(task.solution.program, task.observation.query)
    return correct, result.executed_steps


def evaluate_fixed(tasks, library: Library, action: str) -> dict:
    flags = []
    steps = 0
    for task in tasks:
        correct, executed = _run_fixed(task, library, action)
        flags.append(correct)
        steps += executed
    return {
        "accuracy": round(sum(flags) / len(flags), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "mean_probe_steps": 0.0,
        "correct_flags": flags,
    }


def evaluate_policy(tasks, agent: Agent, explore: bool = False) -> dict:
    agent.reset()
    flags = []
    steps = 0
    probe_steps = 0
    decisions: Counter = Counter()
    for task in tasks:
        outcome = agent.step(task, explore=explore, learn=False)
        decisions[outcome["action"]] += 1
        flags.append(outcome["correct"])
        steps += outcome["steps"]
        probe_steps += outcome["probe_steps"]
    return {
        "accuracy": round(sum(flags) / len(flags), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "mean_probe_steps": round(probe_steps / len(tasks), 1),
        "total_steps": round((steps + probe_steps) / len(tasks), 1),
        "decisions": dict(decisions),
        "correct_flags": flags,
    }


def evaluate_uniform(tasks, agent: Agent, seed: int = 0) -> dict:
    rng = random.Random(f"uniform:{seed}")
    flags = []
    steps = 0
    decisions: Counter = Counter()
    for task in tasks:
        action = rng.choice(ACTIONS)
        decisions[action] += 1
        correct, executed = _run_fixed(task, agent.library, action)
        flags.append(correct)
        steps += executed
    return {
        "accuracy": round(sum(flags) / len(flags), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "mean_probe_steps": 0.0,
        "decisions": dict(decisions),
        "correct_flags": flags,
    }


def evaluate_shuffled(tasks, agent: Agent, seed: int = 0) -> dict:
    """Same action frequencies as the learned policy, assigned without looking at the task."""
    agent.reset()
    chosen = []
    for task in tasks:
        probe_value, _ = probe(task.observation, agent.library)
        vector = agent.policy.vector(probe_value, agent.recent_success())
        chosen.append(agent.policy.choose(vector, explore=False))
    random.Random(f"shuffled:{seed}").shuffle(chosen)
    flags = []
    steps = 0
    decisions: Counter = Counter()
    for task, action in zip(tasks, chosen):
        decisions[action] += 1
        correct, executed = _run_fixed(task, agent.library, action)
        flags.append(correct)
        steps += executed
    return {
        "accuracy": round(sum(flags) / len(flags), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "mean_probe_steps": 0.0,
        "decisions": dict(decisions),
        "correct_flags": flags,
    }


def evaluate_probe_rule(tasks, library: Library) -> dict:
    flags = []
    steps = 0
    probe_steps = 0
    decisions: Counter = Counter()
    for task in tasks:
        value, cost = probe(task.observation, library)
        probe_steps += cost
        action = "memory_first" if value >= 0.5 else "search"
        decisions[action] += 1
        correct, executed = _run_fixed(task, library, action)
        flags.append(correct)
        steps += executed
    return {
        "accuracy": round(sum(flags) / len(flags), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "mean_probe_steps": round(probe_steps / len(tasks), 1),
        "total_steps": round((steps + probe_steps) / len(tasks), 1),
        "decisions": dict(decisions),
        "correct_flags": flags,
    }


def evaluate_oracle(tasks, library: Library) -> dict:
    flags = []
    steps = 0
    for task in tasks:
        best = None
        for action in FIXED_ACTIONS:
            correct, executed = _run_fixed(task, library, action)
            value = reward(correct, True, executed)
            if best is None or value > best[0]:
                best = (value, correct, executed)
        flags.append(best[1])
        steps += best[2]
    return {
        "accuracy": round(sum(flags) / len(flags), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "mean_probe_steps": 0.0,
        "correct_flags": flags,
    }


def run(seed: int = 0) -> dict:
    library = build_library(seed)
    similar = similar_tasks(seed)
    novel = novel_tasks(seed, library)
    mixed = [task for pair in zip(similar, novel) for task in pair]
    sets = {"similar": similar, "novel": novel, "mixed": mixed}
    out = {
        "seed": seed,
        "budget_steps": BUDGET_STEPS,
        "cap": CAP,
        "library": [list(m.body) for m in library.macros],
        "policies": {},
    }
    for label, flag in (("policy-applicability", True), ("policy-blind", False)):
        policy = Policy(use_applicability=flag, seed=seed)
        agent = Agent(policy, library)
        for epoch in range(20):
            policy.epsilon = (
                1.0 if epoch == 0 else max(0.03, 0.5 * (0.8 ** (epoch - 1)))
            )
            for task in training_stream(seed, library):
                agent.step(task, explore=True)
        block = {
            "weights": {a: [round(v, 4) for v in w] for a, w in policy.weights.items()},
            "conditions": {},
        }
        for name, tasks in sets.items():
            rows = {
                action: evaluate_fixed(tasks, library, action)
                for action in FIXED_ACTIONS
            }
            rows["uniform-random"] = evaluate_uniform(tasks, agent, seed)
            rows["shuffled-policy"] = evaluate_shuffled(tasks, agent, seed)
            rows["learned-policy"] = evaluate_policy(tasks, agent, explore=False)
            rows["probe-rule"] = evaluate_probe_rule(tasks, library)
            rows["oracle"] = evaluate_oracle(tasks, library)
            block["conditions"][name] = rows
        out["policies"][label] = block
    return out


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
    print("library:", result["library"])
    for label, block in result["policies"].items():
        print(f"== {label}")
        for set_name, rows in block["conditions"].items():
            print(f"-- {set_name}")
            for name, row in rows.items():
                print(
                    f"   {name:<16} acc={row['accuracy']:.3f} "
                    f"search={row['mean_steps']:.1f} "
                    f"probe={row['mean_probe_steps']:.1f} "
                    f"total={row.get('total_steps', row['mean_steps']):.1f} "
                    f"{row.get('decisions', '')}"
                )


if __name__ == "__main__":
    main()
