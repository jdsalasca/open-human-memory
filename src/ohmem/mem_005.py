"""MEM-005: factorial content x communicated status x instruction.

The MEM-003/004 contrast changed two things at once: the epistemic status
(candidate vs verified) and the operational instruction (verify vs apply).
This module separates them, adds a programmer-written control, and randomizes
condition order per task.

Conditions (10):
- clone
- correct x {candidate, verified} x {verify, apply}
- placebo x {candidate, verified} x {verify, apply}
- written_verified_apply (same program, attributed to a programmer, no prior
  learning session)
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from .v7_transfer import (
    MOTIF,
    PLACEBO,
    SESSION1_SCHEMA,
    SESSION2_SCHEMA,
    extra_examples,
    run_codex,
    session1_prompt,
    session2_prompt,
    transfer_tasks,
    verify,
)
from .v3_tasks import apply_program

CONDITIONS = [
    "clone",
    "correct_candidate_verify",
    "correct_candidate_apply",
    "correct_verified_verify",
    "correct_verified_apply",
    "placebo_candidate_verify",
    "placebo_candidate_apply",
    "placebo_verified_verify",
    "placebo_verified_apply",
    "written_verified_apply",
]

# condition -> (status, instruction, content) or None for clone
SPECS = {
    "clone": None,
    "correct_candidate_verify": ("candidate", "verify", "correct"),
    "correct_candidate_apply": ("candidate", "apply", "correct"),
    "correct_verified_verify": ("verified", "verify", "correct"),
    "correct_verified_apply": ("verified", "apply", "correct"),
    "placebo_candidate_verify": ("candidate", "verify", "placebo"),
    "placebo_candidate_apply": ("candidate", "apply", "placebo"),
    "placebo_verified_verify": ("verified", "verify", "placebo"),
    "placebo_verified_apply": ("verified", "apply", "placebo"),
    "written_verified_apply": ("written", "apply", "correct"),
}


def extra_for(status: str, instruction: str, program: str) -> str:
    if status == "candidate":
        text = f"Una subrutina candidata de experiencias anteriores es: {program}."
    elif status == "verified":
        text = f"Un programa retenido y verificado es: {program}."
    elif status == "written":
        text = f"Un programador escribió y verificó este programa: {program}."
    else:
        raise ValueError(status)
    if instruction == "verify":
        text += (
            " Antes de usarlo, verifica que encaje con los ejemplos; "
            "el programa completo puede tener más pasos."
        )
    elif instruction == "apply":
        text += " Aplícalo a la entrada."
    else:
        raise ValueError(instruction)
    return f"\n{text}\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--support", type=int, default=2)
    parser.add_argument("--session1-examples", type=int, default=12)
    parser.add_argument("--exact-ops", action="store_true")
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--out", default="mem-005.json")
    args = parser.parse_args()

    learned = run_codex(
        session1_prompt(args.session1_examples, args.exact_ops, MOTIF),
        SESSION1_SCHEMA,
        args.model,
        args.effort,
        args.timeout,
    )
    program = (learned["payload"] or {}).get("program")
    verified = verify(program, MOTIF)
    print(
        f"session1 program={program} verified={verified} seconds={learned['seconds']}"
    )
    if not verified:
        payload = {
            "model": args.model,
            "effort": args.effort,
            "seed": args.seed,
            "n": args.n,
            "session1": {"program": program, "verified": False},
            "error": "artifact not verified; experiment aborted",
            "rows": [],
        }
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print("artifact not verified; aborting")
        return

    learned_program = " -> ".join(program)
    written_program = " -> ".join(MOTIF)
    placebo_program = " -> ".join(PLACEBO)
    tasks = transfer_tasks(args.seed, args.n, 0, MOTIF)
    order_rng = random.Random(f"mem005-order:{args.seed}")
    rows = []
    for index, task in enumerate(tasks):
        order = list(CONDITIONS)
        order_rng.shuffle(order)
        for position, condition in enumerate(order):
            spec = SPECS[condition]
            if condition == "clone":
                extra = (
                    "\nNo hay subrutinas de experiencias anteriores disponibles; "
                    "usa únicamente los ejemplos de la tarea actual.\n"
                )
            else:
                status, instruction, content = spec
                chosen = {
                    "correct": learned_program,
                    "placebo": placebo_program,
                }[content]
                if status == "written":
                    chosen = written_program
                extra = extra_for(status, instruction, chosen)
            prompt = session2_prompt(task, extra, args.support)
            result = run_codex(
                prompt,
                SESSION2_SCHEMA,
                args.model,
                args.effort,
                args.timeout,
            )
            expected = list(
                apply_program(task.solution.program, task.observation.query)
            )
            answer = (result["payload"] or {}).get("query_output")
            ok = answer == expected
            rows.append(
                {
                    "condition": condition,
                    "index": index,
                    "order": position,
                    "program": list(task.solution.program),
                    "expected": expected,
                    "answer": answer,
                    "correct": ok,
                    "prompt_chars": len(prompt),
                    "seconds": result["seconds"],
                    "timed_out": result["timed_out"],
                }
            )
            print(
                f"{condition:<26} [{index + 1}/{args.n}] "
                f"{'OK ' if ok else 'FAIL'} {result['seconds']}s"
            )

    summary = {
        "model": args.model,
        "effort": args.effort,
        "seed": args.seed,
        "n": args.n,
        "support": args.support,
        "session1": {
            "program": program,
            "verified": True,
            "seconds": learned["seconds"],
        },
        "programs": {
            "learned": learned_program,
            "written": written_program,
            "placebo": placebo_program,
        },
        "conditions": {
            condition: {
                "correct": sum(
                    1
                    for row in rows
                    if row["condition"] == condition and row["correct"]
                ),
                "n": args.n,
                "accuracy": round(
                    sum(
                        1
                        for row in rows
                        if row["condition"] == condition and row["correct"]
                    )
                    / args.n,
                    4,
                ),
            }
            for condition in CONDITIONS
        },
        "rows": rows,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["conditions"], indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
