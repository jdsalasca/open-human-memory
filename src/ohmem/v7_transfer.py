"""Prototype 007: does a verified procedure survive a reset and transfer?

Session 1: the agent sees six examples of one two-step transformation and returns
the program. The program is verified by *us* on fresh inputs; the model's word is
not trusted.

Reset: every call is a new Codex session with no history.

Session 2: tasks are five steps: the learned motif followed by three random
operations. Three conditions, same model, same examples, same prompt length:

- `clone`   no artifact
- `memory`  the verified motif
- `placebo` a wrong motif of the same length

If `memory` beats `clone` and `placebo`, the retained procedure transfers. If it
only beats `clone`, the gain is extra context. If it ties both, no transfer.
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import tempfile
import time
from pathlib import Path

from .v3_tasks import PRIMITIVES, apply_program, make_task

OPS = PRIMITIVES + ("negate", "reverse")
MOTIF = ("sort_asc", "double")
PLACEBO = ("sort_desc", "double")


def _probe(index: int) -> tuple[int, ...]:
    rng = random.Random(f"v7probe:{index}")
    return tuple(rng.randint(-9, 9) for _ in range(4))


PROBES = tuple(_probe(i) for i in range(60))

SESSION1_SCHEMA = {
    "type": "object",
    "properties": {"program": {"type": "array", "items": {"type": "string"}}},
    "required": ["program"],
    "additionalProperties": False,
}
SESSION2_SCHEMA = {
    "type": "object",
    "properties": {"query_output": {"type": "array", "items": {"type": "integer"}}},
    "required": ["query_output"],
    "additionalProperties": False,
}

SESSION1_PROMPT = """Has resuelto tareas de transformación de listas. Cada fila es
un par entrada -> salida. Las operaciones disponibles son: {ops}.

{examples}

¿Qué programa de 1 a 4 operaciones reproduce todos los pares? Responde con la
secuencia de operaciones, sin explicación."""

SESSION2_PROMPT = """Resuelve esta tarea de transformación de listas. Las
operaciones disponibles son: {ops}.

{examples}
{extra}
Entrada a transformar: {query}

