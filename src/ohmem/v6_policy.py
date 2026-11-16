"""Prototype 006: a policy that decides when to trust a frozen library.

Design (fixed after the first attempt degenerated, see README):

1. A small library is learned once from family A (frequency >= 2, cap 4) and
   frozen. Learning *what* to keep and *when* to use it are separate problems.
2. The policy is trained on a mixed stream: tasks from family A (the library
   applies) and tasks from families the library has never seen (it does not).
3. The policy scores three actions from three features: bias, a cheap
   applicability probe, and recent memory success.

The probe is the signal; the policy is what has to learn its sign and weight. A
second policy is trained with the probe forced to zero. If the blind policy
matches the probe one, the signal was doing nothing and the claim collapses.
"""

from __future__ import annotations

from collections import Counter, deque
import random

from .v3_library import Library, Macro, _name, learn_macros
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


def _fits(obs, body: tuple[str, ...]) -> bool:
    return all(
        apply_program(body, x) == y
        for x, y in zip(obs.support_inputs, obs.support_outputs)
    )


def macro_applicability(obs, library: Library) -> float:
    """Fraction of macros that fit as the first or last two steps of a depth-3 task."""
    if not library.macros:
        return 0.0
    hits = 0
    for macro in library.macros:
        if any(
            _fits(obs, macro.body + (primitive,))
            or _fits(obs, (primitive,) + macro.body)
            for primitive in PRIMITIVES
        ):
            hits += 1
    return hits / len(library.macros)


def macro_any_fit(obs, library: Library) -> float:
    """1.0 if any macro fits as the first or last two steps of a depth-3 task."""
    if not library.macros:
        return 0.0
    for macro in library.macros:
        if any(
            _fits(obs, macro.body + (primitive,))
            or _fits(obs, (primitive,) + macro.body)
            for primitive in PRIMITIVES
        ):
            return 1.0
    return 0.0


def features(obs, library: Library, recent_success: float) -> tuple[float, ...]:
    # Centred probe: -1 when no macro fits, +1 when one does. Without centring the
    # bias and the weight cancel and the learner never separates the two regimes.
    return (1.0, 2.0 * macro_any_fit(obs, library) - 1.0, recent_success)


def reward(correct: bool, solved: bool, steps: int) -> float:
    if correct:
        return 1.0 - 0.3 * steps / BUDGET_STEPS
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

    def vector(self, obs, library: Library, recent_success: float) -> tuple[float, ...]:
        raw = list(features(obs, library, recent_success))
        if not self.use_applicability:
            raw[1] = 0.0
        return tuple(raw)

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
    """Learned from depth-2 tasks in family A, then frozen."""
    library, _ = train(seed, n)
    return Library(library.macros[:CAP])


def seen_pairs(library: Library) -> set[tuple[str, ...]]:
    return {macro.body for macro in library.macros}


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
    pairs = seen_pairs(library)
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
        vector = self.policy.vector(
            task.observation, self.library, self.recent_success()
        )
        action = self.policy.choose(vector, explore=explore)
        result = self.run_action(task, action)
        correct = result.program is not None and apply_program(
            result.program, task.observation.query
        ) == apply_program(task.solution.program, task.observation.query)
        value = reward(correct, result.program is not None, result.executed_steps)
        if learn:
            self.policy.update(vector, action, value)
        if action != "search":
            self.recent.append(1.0 if correct else 0.0)
        return {
            "action": action,
            "correct": correct,
            "steps": result.executed_steps,
            "reward": value,
        }


def training_stream(seed: int, library: Library, per_set: int = 16):
    tasks = similar_tasks(seed, per_set) + novel_tasks(seed, library, per_set)
    order = list(range(len(tasks)))
    random.Random(f"order:{seed}").shuffle(order)
    return [tasks[i] for i in order]


