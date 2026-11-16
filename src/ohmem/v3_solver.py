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
    ops: tuple[str, ...] = ()
    macros: tuple[str, ...] = ()


def solve(
    obs: Observation,
    library: Library,
    max_steps: int = 2,
    budget: int | None = None,
) -> SolveResult:
    candidates = 0
    primitive_ops = 0
    ops = library.operations
    macro_names = {m.name for m in library.macros}
    for length in range(1, max_steps + 1):
        for sequence in product(ops, repeat=length):
            if budget is not None and candidates >= budget:
                return SolveResult(None, candidates, primitive_ops)
            candidates += 1
            expanded = tuple(
                primitive for name in sequence for primitive in library.expand(name)
            )
            # One primitive application per support example: the audit's honest count.
            primitive_ops += len(expanded) * len(obs.support_inputs)
            if all(
                apply_program(expanded, x) == y
                for x, y in zip(obs.support_inputs, obs.support_outputs)
            ):
                used = tuple(name for name in sequence if name in macro_names)
                return SolveResult(expanded, candidates, primitive_ops, sequence, used)
    return SolveResult(None, candidates, primitive_ops)
