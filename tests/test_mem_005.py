"""Tests for MEM-005's factorial conditions (no LLM calls)."""

import unittest

from ohmem.mem_005 import CONDITIONS, SPECS, extra_for


class Mem005Tests(unittest.TestCase):
    def test_all_conditions_have_specs(self):
        self.assertEqual(len(CONDITIONS), 10)
        self.assertEqual(set(CONDITIONS), set(SPECS))
        self.assertIsNone(SPECS["clone"])

    def test_factorial_is_complete(self):
        cells = {
            (content, status, instruction)
            for spec in SPECS.values()
            if spec is not None
            for status, instruction, content in [spec]
            if status in {"candidate", "verified"}
        }
        self.assertEqual(len(cells), 8)
        for content in ("correct", "placebo"):
            for status in ("candidate", "verified"):
                for instruction in ("verify", "apply"):
                    self.assertIn((content, status, instruction), cells)

    def test_status_and_instruction_are_separate(self):
        candidate_verify = extra_for("candidate", "verify", "A -> B")
        candidate_apply = extra_for("candidate", "apply", "A -> B")
        verified_verify = extra_for("verified", "verify", "A -> B")
        verified_apply = extra_for("verified", "apply", "A -> B")
        self.assertIn("candidata", candidate_verify)
        self.assertIn("verifica", candidate_verify)
        self.assertIn("candidata", candidate_apply)
        self.assertIn("Aplícalo", candidate_apply)
        self.assertIn("verificado", verified_verify)
        self.assertIn("verifica", verified_verify)
        self.assertIn("verificado", verified_apply)
        self.assertIn("Aplícalo", verified_apply)
        self.assertNotEqual(candidate_verify, verified_verify)
        self.assertNotEqual(candidate_apply, candidate_verify)

    def test_written_control_is_distinct(self):
        written = extra_for("written", "apply", "A -> B")
        verified = extra_for("verified", "apply", "A -> B")
        self.assertIn("programador", written)
        self.assertNotEqual(written, verified)


if __name__ == "__main__":
    unittest.main()
