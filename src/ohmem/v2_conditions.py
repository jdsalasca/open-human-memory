"""Prototype 002 conditions: infer rules from examples, never from labels."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .v2_tasks import (
    Observation,
    Solution,
    Task,
    apply_primitive,
    apply_rule,
    PRIMITIVES,
)


@dataclass
class Prediction:
    rule: tuple[str, ...]
    memory_reads: int
    verification_calls: int = 0
    context_values: int = 0


def _matches(rule: tuple[str, ...], obs: Observation) -> bool:
    return all(
        apply_rule(rule, x) == y
        for x, y in zip(obs.support_inputs, obs.support_outputs)
    )


def infer_primitive(obs: Observation) -> tuple[str, ...]:
    for primitive in PRIMITIVES:
        if _matches((primitive,), obs):
            return (primitive,)
    return ("sort_asc",)


def infer_composition(obs: Observation) -> tuple[str, ...]:
    # Prefer the shortest rule that explains all support examples.
    candidates = [(p,) for p in PRIMITIVES] + [
        (a, b) for a in PRIMITIVES for b in PRIMITIVES
    ]
    valid = [rule for rule in candidates if _matches(rule, obs)]
    return min(valid, key=len) if valid else ("sort_asc",)


def jaccard(a: tuple[str, ...], b: tuple[str, ...]) -> float:
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb) if sa or sb else 0.0


class CurrentSolver:
    name = "A0-current-solver"

    def predict(self, obs: Observation) -> Prediction:
        return Prediction(infer_composition(obs), 0, 20, 12)


class NoMemory:
    name = "A-no-memory"

    def predict(self, obs: Observation) -> Prediction:
        return Prediction(("sort_asc",), 0, 0, 0)


class Retrieval:
    name = "B-retrieval"

    def __init__(self, train: list[Task]) -> None:
        self.items = [(task.observation, task.solution.rule) for task in train]

    def predict(self, obs: Observation) -> Prediction:
        if not self.items:
            return Prediction(("sort_asc",), 0, 0, 0)
        _, rule = max(
            self.items, key=lambda item: jaccard(obs.surface, item[0].surface)
        )
        return Prediction(rule, 1, 0, 24)


class Oracle:
    name = "C-oracle"

    def predict(self, obs: Observation, solution: Solution) -> Prediction:
        return Prediction(solution.rule, 1, 1, 12)


class Procedure:
    name = "D-primitive-procedure"

    def predict(self, obs: Observation) -> Prediction:
        return Prediction(infer_primitive(obs), 0, 4, 12)


class Abstraction:
    name = "E-compositional-abstraction"

    def predict(self, obs: Observation) -> Prediction:
        return Prediction(infer_composition(obs), 0, 20, 12)


@dataclass
class Conditions:
    no_memory: NoMemory
    retrieval: Retrieval
    oracle: Oracle
    procedure: Procedure
    abstraction: Abstraction
