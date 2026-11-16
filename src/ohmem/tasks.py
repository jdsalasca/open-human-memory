"""Synthetic diagnostic tasks for the memory-vs-selection experiment.

This is not an LLM benchmark. It is a controlled instrument to check that the
experimental conditions separate memory, selection, procedure, and abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

RULES = ("sort_asc", "sort_desc", "add_one", "double")
COMPOSITE_RULE = "sort_asc_then_double"

FAMILIES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "alpha": (("alpha", "orion", "blue"), ("sort_asc", "double")),
    "beta": (("beta", "vega", "red"), ("sort_desc", "add_one")),
    # Same structure as alpha, different surface: D2 transfer.
    "gamma": (("gamma", "lyra", "green"), ("sort_asc", "double")),
    # Structurally new: D3.
    "delta": (("delta", "atlas", "gold"), (COMPOSITE_RULE,)),
}

NOISE = ("north", "south", "east", "west", "dawn", "dusk", "stone", "river")


def apply_rule(rule: str, numbers: tuple[int, ...]) -> tuple[int, ...]:
    if rule == "sort_asc":
        return tuple(sorted(numbers))
    if rule == "sort_desc":
        return tuple(sorted(numbers, reverse=True))
    if rule == "add_one":
        return tuple(n + 1 for n in numbers)
    if rule == "double":
        return tuple(n * 2 for n in numbers)
    if rule == COMPOSITE_RULE:
        return tuple(n * 2 for n in sorted(numbers))
    raise ValueError(f"unknown rule: {rule}")


@dataclass(frozen=True)
class Task:
    id: str
    family: str
    surface: tuple[str, ...]
    numbers: tuple[int, ...]
    rule: str
    expected: tuple[int, ...]


def make_task(
    seed: int, family: str, index: int, rule: str | None = None, tag: str = "train"
) -> Task:
    rng = random.Random(f"{seed}:{family}:{index}")
    tokens, rules = FAMILIES[family]
    chosen = rule or rng.choice(rules)
    numbers = tuple(rng.randint(1, 20) for _ in range(4))
    # The rule token is predictive; family tokens add context; noise adds ambiguity.
    surface = tuple(tokens) + (chosen,) + tuple(rng.sample(NOISE, 2))
    return Task(
        id=f"{tag}-{family}-{index}",
        family=family,
        surface=surface,
        numbers=numbers,
        rule=chosen,
        expected=apply_rule(chosen, numbers),
    )


def make_dataset(seed: int, family: str, n: int, tag: str = "train") -> list[Task]:
    return [make_task(seed, family, i, tag=tag) for i in range(n)]


def make_splits(
    seed: int = 0, n_train: int = 200, n_eval: int = 50
) -> dict[str, list[Task]]:
    """Train on alpha/beta; evaluate D1 (same families), D2 (gamma), D3 (delta)."""
    train = make_dataset(seed, "alpha", n_train // 2, tag="train") + make_dataset(
        seed, "beta", n_train // 2, tag="train"
    )
    return {
        "D1": make_dataset(seed + 1, "alpha", n_eval // 2, tag="d1")
        + make_dataset(seed + 1, "beta", n_eval // 2, tag="d1"),
        "D2": make_dataset(seed + 2, "gamma", n_eval, tag="d2"),
        "D3": make_dataset(seed + 3, "delta", n_eval, tag="d3"),
        "train": train,
    }
