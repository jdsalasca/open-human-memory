"""Macro library learned from solved episodes (Prototype 003)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
import hashlib
import random

from .v3_tasks import DISTRACTORS, PRIMITIVES

PAIRS = tuple(product(PRIMITIVES, repeat=2))


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
    exclude = exclude or set()
    pool = [b for b in product(DISTRACTORS, repeat=2) if b not in exclude]
    if n_macros > len(pool):
        raise ValueError(
            f"only {len(pool)} distinct bodies available, asked {n_macros}"
        )
    bodies = random.Random(seed).sample(pool, n_macros)
    return Library([Macro(_name(b), b) for b in sorted(bodies)])


def same_language_libraries(n_macros: int = 3) -> list[Library]:
    """Every library of n_macros bodies drawn from the generator's own 16 pairs."""
    return [
        Library([Macro(_name(b), b) for b in combo])
        for combo in combinations(PAIRS, n_macros)
    ]
