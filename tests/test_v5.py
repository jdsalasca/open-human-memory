"""Tests for Prototype 005.

`V5ReproductionTests` reproduces the frozen 005-A numbers. They are a historical
record, not invariants: if a future controller beats FROZEN or makes accumulation
work, that is a finding to record in a new test, not a bug to fix here.
`AccountingTests` are software invariants and do apply to any implementation.
"""

import unittest

from ohmem.v3_library import Library
from ohmem.v3_solver import solve
from ohmem.v3_tasks import make_depth3_grid
from ohmem.v5_experiment import Agent, behavioral_classes, run, stream_tasks


class V5ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run(seed=0)
        cls.cont = {(r["level"], r["condition"]): r for r in cls.result["continuity"]}
        cls.policies = {p["policy"]: p for p in cls.result["stream"]["policies"]}

    def test_grid_is_fewer_behaviours_than_syntax(self):
        reps, n = behavioral_classes()
        self.assertEqual(self.result["coverage"]["syntactic"], 64)
        self.assertEqual(len(reps), n)
        self.assertLess(n, 64)

    def test_library_loses_coverage_on_behaviours(self):
        cov = self.result["coverage"]
        self.assertLess(
            cov["learned_d2_on_representatives"],
            cov["no_memory_d3_on_representatives"],
        )

    def test_zero_continuity_hurts_the_library(self):
        no_memory = self.cont[(0.0, "no-memory-d3-uncapped")]["accuracy"]
        learned = self.cont[(0.0, "learned-d2-uncapped")]["accuracy"]
        self.assertGreater(no_memory, learned)

    def test_full_continuity_saves_work_at_equal_accuracy(self):
        no_memory = self.cont[(1.0, "no-memory-d3-uncapped")]
        learned = self.cont[(1.0, "learned-d2-uncapped")]
        self.assertEqual(no_memory["accuracy"], learned["accuracy"])
        self.assertLess(
            learned["mean_executed_steps"], no_memory["mean_executed_steps"]
        )

    def test_macro_first_trades_accuracy_for_steps(self):
        first = self.cont[(1.0, "learned-d2-macrofirst-budget")]
        base = self.cont[(1.0, "learned-d2-budget")]
        self.assertLessEqual(first["accuracy"], base["accuracy"])
        self.assertLess(first["mean_executed_steps"], base["mean_executed_steps"])

    def test_online_accumulation_is_worse_than_frozen(self):
        self.assertLess(
            self.policies["ONLINE"]["overall_accuracy"],
            self.policies["FROZEN"]["overall_accuracy"],
        )

    def test_gated_controller_does_not_beat_frozen(self):
        self.assertLess(
            self.policies["GATED"]["overall_accuracy"],
            self.policies["FROZEN"]["overall_accuracy"],
        )

    def test_frozen_saves_work_without_losing_accuracy(self):
        self.assertLess(
            self.policies["FROZEN"]["total_executed_steps"],
            self.policies["NOLEARN"]["total_executed_steps"],
        )
        self.assertGreaterEqual(
            self.policies["FROZEN"]["overall_accuracy"],
            self.policies["NOLEARN"]["overall_accuracy"] - 0.01,
        )


class AccountingTests(unittest.TestCase):
    def test_executed_steps_never_exceeds_the_upper_bound(self):
        tasks = make_depth3_grid(0)
        for task in tasks[:8]:
            result = solve(task.observation, Library([]), 3)
            self.assertLessEqual(result.executed_steps, result.primitive_ops)

    def test_budget_is_respected(self):
        tasks = [task for _, phase in stream_tasks(0) for task in phase][:6]
        agent = Agent(learn=False, cap=0)
        for task in tasks:
            _, executed = agent.step(task, max_steps=3, budget_steps=60)
            self.assertLessEqual(executed, 60)

    def test_overshoot_is_recorded_on_failed_candidates(self):
        from ohmem.v3_library import Macro
        from ohmem.v3_tasks import make_task

        library = Library([Macro("m", ("sort_asc", "double"))])
        task = make_task(0, "delta", 0, ("reverse", "negate"), "overshoot")
        result = solve(task.observation, library, max_steps=1, budget_steps=5)
        self.assertIsNone(result.program)
        self.assertGreater(result.overshoot, 0)
        self.assertEqual(result.overshoot, result.executed_steps - 5)

    def test_agent_caps_its_library(self):
        agent = Agent(learn=True, cap=3)
        for _, phase in stream_tasks(0):
            for task in phase:
                agent.step(task, max_steps=2, budget_steps=120)
        self.assertLessEqual(len(agent.macros), 3)


if __name__ == "__main__":
    unittest.main()
