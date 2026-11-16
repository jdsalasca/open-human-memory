"""Tests for Prototype 006, corrected after the direction audit.

These reproduce the corrected 006-A' numbers on seed 1. They encode the
*negative* result: the learned policy must not beat the one-line rule, and its
probe must cost more than it saves. A future mechanism that beats the rule should
add a new test, not silently invert these.
"""

import unittest

from ohmem.v6_policy import build_library, novel_tasks, probe, run, similar_tasks


class V6CorrectedTests(unittest.TestCase):
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
        fit_similar = sum(probe(t.observation, self.lib)[0] for t in similar)
        fit_novel = sum(probe(t.observation, self.lib)[0] for t in novel)
        self.assertGreater(fit_similar, fit_novel)
        self.assertGreaterEqual(fit_similar / len(similar), 0.9)

    def test_policy_does_not_beat_the_simple_rule(self):
        self.assertLessEqual(
            self.app["mixed"]["learned-policy"]["accuracy"],
            self.app["mixed"]["probe-rule"]["accuracy"],
        )

    def test_policy_beats_search_on_accuracy(self):
        self.assertGreater(
            self.app["mixed"]["learned-policy"]["accuracy"],
            self.app["mixed"]["search"]["accuracy"],
        )

    def test_probe_costs_more_than_it_saves(self):
        policy = self.app["mixed"]["learned-policy"]
        search = self.app["mixed"]["search"]
        saved = search["mean_steps"] - policy["mean_steps"]
        self.assertGreater(policy["mean_probe_steps"], saved)
        self.assertGreater(policy["total_steps"], search["mean_steps"])

    def test_policy_total_cost_exceeds_not_deciding(self):
        self.assertGreater(
            self.app["mixed"]["learned-policy"]["total_steps"],
            self.app["mixed"]["memory_first"]["mean_steps"],
        )

    def test_uniform_random_is_not_the_trained_policy(self):
        uniform = self.app["mixed"]["uniform-random"]
        learned = self.app["mixed"]["learned-policy"]
        self.assertNotEqual(uniform["decisions"], learned["decisions"])

    def test_counters_are_measured_not_bounded(self):
        policy = self.app["mixed"]["learned-policy"]
        self.assertLess(policy["mean_probe_steps"], 60)


if __name__ == "__main__":
    unittest.main()