def evaluate_action(tasks, library: Library, action: str) -> dict:
    correct = 0
    steps = 0
    solved = 0
    for task in tasks:
        result = solve(
            task.observation,
            NO_MEMORY if action == "search" else library,
            3 if action == "search" else 2,
            budget_steps=BUDGET_STEPS,
            macro_first=action == "memory_first",
        )
        steps += result.executed_steps
        if result.program is not None:
            solved += 1
            if apply_program(result.program, task.observation.query) == apply_program(
                task.solution.program, task.observation.query
            ):
                correct += 1
    return {
        "accuracy": round(correct / len(tasks), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "solved_rate": round(solved / len(tasks), 4),
    }


def evaluate_agent(tasks, agent: Agent, explore: bool = False) -> dict:
    correct = 0
    steps = 0
    rewarded = 0.0
    decisions: Counter = Counter()
    for task in tasks:
        outcome = agent.step(task, explore=explore, learn=False)
        decisions[outcome["action"]] += 1
        correct += outcome["correct"]
        steps += outcome["steps"]
        rewarded += outcome["reward"]
    return {
        "accuracy": round(correct / len(tasks), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "mean_reward": round(rewarded / len(tasks), 4),
        "decisions": dict(decisions),
    }


def evaluate_probe_rule(tasks, library: Library) -> dict:
    """Hand-coded version of the target rule: probe says yes -> memory, else search."""
    correct = 0
    steps = 0
    decisions: Counter = Counter()
    for task in tasks:
        action = (
            "memory_first"
            if macro_any_fit(task.observation, library) >= 0.5
            else "search"
        )
        decisions[action] += 1
        result = solve(
            task.observation,
            NO_MEMORY if action == "search" else library,
            3 if action == "search" else 2,
            budget_steps=BUDGET_STEPS,
        )
        steps += result.executed_steps
        if result.program is not None and apply_program(
            result.program, task.observation.query
        ) == apply_program(task.solution.program, task.observation.query):
            correct += 1
    return {
        "accuracy": round(correct / len(tasks), 4),
        "mean_steps": round(steps / len(tasks), 1),
        "decisions": dict(decisions),
    }


def evaluate_oracle(tasks, library: Library) -> dict:
    total = 0.0
    correct = 0
    steps = 0
    for task in tasks:
        best = None
        for action in ACTIONS:
            result = solve(
                task.observation,
                NO_MEMORY if action == "search" else library,
                3 if action == "search" else 2,
                budget_steps=BUDGET_STEPS,
                macro_first=action == "memory_first",
            )
            ok = result.program is not None and apply_program(
                result.program, task.observation.query
            ) == apply_program(task.solution.program, task.observation.query)
            value = reward(ok, result.program is not None, result.executed_steps)
            if best is None or value > best[0]:
                best = (value, ok, result.executed_steps)
        total += best[0]
        correct += best[1]
        steps += best[2]
    return {
        "mean_reward": round(total / len(tasks), 4),
        "accuracy": round(correct / len(tasks), 4),
        "mean_steps": round(steps / len(tasks), 1),
    }


def run(seed: int = 0) -> dict:
    library = build_library(seed)
    similar = similar_tasks(seed)
    novel = novel_tasks(seed, library)
    sets = {"similar": similar, "novel": novel, "mixed": similar + novel}
    out = {
        "seed": seed,
        "budget_steps": BUDGET_STEPS,
        "cap": CAP,
        "library": [list(m.body) for m in library.macros],
        "probe": {
            name: round(
                sum(macro_applicability(task.observation, library) for task in tasks)
                / len(tasks),
                3,
            )
            for name, tasks in sets.items()
        },
        "policies": {},
    }
    for label, flag in (("policy-applicability", True), ("policy-blind", False)):
        policy = Policy(use_applicability=flag, seed=seed)
        agent = Agent(policy, library)
        stream = training_stream(seed, library)
        for epoch in range(20):
            policy.epsilon = (
                1.0 if epoch == 0 else max(0.03, 0.5 * (0.8 ** (epoch - 1)))
            )
            for task in stream:
                agent.step(task, explore=True)
        block = {
            "weights": {a: [round(v, 4) for v in w] for a, w in policy.weights.items()},
            "conditions": {},
        }
        for name, tasks in sets.items():
            agent.recent.clear()
            rows = {
                action: evaluate_action(tasks, library, action)
                for action in FIXED_ACTIONS
            }
            rows["random-action"] = evaluate_agent(tasks, agent, explore=True)
            agent.recent.clear()
            rows["learned-policy"] = evaluate_agent(tasks, agent, explore=False)
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
    print("probe applicability:", result["probe"])
    for label, block in result["policies"].items():
        print(f"== {label}  weights={block['weights']}")
        for set_name, rows in block["conditions"].items():
            print(f"-- {set_name}")
            for name, row in rows.items():
                print(
                    f"   {name:<16} acc={row['accuracy']:.3f} "
                    f"steps={row['mean_steps']:.1f} "
                    f"reward={row.get('mean_reward', '-')} "
                    f"decisions={row.get('decisions', {})}"
                )


if __name__ == "__main__":
    main()
