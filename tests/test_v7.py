"""Tests for Prototype 007's task generation and verification (no LLM calls)."""

import unittest

from ohmem.v7_transfer import (
    MOTIF,
    PLACEBO,
    OPS,
    build_conditions,
    extra_examples,
    transfer_tasks,
    verify,
    wrong_program,
)

MOTIF4 = ("sort_asc", "double", "add_one", "negate")


class V7Tests(unittest.TestCase):
    def test_unverified_artifact_is_never_delivered(self):
        with self.assertRaises(ValueError):
            build_conditions(None, False)
        with self.assertRaises(ValueError):
            build_conditions(list(MOTIF), False)
        with self.assertRaises(ValueError):
            build_conditions([], True)

    def test_memory_and_placebo_share_the_same_framing(self):
        conditions = build_conditions(list(MOTIF), True)
        self.assertIn("candidata", conditions["memory"])
        self.assertIn("candidata", conditions["placebo"])
        self.assertIn("Verifícala", conditions["memory"])
        self.assertIn("Verifícala", conditions["placebo"])
        self.assertIn("sort_asc", conditions["memory"])
        self.assertIn("sort_desc", conditions["placebo"])

    def test_motif_verifies(self):
        self.assertTrue(verify(list(MOTIF)))

    def test_placebo_does_not_verify(self):
        self.assertFalse(verify(list(PLACEBO)))

    def test_empty_program_does_not_verify(self):
        self.assertFalse(verify([]))
        self.assertFalse(verify(None))

    def test_transfer_tasks_are_depth_five_and_start_with_the_motif(self):
        tasks = transfer_tasks(0, 12)
        self.assertEqual(len(tasks), 12)
        for task in tasks:
            program = task.solution.program
            self.assertEqual(len(program), 5)
            self.assertEqual(program[:2], MOTIF)
            for op in program[2:]:
                self.assertIn(op, OPS)

    def test_custom_motif_verifies_and_builds_its_own_tasks(self):
        self.assertTrue(verify(list(MOTIF4), MOTIF4))
        self.assertFalse(verify(list(MOTIF), MOTIF4))
        for task in transfer_tasks(0, 6, 1, MOTIF4):
            self.assertEqual(len(task.solution.program), 5)
            self.assertEqual(task.solution.program[:4], MOTIF4)

    def test_wrong_program_has_the_same_length_and_does_not_verify(self):
        candidate = wrong_program(MOTIF4)
        self.assertEqual(len(candidate), 4)
        self.assertFalse(verify(list(candidate), MOTIF4))

    def test_history_and_oracle_conditions_keep_the_framing(self):
        conditions = build_conditions(
            list(MOTIF4),
            True,
            motif=MOTIF4,
            history=extra_examples(MOTIF4, 3, "session1"),
            include_oracle=True,
        )
        self.assertIn("experiencias anteriores", conditions["history"])
        self.assertIn(" -> ", conditions["history"])
        self.assertIn("{program}", conditions["oracle"])
        self.assertIn("candidata", conditions["memory"])
        self.assertIn("candidata", conditions["placebo"])


if __name__ == "__main__":
    unittest.main()
