"""Experimental conditions A-E for the diagnostic."""

from __future__ import annotations

from dataclasses import dataclass

from .memory import AbstractionLearner, Memory, ProcedureLearner
from .tasks import Task


@dataclass
class Prediction:
    rule: str
    memory_reads: int


class NoMemory:
    name = "A-no-memory"

    def predict(self, task: Task) -> Prediction:
        return Prediction("sort_asc", 0)


class Retrieval:
    name = "B-retrieval"

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def predict(self, task: Task) -> Prediction:
        item = self.memory.retrieve(task)
        return Prediction(item.rule if item else "sort_asc", 1)


class Oracle:
    name = "C-oracle"

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def predict(self, task: Task) -> Prediction:
        item = self.memory.oracle(task)
        return Prediction(item.rule if item else "sort_asc", 1)


class Procedure:
    name = "D-procedure"

    def __init__(self, learner: ProcedureLearner) -> None:
        self.learner = learner

    def predict(self, task: Task) -> Prediction:
        return Prediction(self.learner.predict(task), 0)


class Abstraction:
    name = "E-abstraction"

    def __init__(self, learner: AbstractionLearner) -> None:
        self.learner = learner

    def predict(self, task: Task) -> Prediction:
        return Prediction(self.learner.predict(task), 0)


def build_conditions(train: list[Task]) -> list[object]:
    memory = Memory(train)
    return [
        NoMemory(),
        Retrieval(memory),
        Oracle(memory),
        Procedure(ProcedureLearner().fit(train)),
        Abstraction(AbstractionLearner().fit(train)),
    ]
