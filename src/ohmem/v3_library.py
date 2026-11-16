"""Macro library learned from solved episodes (Prototype 003)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import random

from .v3_tasks import DISTRACTORS, PRIMITIVES


@dataclass(frozen=True)
class Macro:
    name: str
    body: tuple[str, ...]


@dataclass
class Library:
    macros: list[Macro]

    @property
    def operations(self) -> tuple[str, ...]:
        return tuple(PRIMITIVES) + tuple(m.name for m in self.macros)

    def expand(self, name: str) -> tuple[str, ...]:
        for macro in self.macros:
            if macro.name == name:
                return macro.body
        return (name,)

    def size(self) -> int:
        return len(self.operations)


def _name(body: tuple[str, ...]) -> str:
    digest = hashlib.sha1("|".join(body).encode()).hexdigest()[:8]
    return f"m_{digest}"


def learn_macros(programs: list[tuple[str, ...]], min_count: int = 2) -> Library:
    counts = Counter(p for p in programs if len(p) == 2)
    macros = [
        Macro(_name(body), body) for body, count in counts.items() if count >= min_count
    ]
    return Library(macros)


def random_library(
    n_macros: int, seed: int = 0, exclude: set[tuple[str, ...]] | None = None
) -> Library:
    rng = random.Random(seed)
    exclude = exclude or set()
    bodies = set()
    while len(bodies) < n_macros:
        body = tuple(rng.choice(DISTRACTORS) for _ in range(2))
        if body not in exclude:
            bodies.add(body)
    return Library([Macro(_name(b), b) for b in sorted(bodies)])
