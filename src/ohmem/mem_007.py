"""MEM-007: applicability. Can the agent reject a verified skill when its
precondition fails?"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from .lire_001 import run_codex
from .v3_tasks import apply_program, make_task
from .v7_transfer import OPS

SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string"},
        "query_output": {"type": "array", "items": {"type": "integer"}},
    },
    "required": ["status", "query_output"],
    "additionalProperties": False,
}

SKILLS = [
    {
        "id": "p1",
        "program": ("sort_asc", "double"),
        "precondition": lambda q: len(set(q)) == len(q),
        "text": "la entrada no tiene elementos duplicados",
    },
    {
        "id": "p2",
        "program": ("reverse", "add_one"),
        "precondition": lambda q: q[0] > 5,
        "text": "el primer elemento es mayor que 5",
    },
    {
        "id": "p3",
        "program": ("sort_desc", "negate"),
        "precondition": lambda q: sum(q) < 20,
        "text": "la suma de los elementos es menor que 20",
    },
    {
        "id": "p4",
        "program": ("double", "add_one"),
        "precondition": lambda q: 5 in q,
        "text": "la entrada contiene el número 5",
    },
]


def prompt_for(task, skill: dict, mode: str, support: int = 2) -> str:
    examples = "\n".join(
        f"{list(x)} -> {list(y)}"
        for x, y in zip(
            task.observation.support_inputs[:support],
            task.observation.support_outputs[:support],
        )
    )
    if mode == "clone":
        return (
            f"Resuelve esta tarea de transformación de listas.\n{examples}\n"
            f"Entrada a transformar: {list(task.observation.query)}\n\n"
            "Si la tarea no se puede resolver, devuelve status NONE y una lista vacía."
        )
    procedure = " -> ".join(skill["program"])
    if mode == "skill_no_meta":
        return (
            f"Habilidad verificada {skill['id']}: {procedure}.\n"
            f"Verificación: aprobada (60 sondas).\n{examples}\n"
            f"Entrada a transformar: {list(task.observation.query)}\n\n"
            "Aplica la habilidad y devuelve status APPLY y la lista resultante."
        )
    if mode == "skill_meta":
        return (
            f"Habilidad verificada {skill['id']}: {procedure}.\n"
            f"Verificación: aprobada (60 sondas).\n"
            f"Precondición: {skill['text']}.\n{examples}\n"
            f"Entrada a transformar: {list(task.observation.query)}\n\n"
            "Si la precondición se cumple, aplica la habilidad y devuelve status APPLY "
            "y la lista resultante. Si no se cumple, devuelve status NONE y una lista "
            "vacía."
        )
    raise ValueError(mode)


def symbolic_solve(task, support: int = 2) -> tuple[list[str] | None, list[int], int]:
    pairs = list(
        zip(
            task.observation.support_inputs[:support],
            task.observation.support_outputs[:support],
        )
    )
    consistent = [
        program
        for program in itertools.product(OPS, repeat=2)
        if all(apply_program(program, x) == y for x, y in pairs)
    ]
    if not consistent:
        return None, [], 0
    program = consistent[0]
    return (
        list(program),
        list(apply_program(program, task.observation.query)),
        len(consistent),
    )


def task_for(skill: dict, applicable: bool, index: int, seed: int = 1):
    offset = 0
    while True:
        task = make_task(
            seed,
            "delta",
            60_000 + int(skill["id"][1:]) * 100 + (0 if applicable else 50) + offset,
            skill["program"],
            "mem007",
        )
        if bool(skill["precondition"](task.observation.query)) == applicable:
            return task
        offset += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--support", type=int, default=2)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--out", default="mem-007.json")
    args = parser.parse_args()

    tasks = []
    for skill in SKILLS:
        for applicable in (True, False):
            for j in range(2):
                tasks.append(
                    (skill, applicable, task_for(skill, applicable, j, args.seed))
                )
    order_rng = random.Random(f"mem007-order:{args.seed}")
    rows = []
    for task_index, (skill, applicable, task) in enumerate(tasks):
        expected = list(apply_program(skill["program"], task.observation.query))
        expected_status = "APPLY" if applicable else "NONE"
        solver_program, solver_answer, n_consistent = symbolic_solve(task, args.support)
        rows.append(
            {
                "condition": "symbolic_solver",
                "task_index": task_index,
                "skill_id": skill["id"],
                "applicable": applicable,
                "expected_status": expected_status,
                "expected": expected if applicable else [],
                "status": "APPLY",
                "answer": solver_answer,
                "correct": applicable and solver_answer == expected,
                "solver_program": solver_program,
                "n_consistent": n_consistent,
                "prompt_chars": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "timed_out": False,
                "seconds": 0,
            }
        )
        conditions = ["clone", "skill_no_meta", "skill_meta"]
        order_rng.shuffle(conditions)
        for position, condition in enumerate(conditions):
            prompt = prompt_for(task, skill, condition, args.support)
            result = run_codex(
                prompt,
                args.model,
                args.effort,
                args.timeout,
                schema=SCHEMA,
                answer_key="status",
            )
            payload = result["payload"] or {}
            status = str(payload.get("status", "")).strip().upper()
            answer = payload.get("query_output")
            if applicable:
                correct = status == "APPLY" and answer == expected
            else:
                correct = status == "NONE"
            rows.append(
                {
                    "condition": condition,
                    "task_index": task_index,
                    "skill_id": skill["id"],
                    "applicable": applicable,
                    "expected_status": expected_status,
                    "expected": expected if applicable else [],
                    "status": status,
                    "answer": answer,
                    "correct": correct,
                    "solver_program": solver_program,
                    "n_consistent": n_consistent,
                    "prompt_chars": len(prompt),
                    "input_tokens": result["usage"].get("input_tokens"),
                    "output_tokens": result["usage"].get("output_tokens"),
                    "timed_out": result["timed_out"],
                    "seconds": result["seconds"],
                    "order": position,
                }
            )
            print(
                f"{condition:<14} [{task_index + 1}/{len(tasks)}] "
                f"{'OK ' if correct else 'FAIL'} applicable={applicable} "
                f"status={status} {result['seconds']}s"
            )

    summary = {
        "model": args.model,
        "effort": args.effort,
        "seed": args.seed,
        "support": args.support,
        "conditions": {
            condition: {
                "correct": sum(
                    1
                    for row in rows
                    if row["condition"] == condition and row["correct"]
                ),
                "n": sum(1 for row in rows if row["condition"] == condition),
                "applicable_correct": sum(
                    1
                    for row in rows
                    if row["condition"] == condition
                    and row["applicable"]
                    and row["correct"]
                ),
                "applicable_n": sum(
                    1
                    for row in rows
                    if row["condition"] == condition and row["applicable"]
                ),
                "inapplicable_correct": sum(
                    1
                    for row in rows
                    if row["condition"] == condition
                    and not row["applicable"]
                    and row["correct"]
                ),
                "inapplicable_n": sum(
                    1
                    for row in rows
                    if row["condition"] == condition and not row["applicable"]
                ),
            }
            for condition in ["clone", "skill_no_meta", "skill_meta", "symbolic_solver"]
        },
        "rows": rows,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["conditions"], indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
