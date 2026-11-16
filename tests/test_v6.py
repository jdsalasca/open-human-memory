"""Tests for Prototype 006.

`V6ReproductionTests` reproduces the frozen 006-A numbers on seed 1 (not used for
development). They are a historical record: a future policy that beats these
numbers should add a test, not break one. `ProbeAccountingTests` is the invariant
that matters for any implementation: the decision signal has to be cheaper than
the work it saves.
"""

import unittest

from ohmem.v3_solver import solve
from ohmem.v3_tasks import PRIMITIVES, apply_program
from ohmem.v6_policy import (
    build_library,
    macro_any_fit,
    novel_tasks,
    run,
    similar_tasks,
)


def probe_cost(obs, library) -> int:
    steps = 0
    for macro in library.macros:
        for primitive in PRIMITIVES:
            for body in (macro.body + (primitive,), (primitive,) + macro.body):
                steps += len(body) * len(obs.support_inputs)
                if all(
                    apply_program(body, x) == y
                    for x, y in zip(obs.support_inputs, obs.support_outputs)
                ):
                    return steps
    return steps


class V6ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run(seed=1)
        cls.lib = build_library(1)
        cls.app = cls.result["policies"]["policy-applicability"]["conditions"]
        cls.blind = cls.result["policies"]["policy-blind"]["conditions"]

    def test_library_is_small_and_frozen(self):
        self.assertLessEqual(len(self.lib.macros), 4)
        self.assertEqual(
            [list(m.body) for m in self.lib.macros], self.result["library"]
        )

    def test_probe_separates_the_two_regimes(self):
        similar = similar_tasks(1)
        novel = novel_tasks(1, self.lib)
        fit_similar = sum(macro_any_fit(t.observation, self.lib) for t in similar)
        fit_novel = sum(macro_any_fit(t.observation, self.lib) for t in novel)
        self.assertGreater(fit_similar, fit_novel)
        self.assertGreaterEqual(fit_similar / len(similar), 0.9)

    def test_policy_recovers_on_novel(self):
        self.assertGreaterEqual(
            self.app["novel"]["learned-policy"]["accuracy"],
            self.app["novel"]["memory"]["accuracy"],
        )

    def test_blind_policy_cannot_recover(self):
        self.assertLessEqual(
            self.blind["novel"]["learned-policy"]["accuracy"],
            self.app["novel"]["learned-policy"]["accuracy"],
        )

    def test_policy_beats_search_on_mixed(self):
        self.assertGreater(
            self.app["mixed"]["learned-policy"]["accuracy"],
            self.app["mixed"]["search"]["accuracy"],
        )


class ProbeAccountingTests(unittest.TestCase):
    def test_probe_costs_more_than_it_saves(self):
        library = build_library(1)
        tasks = similar_tasks(1)
        probe = sum(probe_cost(t.observation, library) for t in tasks) / len(tasks)
        with_memory = solve(tasks[0].observation, library, 2, budget_steps=120)
        self.assertGreater(probe, 0)
        self.assertGreater(with_memory.executed_steps, 0)
        # The search saving on this set is ~29 steps/task; the probe is far larger.
        self.assertGreater(probe, 60)


if __name__ == "__main__":
    unittest.main()
