"""Episodic memory and simple learners used by the diagnostic conditions."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .tasks import Task


def jaccard(a: tuple[str, ...], b: tuple[str, ...]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


@dataclass
class Memory:
    items: list[Task]

    def retrieve(self, query: Task) -> Task | None:
        if not self.items:
            return None
        return max(self.items, key=lambda t: jaccard(query.surface, t.surface))

    def oracle(self, query: Task) -> Task | None:
        for task in self.items:
            if task.rule == query.rule:
                return task
        return None


class ProcedureLearner:
    """Learns a token -> rule vote table from successful traces."""

    def __init__(self) -> None:
        self.votes: dict[str, Counter[str]] = defaultdict(Counter)

    def fit(self, tasks: list[Task]) -> "ProcedureLearner":
        for task in tasks:
            for token in task.surface:
                self.votes[token][task.rule] += 1
        return self

    def predict(self, task: Task) -> str:
        scores: Counter[str] = Counter()
        for token in task.surface:
            scores.update(self.votes.get(token, {}))
        return scores.most_common(1)[0][0] if scores else "sort_asc"


class AbstractionLearner:
    """Learns a family -> rule mapping and a global fallback."""

    def __init__(self) -> None:
        self.by_family: dict[str, Counter[str]] = defaultdict(Counter)
        self.global_counts: Counter[str] = Counter()

    def fit(self, tasks: list[Task]) -> "AbstractionLearner":
        for task in tasks:
            self.by_family[task.family][task.rule] += 1
            self.global_counts[task.rule] += 1
        return self

    def predict(self, task: Task) -> str:
        counts = self.by_family.get(task.family)
        if counts:
            return counts.most_common(1)[0][0]
        return (
            self.global_counts.most_common(1)[0][0]
            if self.global_counts
            else "sort_asc"
        )
