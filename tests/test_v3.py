import unittest

from ohmem.v3_experiment import run, train_library
from ohmem.v3_library import Library
from ohmem.v3_solver import solve
from ohmem.v3_tasks import PRIMITIVES, make_splits


class V3Tests(unittest.TestCase):
    def test_learns_macros_from_training(self):
        library, solved = train_library(seed=0, n_train=60)
        self.assertGreater(solved, 0)
        self.assertGreater(len(library.macros), 0)
        for macro in library.macros:
            self.assertEqual(len(macro.body), 2)

    def test_no_program_names_in_surface(self):
        splits = make_splits(seed=0, n_train=5, n_eval=2)
        task = splits["D3"][0]
        for primitive in PRIMITIVES:
            self.assertNotIn(primitive, task.observation.surface)

    def test_learned_beats_no_learn_on_depth_three(self):
        result = run(seed=0, n_train=60, n_eval=30)
        by_key = {
            (r["condition"], r["distribution"]): r["accuracy"] for r in result["rows"]
        }
        self.assertGreater(by_key[("LEARNED", "D3")], by_key[("NOLEARN", "D3")])

    def test_ablation_loses_the_gain(self):
        result = run(seed=0, n_train=60, n_eval=30)
        by_key = {
            (r["condition"], r["distribution"]): r["accuracy"] for r in result["rows"]
        }
        self.assertEqual(by_key[("ABLATED", "D3")], by_key[("NOLEARN", "D3")])
        self.assertGreater(by_key[("LEARNED", "D3")], by_key[("ABLATED", "D3")])

    def test_costs_are_measured(self):
        result = run(seed=0, n_train=20, n_eval=10)
        self.assertTrue(all(row["cost"]["candidates"] > 0 for row in result["rows"]))

    def test_solver_returns_none_when_no_program_fits(self):
        splits = make_splits(seed=0, n_train=1, n_eval=1)
        task = splits["D3"][0]
        result = solve(task.observation, Library([]), max_steps=2)
        self.assertIsNone(result.program)


if __name__ == "__main__":
    unittest.main()
