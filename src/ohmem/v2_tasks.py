"""Prototype 002: observations without labels, rules inferred from examples.

The public observation never contains the rule name. Each task provides a small
support set of input/output examples; the agent must infer the transformation.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

PRIMITIVES = ("sort_asc", "sort_desc", "add_one", "double")
COMPOSITIONS = (
    ("sort_asc", "double"),
    ("add_one", "double"),
    ("sort_desc", "add_one"),
)

FAMILIES: dict[str, tuple[tuple[str, ...], tuple[str, ...], bool]] = {
    # family: (surface tokens, allowed primitives, compositional?)
    "alpha": (("alpha", "orion", "blue"), ("sort_asc", "double"), False),
    "beta": (("beta", "vega", "red"), ("sort_desc", "add_one"), False),
    "gamma": (("gamma", "lyra", "green"), ("sort_asc", "double"), False),
    "delta": (("delta", "atlas", "gold"), ("sort_asc", "double"), True),
}

NOISE = ("north", "south", "east", "west", "dawn", "dusk", "stone", "river")


def apply_primitive(rule: str, numbers: tuple[int, ...]) -> tuple[int, ...]:
    if rule == "sort_asc":
        return tuple(sorted(numbers))
    if rule == "sort_desc":
        return tuple(sorted(numbers, reverse=True))
    if rule == "add_one":
        return tuple(n + 1 for n in numbers)
    if rule == "double":
        return tuple(n * 2 for n in numbers)
    raise ValueError(f"unknown primitive: {rule}")


def apply_rule(rule: tuple[str, ...], numbers: tuple[int, ...]) -> tuple[int, ...]:
    values = numbers
    for primitive in rule:
        values = apply_primitive(primitive, values)
    return values


@dataclass(frozen=True)
class Observation:
    id: str
    family: str
    surface: tuple[str, ...]
    support_inputs: tuple[tuple[int, ...], ...]
    support_outputs: tuple[tuple[int, ...], ...]
    query: tuple[int, ...]


@dataclass(frozen=True)
class Solution:
    rule: tuple[str, ...]


@dataclass(frozen=True)
class Task:
    observation: Observation
    solution: Solution


def make_task(seed: int, family: str, index: int, tag: str = "train") -> Task:
    rng = random.Random(f"{seed}:{family}:{index}")
    tokens, allowed, compositional = FAMILIES[family]
    if compositional:
        rule = rng.choice(COMPOSITIONS)
    else:
        rule = (rng.choice(allowed),)
    support_inputs = tuple(tuple(rng.randint(1, 9) for _ in range(4)) for _ in range(3))
    support_outputs = tuple(apply_rule(rule, x) for x in support_inputs)
    query = tuple(rng.randint(1, 9) for _ in range(4))
    # No rule token in the surface: only family and noise.
    surface = tuple(tokens) + tuple(rng.sample(NOISE, 2))
    observation = Observation(
        id=f"{tag}-{family}-{index}",
        family=family,
        surface=surface,
        support_inputs=support_inputs,
        support_outputs=support_outputs,
        query=query,
    )
    return Task(observation=observation, solution=Solution(rule=rule))


def make_dataset(seed: int, family: str, n: int, tag: str = "train") -> list[Task]:
    return [make_task(seed, family, i, tag=tag) for i in range(n)]


def make_splits(
    seed: int = 0, n_train: int = 200, n_eval: int = 50
) -> dict[str, list[Task]]:
    """Train on primitive alpha/beta. D1/D2 primitive; D3 compositional."""
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
