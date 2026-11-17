"""Tests for MEM-006's skills, library, and symbolic baseline (no LLM calls)."""

import unittest

from ohmem.mem_006 import (
    RETRIEVAL_SCHEMA,
    SKILLS,
    library_text,
    retrieval_prompt,
    symbolic_solve,
)
from ohmem.v3_tasks import apply_program, make_task
from ohmem.v7_transfer import PROBES


def signature(program):
    return tuple(apply_program(program, probe) for probe in PROBES)


class Mem006Tests(unittest.TestCase):
    def test_skills_are_two_operations_and_distinct(self):
        self.assertEqual(len(SKILLS), 8)
        self.assertEqual(len({skill["id"] for skill in SKILLS}), 8)
        signatures = set()
        for skill in SKILLS:
            self.assertEqual(len(skill["program"]), 2)
            signatures.add(signature(skill["program"]))
        self.assertEqual(len(signatures), 8)

    def test_library_contains_all_skills_and_expert_variant(self):
        library = library_text(SKILLS)
        expert = library_text(SKILLS, expert=True)
        for skill in SKILLS:
            self.assertIn(skill["id"], library)
            self.assertIn(skill["id"], expert)
        self.assertIn("experto", expert)
        self.assertNotIn("experto", library)

    def test_retrieval_prompt_contains_examples_and_query(self):
        task = make_task(1, "delta", 50_001, SKILLS[0]["program"], "test")
        prompt = retrieval_prompt(library_text(SKILLS), task, 2)
        self.assertIn(str(list(task.observation.query)), prompt)
        self.assertIn(str(list(task.observation.support_inputs[0])), prompt)
        self.assertIn("skill_id", RETRIEVAL_SCHEMA["required"] or [])
        self.assertIn("query_output", RETRIEVAL_SCHEMA["properties"])

    def test_symbolic_solver_finds_a_consistent_program(self):
        task = make_task(1, "delta", 50_001, SKILLS[0]["program"], "test")
        program, answer, n_consistent = symbolic_solve(task, 2)
        self.assertIsNotNone(program)
        self.assertEqual(len(program), 2)
        self.assertGreaterEqual(n_consistent, 1)
        self.assertEqual(
            answer, list(apply_program(tuple(program), task.observation.query))
        )


if __name__ == "__main__":
    unittest.main()
