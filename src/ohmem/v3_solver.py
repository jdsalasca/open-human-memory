"""Program synthesis over a library, with two cost counters.

`primitive_ops` is an upper bound: every candidate, every primitive, every
support example, whether or not the check short-circuits. Prototype 004-A used it
and its numbers stay frozen.

`executed_steps` is the measured count: primitive applications actually run
before the first counterexample stops the check. Prototype 005 uses it.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from .v3_library import Library
from .v3_tasks import PRIMITIVES, Observation, apply_program


@dataclass
class SolveResult:
    program: tuple[str, ...] | None
    candidates: int
    primitive_ops: int
    ops: tuple[str, ...] = ()
    macros: tuple[str, ...] = ()
    executed_steps: int = 0
    overshoot: int = 0


def _over(executed: int, budget_steps: int | None) -> int:
    """Steps past the limit, measured from what actually ran."""
    return max(0, executed - budget_steps) if budget_steps else 0


def solve(
    obs: Observation,
    library: Library,
    max_steps: int = 2,
    budget: int | None = None,
    budget_steps: int | None = None,
    macro_first: bool = False,
) -> SolveResult:
    candidates = 0
    primitive_ops = 0
    executed = 0
    ops = (
        tuple(m.name for m in library.macros) + tuple(PRIMITIVES)
        if macro_first
        else library.operations
    )
    macro_names = {m.name for m in library.macros}
    for length in range(1, max_steps + 1):
        for sequence in product(ops, repeat=length):
            if budget is not None and candidates >= budget:
                return SolveResult(
                    None,
                    candidates,
                    primitive_ops,
                    (),
                    (),
                    executed,
                    _over(executed, budget_steps),
                )
            if budget_steps is not None and executed >= budget_steps:
                return SolveResult(
                    None,
                    candidates,
                    primitive_ops,
                    (),
                    (),
                    executed,
                    _over(executed, budget_steps),
                )
            candidates += 1
            expanded = tuple(
                primitive for name in sequence for primitive in library.expand(name)
            )
            primitive_ops += len(expanded) * len(obs.support_inputs)
            matched = True
            for x, y in zip(obs.support_inputs, obs.support_outputs):
                executed += len(expanded)
                if apply_program(expanded, x) != y:
                    matched = False
                    break
            if matched:
                used = tuple(name for name in sequence if name in macro_names)
                overshoot = _over(executed, budget_steps)
                return SolveResult(
                    expanded,
                    candidates,
                    primitive_ops,
                    sequence,
                    used,
                    executed,
                    overshoot,
                )
    return SolveResult(
        None, candidates, primitive_ops, (), (), executed, _over(executed, budget_steps)
    )
