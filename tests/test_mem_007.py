"""Tests for MEM-007's applicability conditions (no LLM calls)."""

import unittest

from ohmem.mem_007 import SKILLS, prompt_for, symbolic_solve, task_for


class Mem007Tests(unittest.TestCase):
    def test_preconditions(self):
        p1, p2, p3, p4 = SKILLS
        self.assertTrue(p1["precondition"]((1, 2, 3, 4)))
        self.assertFalse(p1["precondition"]((1, 1, 3, 4)))
        self.assertTrue(p2["precondition"]((6, 1, 2, 3)))
        self.assertFalse(p2["precondition"]((5, 1, 2, 3)))
        self.assertTrue(p3["precondition"]((1, 2, 3, 4)))
        self.assertFalse(p3["precondition"]((9, 9, 9, 9)))
        self.assertTrue(p4["precondition"]((1, 5, 2, 3)))
        self.assertFalse(p4["precondition"]((1, 2, 3, 4)))

    def test_tasks_cover_applicable_and_inapplicable(self):
        for skill in SKILLS:
            applicable = task_for(skill, True, 0)
            inapplicable = task_for(skill, False, 0)
            self.assertTrue(skill["precondition"](applicable.observation.query))
            self.assertFalse(skill["precondition"](inapplicable.observation.query))

    def test_prompts_differ_only_in_precondition(self):
        skill = SKILLS[0]
        task = task_for(skill, True, 0)
        clone = prompt_for(task, skill, "clone")
        no_meta = prompt_for(task, skill, "skill_no_meta")
        meta = prompt_for(task, skill, "skill_meta")
        self.assertNotIn("Precondición", clone)
        self.assertNotIn("Precondición", no_meta)
        self.assertIn("Precondición", meta)
        self.assertIn(skill["text"], meta)
        self.assertIn(" -> ".join(skill["program"]), no_meta)
        self.assertIn(" -> ".join(skill["program"]), meta)

    def test_symbolic_solver_finds_a_consistent_program(self):
        skill = SKILLS[0]
        task = task_for(skill, True, 0)
        program, answer, n_consistent = symbolic_solve(task, 2)
        self.assertIsNotNone(program)
        self.assertEqual(len(program), 2)
        self.assertGreaterEqual(n_consistent, 1)


if __name__ == "__main__":
    unittest.main()
