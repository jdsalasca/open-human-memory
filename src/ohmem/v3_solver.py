"""Program synthesis over a library, with measured search cost."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .v3_library import Library
from .v3_tasks import Observation, apply_program


@dataclass
class SolveResult:
    program: tuple[str, ...] | None
    candidates: int
    primitive_ops: int


def solve(obs: Observation, library: Library, max_steps: int = 2) -> SolveResult:
    candidates = 0
    primitive_ops = 0
    ops = library.operations
    for length in range(1, max_steps + 1):
        for sequence in product(ops, repeat=length):
            candidates += 1
            expanded = tuple(
                primitive for name in sequence for primitive in library.expand(name)
            )
            primitive_ops += len(expanded)
            if all(
                apply_program(expanded, x) == y
                for x, y in zip(obs.support_inputs, obs.support_outputs)
            ):
                return SolveResult(expanded, candidates, primitive_ops)
    return SolveResult(None, candidates, primitive_ops)