Responde solo con la lista de enteros resultante."""


def extra_examples(
    program, n: int, salt: str
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    rng = random.Random(f"v7:{salt}")
    return [
        (
            x := tuple(rng.randint(-9, 9) for _ in range(4)),
            apply_program(program, x),
        )
        for _ in range(n)
    ]


def session1_prompt() -> str:
    pairs = extra_examples(MOTIF, 6, "session1")
    examples = "\n".join(f"{list(x)} -> {list(y)}" for x, y in pairs)
    return SESSION1_PROMPT.format(ops=", ".join(OPS), examples=examples)


def session2_prompt(task, extra: str, support: int = 3) -> str:
    obs = task.observation
    examples = "\n".join(
        f"{list(x)} -> {list(y)}"
        for x, y in zip(obs.support_inputs[:support], obs.support_outputs[:support])
    )
    return SESSION2_PROMPT.format(
        ops=", ".join(OPS), examples=examples, extra=extra, query=list(obs.query)
    )


def run_codex(prompt: str, schema: dict, model: str, effort: str, timeout: int) -> dict:
    workdir = Path(tempfile.mkdtemp(prefix="ohmem-v7-"))
    schema_path = workdir / "schema.json"
    schema_path.write_text(json.dumps(schema), encoding="utf-8")
    out_path = workdir / "last.json"
    command = (
        "codex exec --ephemeral --skip-git-repo-check -s read-only "
        f'-m {model} -c model_reasoning_effort="{effort}" '
        f'--output-schema "{schema_path}" -o "{out_path}" -'
    )
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        input=prompt,
        text=True,
        encoding="utf-8",
        capture_output=True,
        timeout=timeout,
        cwd=str(workdir),
        shell=True,
    )
    raw = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    payload = None
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        payload = None
    return {
        "payload": payload,
        "raw": raw,
        "returncode": completed.returncode,
        "seconds": round(time.perf_counter() - started, 2),
    }


def verify(program: list[str] | None) -> bool:
    if not program:
        return False
    for probe in PROBES:
        if apply_program(tuple(program), probe) != apply_program(MOTIF, probe):
            return False
    return True


def transfer_tasks(seed: int, n: int, suffix: int = 3) -> list:
    rng = random.Random(f"v7tasks:{seed}")
    tasks = []
    for i in range(n):
        tail = tuple(rng.choice(OPS) for _ in range(suffix))
        program = MOTIF + tail
        tasks.append(make_task(seed, "delta", 30_000 + i, program, "transfer"))
    return tasks


def build_conditions(program: list[str] | None, verified: bool) -> dict[str, str]:
    """Only a verified artifact may be delivered. No fallback to the true motif."""
    if not verified or not program:
        raise ValueError("artifact not verified; refusing to deliver memory")
    artifact = " -> ".join(program)
    placebo = " -> ".join(PLACEBO)
    return {
        "clone": (
            "\nNo hay subrutinas de experiencias anteriores disponibles; "
            "usa únicamente los ejemplos de la tarea actual.\n"
        ),
        "memory": (
            "\nUna subrutina candidata de experiencias anteriores es: "
            f"{artifact}. Verifícala contra los ejemplos y úsala si encaja; "
            "el programa completo puede tener más pasos.\n"
        ),
        "placebo": (
            "\nUna subrutina candidata de experiencias anteriores es: "
            f"{placebo}. Verifícala contra los ejemplos y úsala si encaja; "
            "el programa completo puede tener más pasos.\n"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument("--suffix", type=int, default=3)
    parser.add_argument("--support", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--out", default="v7-transfer.json")
    args = parser.parse_args()

    # Session 1: learn and verify a procedure.
    learned = run_codex(
        session1_prompt(), SESSION1_SCHEMA, args.model, args.effort, args.timeout
    )
    program = (learned["payload"] or {}).get("program")
    verified = verify(program)
    print(
        f"session1 program={program} verified={verified} seconds={learned['seconds']}"
    )

    if not verified:
        summary = {
            "model": args.model,
            "effort": args.effort,
            "seed": args.seed,
            "n": args.n,
            "support": args.support,
            "suffix": args.suffix,
            "session1": {
                "program": program,
                "verified": False,
                "seconds": learned["seconds"],
            },
            "error": "artifact not verified; experiment aborted before session 2",
            "conditions": {},
            "rows": [],
        }
        Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print("artifact not verified; aborting before session 2")
        return

    tasks = transfer_tasks(args.seed, args.n, args.suffix)
    conditions = build_conditions(program, verified)
    rows = []
    for condition, extra in conditions.items():
        for index, task in enumerate(tasks):
            result = run_codex(
                session2_prompt(task, extra, args.support),
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
                    "program": list(task.solution.program),
                    "expected": expected,
                    "answer": answer,
                    "correct": ok,
                    "seconds": result["seconds"],
                    "returncode": result["returncode"],
                }
            )
            print(
                f"{condition:<8} [{index + 1}/{args.n}] {'OK ' if ok else 'FAIL'} {result['seconds']}s"
            )

    summary = {
        "model": args.model,
        "effort": args.effort,
        "seed": args.seed,
        "n": args.n,
        "support": args.support,
        "suffix": args.suffix,
        "session1": {
            "program": program,
            "verified": verified,
            "seconds": learned["seconds"],
        },
        "conditions": {
            condition: {
                "correct": sum(
                    1 for r in rows if r["condition"] == condition and r["correct"]
                ),
                "n": args.n,
                "accuracy": round(
                    sum(1 for r in rows if r["condition"] == condition and r["correct"])
                    / args.n,
                    4,
                ),
                "mean_seconds": round(
                    sum(r["seconds"] for r in rows if r["condition"] == condition)
                    / args.n,
                    1,
                ),
            }
            for condition in conditions
        },
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["conditions"], indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
