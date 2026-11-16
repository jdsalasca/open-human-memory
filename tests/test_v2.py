import unittest

from ohmem.v2_conditions import (
    Abstraction,
    Oracle,
    Procedure,
    infer_composition,
    infer_primitive,
)
from ohmem.v2_experiment import run
from ohmem.v2_tasks import (
    PRIMITIVES,
    Solution,
    apply_rule,
    make_dataset,
    make_splits,
    make_task,
)


class LeakageTests(unittest.TestCase):
    def test_surface_has_no_rule_names(self):
        for family in ("alpha", "beta", "gamma", "delta"):
            task = make_task(0, family, 0)
            for primitive in PRIMITIVES:
                self.assertNotIn(primitive, task.observation.surface)

    def test_observation_has_no_solution(self):
        task = make_task(0, "alpha", 0)
        self.assertFalse(hasattr(task.observation, "solution"))
        self.assertFalse(hasattr(task.observation, "rule"))

    def test_support_examples_match_solution(self):
        task = make_task(0, "delta", 0)
        for x, y in zip(
            task.observation.support_inputs, task.observation.support_outputs
        ):
            self.assertEqual(apply_rule(task.solution.rule, x), y)


class InferenceTests(unittest.TestCase):
    def test_infer_primitive_on_primitive_task(self):
        for i in range(10):
            task = make_task(0, "alpha", i)
            self.assertEqual(infer_primitive(task.observation), task.solution.rule)

    def test_infer_composition_on_compositional_task(self):
        for i in range(10):
            task = make_task(0, "delta", i)
            inferred = infer_composition(task.observation)
            for x, y in zip(
                task.observation.support_inputs, task.observation.support_outputs
            ):
                self.assertEqual(apply_rule(inferred, x), y)

    def test_oracle_is_ceiling(self):
        task = make_task(0, "delta", 0)
        prediction = Oracle().predict(task.observation, task.solution)
        self.assertEqual(prediction.rule, task.solution.rule)


class ExperimentTests(unittest.TestCase):
    def test_shape(self):
        result = run(seed=0, n_train=40, n_eval=10)
        self.assertEqual(len(result["rows"]), 15)
        self.assertEqual(
            {r["distribution"] for r in result["rows"]}, {"D1", "D2", "D3"}
        )

    def test_abstraction_beats_procedure_on_composition(self):
        result = run(seed=0, n_train=80, n_eval=20)
        by_key = {
            (r["condition"], r["distribution"]): r["accuracy"] for r in result["rows"]
        }
        self.assertGreater(
            by_key[("E-compositional-abstraction", "D3")],
            by_key[("D-primitive-procedure", "D3")],
        )

    def test_oracle_upper_bound(self):
        result = run(seed=0, n_train=80, n_eval=20)
        by_key = {
            (r["condition"], r["distribution"]): r["accuracy"] for r in result["rows"]
        }
        for distribution in ("D1", "D2", "D3"):
            self.assertGreaterEqual(
                by_key[("C-oracle", distribution)],
                by_key[("B-retrieval", distribution)],
            )

    def test_splits_no_id_overlap(self):
        splits = make_splits(seed=0, n_train=20, n_eval=10)
        train_ids = {t.observation.id for t in splits["train"]}
        for name in ("D1", "D2", "D3"):
            self.assertFalse(train_ids & {t.observation.id for t in splits[name]})


if __name__ == "__main__":
    unittest.main()
