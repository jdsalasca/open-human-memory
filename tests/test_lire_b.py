"""Tests for LIRE-001b's long skill (no LLM calls)."""

import unittest

from ohmem.lire_001b import CASES, LINES, N_RULES, expected, skill_for


class LireLongSkillTests(unittest.TestCase):
    def test_threshold_rule(self):
        self.assertEqual(expected(3, 2), "S003")
        self.assertEqual(expected(51, 60), "NONE")
        self.assertEqual(expected(117, 120), "NONE")

    def test_every_representation_contains_all_rules(self):
        for representation in LINES:
            skill = skill_for(representation)
            self.assertGreater(len(skill), 2000)
            for code in (0, 57, 119):
                self.assertIn(f"C{code:03d}", skill)

    def test_cases_cover_both_outcomes(self):
        outcomes = {expected(code, amount) for code, amount in CASES}
        self.assertIn("NONE", outcomes)
        self.assertTrue(any(outcome.startswith("S") for outcome in outcomes))


if __name__ == "__main__":
    unittest.main()
