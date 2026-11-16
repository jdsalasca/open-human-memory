import unittest

from ohmem.conditions import build_conditions
from ohmem.experiment import run
from ohmem.memory import AbstractionLearner, Memory, ProcedureLearner
from ohmem.tasks import apply_rule, make_dataset, make_splits


class TaskTests(unittest.TestCase):
    def test_rules(self):
        self.assertEqual(apply_rule("sort_asc", (3, 1, 2)), (1, 2, 3))
        self.assertEqual(apply_rule("sort_desc", (3, 1, 2)), (3, 2, 1))
        self.assertEqual(apply_rule("add_one", (1, 2)), (2, 3))
        self.assertEqual(apply_rule("double", (1, 2)), (2, 4))
        self.assertEqual(apply_rule("sort_asc_then_double", (3, 1, 2)), (2, 4, 6))

    def test_generation_is_deterministic(self):
        a = make_dataset(7, "alpha", 5)
        b = make_dataset(7, "alpha", 5)
        self.assertEqual(a, b)
        self.assertEqual(len({t.id for t in a}), 5)

    def test_splits_have_no_id_overlap(self):
        splits = make_splits(seed=1, n_train=20, n_eval=10)
        train_ids = {t.id for t in splits["train"]}
        for name in ("D1", "D2", "D3"):
            self.assertFalse(train_ids & {t.id for t in splits[name]})


class MemoryTests(unittest.TestCase):
    def test_retrieval_returns_most_similar(self):
        tasks = make_dataset(0, "alpha", 10)
        memory = Memory(tasks)
        self.assertIn(memory.retrieve(tasks[0]), tasks)

    def test_oracle_finds_same_rule(self):
        tasks = make_dataset(0, "alpha", 20)
        memory = Memory(tasks)
        for task in tasks:
            found = memory.oracle(task)
            self.assertIsNotNone(found)
            self.assertEqual(found.rule, task.rule)

    def test_learners_fit_and_predict(self):
        tasks = make_dataset(0, "alpha", 20)
        self.assertIn(
            ProcedureLearner().fit(tasks).predict(tasks[0]), {"sort_asc", "double"}
        )
        self.assertIn(
            AbstractionLearner().fit(tasks).predict(tasks[0]), {"sort_asc", "double"}
        )


class ExperimentTests(unittest.TestCase):
    def test_run_has_expected_shape(self):
        result = run(seed=0, n_train=40, n_eval=10)
        self.assertEqual(len(result["rows"]), 15)
        self.assertEqual(
            {r["distribution"] for r in result["rows"]}, {"D1", "D2", "D3"}
        )
        self.assertTrue(all(0.0 <= r["accuracy"] <= 1.0 for r in result["rows"]))

    def test_oracle_is_upper_bound_on_d1(self):
        result = run(seed=0, n_train=100, n_eval=20)
        by_key = {
            (r["condition"], r["distribution"]): r["accuracy"] for r in result["rows"]
        }
        self.assertGreaterEqual(
            by_key[("C-oracle", "D1")], by_key[("B-retrieval", "D1")]
        )

    def test_abstraction_beats_no_memory_on_known_families(self):
        result = run(seed=0, n_train=100, n_eval=20)
        by_key = {
            (r["condition"], r["distribution"]): r["accuracy"] for r in result["rows"]
        }
        self.assertGreater(
            by_key[("E-abstraction", "D1")], by_key[("A-no-memory", "D1")]
        )

    def test_conditions_are_built(self):
        splits = make_splits(seed=0, n_train=20, n_eval=5)
        self.assertEqual(len(build_conditions(splits["train"])), 5)


if __name__ == "__main__":
    unittest.main()
