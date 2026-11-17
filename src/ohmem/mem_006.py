"""MEM-006: multiple skills, autonomous retrieval, and a symbolic baseline."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

from .lire_001 import run_codex
from .v3_tasks import apply_program, make_task
from .v7_transfer import (
    OPS,
    SESSION1_SCHEMA,
    SESSION2_SCHEMA,
    session1_prompt,
    session2_prompt,
    verify,
)

SKILLS = [
    {"id": "s1", "program": ("sort_asc", "double")},
    {"id": "s2", "program": ("reverse", "add_one")},
    {"id": "s3", "program": ("sort_desc", "negate")},
    {"id": "s4", "program": ("double", "add_one")},
    {"id": "s5", "program": ("reverse", "double")},
    {"id": "s6", "program": ("sort_asc", "negate")},
    {"id": "s7", "program": ("sort_desc", "add_one")},
    {"id": "s8", "program": ("sort_desc", "double")},
]

RETRIEVAL_SCHEMA = {
    "type": "object",
    "properties": {
        "skill_id": {"type": "string"},
        "query_output": {"type": "array", "items": {"type": "integer"}},
    },
    "required": ["skill_id", "query_output"],
    "additionalProperties": False,
}


def library_text(skills: list[dict], expert: bool = False) -> str:
    header = (
        "Biblioteca escrita por un experto; cada habilidad tiene 2 operaciones:"
        if expert
        else "Biblioteca de habilidades; cada una tiene 2 operaciones:"
    )
    rows = "\n".join(
        f"{skill['id']}: {' -> '.join(skill['program'])}. "
        "Verificación: aprobada; ámbito: listas de enteros."
        for skill in skills
    )
    return f"{header}\n{rows}"


def retrieval_prompt(library: str, task, support: int) -> str:
    examples = "\n".join(
        f"{list(x)} -> {list(y)}"
        for x, y in zip(
            task.observation.support_inputs[:support],
            task.observation.support_outputs[:support],
        )
    )
    return (
        f"{library}\n\nTarea: elige la habilidad que reproduce los dos ejemplos.\n"
        f"{examples}\nEntrada a transformar: {list(task.observation.query)}\n\n"
        "Devuelve el id de la habilidad y la lista resultante."
    )


def symbolic_solve(task, support: int = 2) -> tuple[list[str] | None, list[str], int]:
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks-per-skill", type=int, default=2)
    parser.add_argument("--support", type=int, default=2)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--session1-examples", type=int, default=12)
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--out", default="mem-006.json")
    args = parser.parse_args()

    library: list[dict] = []
    acquisition = []
    for skill in SKILLS:
        result = run_codex(
            session1_prompt(args.session1_examples, True, skill["program"]),
            args.model,
            args.effort,
            args.timeout,
            schema=SESSION1_SCHEMA,
            answer_key="program",
        )
        learned = result["answer"]
        ok = verify(learned, skill["program"])
        acquisition.append(
            {
                "skill_id": skill["id"],
                "program": list(skill["program"]),
                "learned": learned,
                "verified": ok,
                "seconds": result["seconds"],
                "input_tokens": result["usage"].get("input_tokens"),
            }
        )
        print(f"acquisition {skill['id']} verified={ok} program={learned}")
        if ok:
            library.append({"id": skill["id"], "program": tuple(learned)})

    if len(library) < 2:
        payload = {
            "model": args.model,
            "effort": args.effort,
            "acquisition": acquisition,
            "error": "fewer than two skills verified; experiment aborted",
            "rows": [],
        }
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print("fewer than two skills verified; aborting")
        return

    retrieval_library = library_text(library)
    expert_library = library_text(library, expert=True)
    conditions = [
        "clone",
        "oracle_skill",
        "retrieval",
        "random_skill",
        "expert_written",
    ]
    order_rng = random.Random(f"mem006-order:{args.seed}")
    rows = []
    tasks = []
    for skill in library:
        for j in range(args.tasks_per_skill):
            task = make_task(
                args.seed,
                "delta",
                50_000 + int(skill["id"][1:]) * 10 + j,
                tuple(skill["program"]),
                "mem006",
            )
            tasks.append((skill, task))

    for task_index, (skill, task) in enumerate(tasks):
        expected = list(apply_program(tuple(skill["program"]), task.observation.query))
        solver_program, solver_answer, n_consistent = symbolic_solve(task, args.support)
        solver_ok = solver_answer == expected
        rows.append(
            {
                "condition": "symbolic_solver",
                "task_index": task_index,
                "skill_id": skill["id"],
                "chosen_skill": "symbolic",
                "expected": expected,
                "answer": solver_answer,
                "correct": solver_ok,
                "skill_correct": True,
                "program": list(skill["program"]),
                "solver_program": solver_program,
                "n_consistent": n_consistent,
                "prompt_chars": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "timed_out": False,
                "seconds": 0,
            }
        )
        order = list(conditions)
        order_rng.shuffle(order)
        for position, condition in enumerate(order):
            if condition == "clone":
                extra = (
                    "\nNo hay subrutinas de experiencias anteriores disponibles; "
                    "usa únicamente los ejemplos de la tarea actual.\n"
                )
                prompt = session2_prompt(task, extra, args.support)
                result = run_codex(
                    prompt,
                    args.model,
                    args.effort,
                    args.timeout,
                    schema=SESSION2_SCHEMA,
                    answer_key="query_output",
                )
                chosen = None
                answer = result["answer"]
                skill_ok = False
            elif condition in {"oracle_skill", "random_skill"}:
                if condition == "oracle_skill":
                    chosen = skill
                else:
                    others = [s for s in library if s["id"] != skill["id"]]
                    chosen = order_rng.choice(others)
                extra = (
                    f"\nLa habilidad seleccionada es {chosen['id']}: "
                    f"{' -> '.join(chosen['program'])}. Aplícala a la entrada.\n"
                )
                prompt = session2_prompt(task, extra, args.support)
                result = run_codex(
                    prompt,
                    args.model,
                    args.effort,
                    args.timeout,
                    schema=SESSION2_SCHEMA,
                    answer_key="query_output",
                )
                answer = result["answer"]
                skill_ok = chosen["id"] == skill["id"]
            else:
                library_used = (
                    expert_library
                    if condition == "expert_written"
                    else retrieval_library
                )
                prompt = retrieval_prompt(library_used, task, args.support)
                result = run_codex(
                    prompt,
                    args.model,
                    args.effort,
                    args.timeout,
                    schema=RETRIEVAL_SCHEMA,
                    answer_key="skill_id",
                )
                payload = result["payload"] or {}
                chosen = payload.get("skill_id")
                answer = payload.get("query_output")
                skill_ok = chosen == skill["id"]

            ok = answer == expected
            rows.append(
                {
                    "condition": condition,
                    "task_index": task_index,
                    "skill_id": skill["id"],
                    "chosen_skill": chosen["id"]
                    if isinstance(chosen, dict)
                    else chosen,
                    "expected": expected,
                    "answer": answer,
                    "correct": ok,
                    "skill_correct": skill_ok,
                    "program": list(skill["program"]),
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
                f"{condition:<15} [{task_index + 1}/{len(tasks)}] "
                f"{'OK ' if ok else 'FAIL'} skill={chosen if isinstance(chosen, str) else (chosen or {}).get('id')} "
                f"want={skill['id']} {result['seconds']}s"
            )

    summary = {
        "model": args.model,
        "effort": args.effort,
        "seed": args.seed,
        "tasks_per_skill": args.tasks_per_skill,
        "support": args.support,
        "n_skills": len(library),
        "library": library,
        "acquisition": acquisition,
        "conditions": {
            condition: {
                "correct": sum(
                    1
                    for row in rows
                    if row["condition"] == condition and row["correct"]
                ),
                "n": sum(1 for row in rows if row["condition"] == condition),
                "accuracy": round(
                    sum(
                        1
                        for row in rows
                        if row["condition"] == condition and row["correct"]
                    )
                    / max(1, sum(1 for row in rows if row["condition"] == condition)),
                    4,
                ),
                "skill_correct": sum(
                    1
                    for row in rows
                    if row["condition"] == condition and row["skill_correct"]
                ),
            }
            for condition in conditions + ["symbolic_solver"]
        },
        "rows": rows,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["conditions"], indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
