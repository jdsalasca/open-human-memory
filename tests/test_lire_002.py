"""Tests for LIRE-002's independent table and case construction (no LLM calls)."""

import unittest

from ohmem.lire_002 import (
    LABELS,
    N_EXCEPTIONS,
    N_RULES,
    REPRESENTATIONS,
    build_prompt,
    build_skill,
    expected,
    make_cases,
    make_rules,
    table_bits,
)


class Lire002Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = make_rules(42)
        cls.by_code = {rule["code"]: rule for rule in cls.rules}
        cls.cases = make_cases(cls.rules, 42)

    def test_rules_are_unique_and_independent(self):
        self.assertEqual(len(self.rules), N_RULES)
        self.assertEqual(len(self.by_code), N_RULES)
        for rule in self.rules:
            self.assertEqual(len(rule["code"]), 4)
            self.assertIn(rule["status"], LABELS)
            self.assertFalse(
                len(rule["code"]) == 4
                and rule["code"][0] == "C"
                and rule["code"][1:].isdigit()
            )
        exceptions = [rule for rule in self.rules if rule["exception"] is not None]
        self.assertEqual(len(exceptions), N_EXCEPTIONS)
        for rule in exceptions:
            self.assertLess(rule["exception"]["threshold"], rule["threshold"])
            self.assertNotEqual(rule["exception"]["status"], rule["status"])

    def test_expected_checks_membership(self):
        rule = self.rules[0]
        self.assertEqual(expected(self.by_code, rule["code"], 0), rule["status"])
        self.assertEqual(
            expected(self.by_code, rule["code"], rule["threshold"]), "NONE"
        )
        self.assertEqual(expected(self.by_code, "ZZZZ", 0), "NONE")

    def test_exception_has_priority(self):
        rule = next(r for r in self.rules if r["exception"] is not None)
        amount = rule["exception"]["threshold"] - 1
        self.assertEqual(
            expected(self.by_code, rule["code"], amount),
            rule["exception"]["status"],
        )

    def test_cases_cover_the_strata(self):
        self.assertEqual(len(self.cases), 12)
        primary = [case for case in self.cases if case["primary"]]
        self.assertEqual(len(primary), 7)
        kinds = [case["kind"] for case in self.cases]
        self.assertEqual(kinds.count("unknown"), 2)
        self.assertEqual(kinds.count("positive_exception"), 2)
        self.assertEqual(kinds.count("positive_boundary"), 1)
        self.assertEqual(kinds.count("negative_boundary"), 1)
        for case in self.cases:
            self.assertEqual(
                case["expected"],
                expected(self.by_code, case["code"], case["amount"]),
            )
            if case["primary"]:
                self.assertNotEqual(case["expected"], "NONE")
            elif case["kind"] in {"unknown", "negative", "negative_boundary"}:
                self.assertEqual(case["expected"], "NONE")

    def test_every_representation_contains_the_table(self):
        for representation in REPRESENTATIONS:
            skill = build_skill(representation, self.rules)
            for rule in self.rules[:5]:
                self.assertIn(rule["code"], skill)
            self.assertIn(self.rules[0]["status"], skill)
        no_table = build_skill("none", self.rules)
        for rule in self.rules[:5]:
            self.assertNotIn(rule["code"], no_table)

    def test_prompt_defines_the_none_output(self):
        prompt = build_prompt("RULES", {"code": "AB12", "amount": 1})
        self.assertIn("return NONE", prompt)
        self.assertIn("AB12", prompt)

    def test_table_has_independent_information(self):
        self.assertGreater(table_bits(self.rules), 3000)


if __name__ == "__main__":
    unittest.main()
