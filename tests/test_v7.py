"""Tests for Prototype 007's task generation and verification (no LLM calls)."""

import unittest

from ohmem.v7_transfer import (
    MOTIF,
    PLACEBO,
    OPS,
    build_conditions,
    transfer_tasks,
    verify,
)


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


if __name__ == "__main__":
    unittest.main()
