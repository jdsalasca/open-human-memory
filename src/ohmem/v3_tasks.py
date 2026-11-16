"""Prototype 003: tasks whose depth-3 solutions require learned macros."""

from __future__ import annotations

from dataclasses import dataclass
import random

PRIMITIVES = ("sort_asc", "sort_desc", "add_one", "double")
DISTRACTORS = ("reverse", "negate")

TRAIN_PROGRAMS = (
    ("sort_asc", "double"),
    ("add_one", "sort_desc"),
    ("double", "add_one"),
)
D2_PROGRAMS = (
    ("sort_desc", "double"),
    ("double", "sort_desc"),
    ("add_one", "sort_asc"),
)
D3_PROGRAMS = (
    ("sort_asc", "double", "add_one"),
    ("add_one", "sort_desc", "double"),
    ("double", "add_one", "sort_asc"),
)

FAMILIES = {
    "alpha": ("alpha", "orion", "blue"),
    "beta": ("beta", "vega", "red"),
    "gamma": ("gamma", "lyra", "green"),
    "delta": ("delta", "atlas", "gold"),
}
NOISE = ("north", "south", "east", "west", "dawn", "dusk", "stone", "river")


def apply_primitive(name: str, numbers: tuple[int, ...]) -> tuple[int, ...]:
    if name == "sort_asc":
        return tuple(sorted(numbers))
    if name == "sort_desc":
        return tuple(sorted(numbers, reverse=True))
    if name == "add_one":
        return tuple(n + 1 for n in numbers)
    if name == "double":
        return tuple(n * 2 for n in numbers)
    if name == "reverse":
        return tuple(reversed(numbers))
    if name == "negate":
        return tuple(-n for n in numbers)
    raise ValueError(name)


def apply_program(
    program: tuple[str, ...], numbers: tuple[int, ...]
) -> tuple[int, ...]:
    values = numbers
    for primitive in program:
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
    program: tuple[str, ...]


@dataclass(frozen=True)
class Task:
    observation: Observation
    solution: Solution


def make_task(
    seed: int, family: str, index: int, program: tuple[str, ...], tag: str
) -> Task:
    rng = random.Random(f"{seed}:{family}:{index}:{program}")
    support_inputs = tuple(tuple(rng.randint(1, 9) for _ in range(4)) for _ in range(3))
    support_outputs = tuple(apply_program(program, x) for x in support_inputs)
    query = tuple(rng.randint(1, 9) for _ in range(4))
    surface = tuple(FAMILIES[family]) + tuple(rng.sample(NOISE, 2))
    return Task(
        observation=Observation(
            id=f"{tag}-{family}-{index}",
            family=family,
            surface=surface,
            support_inputs=support_inputs,
            support_outputs=support_outputs,
            query=query,
        ),
        solution=Solution(program),
    )


def make_splits(
    seed: int = 0, n_train: int = 60, n_eval: int = 30
) -> dict[str, list[Task]]:
    train = [
        make_task(
            seed,
            "alpha" if i % 2 else "beta",
            i,
            TRAIN_PROGRAMS[i % len(TRAIN_PROGRAMS)],
            "train",
        )
        for i in range(n_train)
    ]
    d1 = [
        make_task(
            seed + 1,
            "alpha" if i % 2 else "beta",
            i,
            (PRIMITIVES[i % len(PRIMITIVES)],),
            "d1",
        )
        for i in range(n_eval)
    ]
    d2 = [
        make_task(seed + 2, "gamma", i, D2_PROGRAMS[i % len(D2_PROGRAMS)], "d2")
        for i in range(n_eval)
    ]
    d3 = [
        make_task(seed + 3, "delta", i, D3_PROGRAMS[i % len(D3_PROGRAMS)], "d3")
        for i in range(n_eval)
    ]
    return {"train": train, "D1": d1, "D2": d2, "D3": d3}
