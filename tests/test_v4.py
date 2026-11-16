"""Validity tests for Prototype 004-A.

These reproduce the frozen 004-A numbers. They are a historical record, not
invariants: if a future implementation beats plain deeper search, record it in a
new test instead of treating this one as broken.
"""

import unittest

from ohmem.v3_library import Library, random_library
from ohmem.v4_experiment import run, train
from ohmem.v3_solver import solve
from ohmem.v3_tasks import make_depth3_grid


class V4ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run(seed=0, n_train=60)
        cls.by = {c["condition"]: c for c in cls.result["conditions"]}

    def test_no_history_depth3_solves_the_whole_grid(self):
        self.assertEqual(self.by["A1-nolearn-d3"]["accuracy"], 1.0)

    def test_learned_library_does_not_cover_the_grid(self):
        self.assertLess(self.by["A3-learned-d2"]["accuracy"], 1.0)
        self.assertLess(
            self.by["A3-learned-d2"]["correct"], self.by["A1-nolearn-d3"]["correct"]
        )

    def test_macros_save_candidates_but_lose_correctness(self):
        self.assertLess(
            self.by["A3-learned-d2"]["cost"]["candidates"],
            self.by["A1-nolearn-d3"]["cost"]["candidates"],
        )
        self.assertLess(
            self.by["A3-learned-d2"]["correct"], self.by["A1-nolearn-d3"]["correct"]
        )

    def test_learned_library_at_depth3_is_more_expensive(self):
        self.assertGreater(
            self.by["A4-learned-d3"]["cost"]["candidates"],
            self.by["A1-nolearn-d3"]["cost"]["candidates"],
        )

    def test_same_language_sweep_reproduces_the_audit(self):
        sweep = self.result["sweep_selected_d3"]
        self.assertEqual(sweep["n_libraries"], 560)
        self.assertEqual(sweep["perfect"], 250)
        self.assertAlmostEqual(sweep["mean_accuracy"], 0.7054, places=4)

    def test_arbitrary_libraries_match_or_beat_the_learned_one(self):
        learned = self.by["A3-learned-d2"]["accuracy"]
        better = [
            row
            for row in self.result["sweep_grid"]["rows"]
            if row["accuracy"] >= learned
        ]
        self.assertGreater(len(better), 0)

    def test_acquisition_saturates_early(self):
        rows = {r["n_train"]: r["accuracy"] for r in self.result["acquisition"]["rows"]}
        self.assertEqual(rows[6], rows[60])
        self.assertLess(rows[3], rows[6])

    def test_budget_matched_deeper_search_wins_at_full_budget(self):
        budget = self.result["budget"]
        self.assertGreaterEqual(
            budget["A1-nolearn-d3"][-1]["correct"],
            budget["A3-learned-d2"][-1]["correct"],
        )

    def test_ablation_removes_macros_not_history(self):
        ablated = self.by["A0-nolearn-d2"]
        self.assertEqual(ablated["library_size"], 4)
        self.assertEqual(ablated["macro_tasks"], 0)

    def test_random_library_refuses_impossible_request(self):
        with self.assertRaises(ValueError):
            random_library(5)


class ZeroHistoryTests(unittest.TestCase):
    def test_depth_two_already_solves_some_depth_three_programs(self):
        # Observational equivalence: sort twice equals sort once, so a depth-2
        # solver covers part of the depth-3 lattice without any memory.
        tasks = make_depth3_grid(0)
        solved = sum(
            1 for task in tasks if solve(task.observation, Library([]), 2).program
        )
        self.assertGreater(solved, 0)

    def test_training_cost_is_reported(self):
        _, report = train(0, 60)
        self.assertGreater(report["cost"]["candidates"], 0)
        self.assertEqual(report["solved"], 60)


if __name__ == "__main__":
    unittest.main()
