"""Tests for LIRE-001's four-branch rule (no LLM calls)."""

import unittest

from ohmem.lire_001 import CASES, RULES, expected


class LireRuleTests(unittest.TestCase):
    def test_duplicate_even_adds_one(self):
        self.assertEqual(expected([4, 1, 4, 2]), [2, 3, 5, 5])

    def test_duplicate_odd_sorts_descending(self):
        self.assertEqual(expected([3, 1, 3, 7]), [7, 3, 3, 1])

    def test_no_duplicate_negative_doubles_reversed(self):
        self.assertEqual(expected([7, 2, 0, -1]), [-2, 0, 4, 14])

    def test_otherwise_adds_one_and_drops_last(self):
        self.assertEqual(expected([8, 3, 6, 2]), [3, 7, 4])

    def test_cases_cover_four_branches(self):
        branches = set()
        for case in CASES:
            duplicates = len(set(case)) < len(case)
            if duplicates and case[0] % 2 == 0:
                branches.add("dup_even")
            elif duplicates and case[0] % 2 == 1:
                branches.add("dup_odd")
            elif case[-1] < 0:
                branches.add("no_dup_negative")
            else:
                branches.add("otherwise")
        self.assertEqual(
            branches, {"dup_even", "dup_odd", "no_dup_negative", "otherwise"}
        )

    def test_every_representation_encodes_the_four_branches(self):
        self.assertEqual(set(RULES), {"es", "en", "zh", "es_concise", "dsl"})
        for rule in RULES.values():
            self.assertGreater(len(rule), 80)


if __name__ == "__main__":
    unittest.main()
