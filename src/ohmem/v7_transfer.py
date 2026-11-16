"""Prototype 007: does a verified procedure survive a reset and transfer?

Session 1: the agent sees examples of one transformation and returns the program.
The program is verified by *us* on fresh inputs; the model's word is not trusted.

Reset: every call is a new Codex session with no history.

Session 2: tasks are the learned motif followed by random operations. Conditions,
same model, same examples:

- `clone`   no artifact
- `memory`  the verified motif
- `placebo` a wrong motif of the same length
- `history` the session-1 examples (source experience)
- `oracle`  the full task program (leakage; execution control)

If `memory` beats `clone` and `placebo`, the retained procedure transfers. If it
only beats `clone`, the gain is extra context. If it ties both, no transfer.
"""

from __future__ import annotations

import argparse
import itertools
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
{hint}
¿Qué programa reproduce todos los pares? Responde con la secuencia de operaciones,
sin explicación."""

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


def session1_prompt(
    examples: int = 6, exact_ops: bool = False, motif: tuple[str, ...] = MOTIF
) -> str:
    pairs = extra_examples(motif, examples, "session1")
    rows = "\n".join(f"{list(x)} -> {list(y)}" for x, y in pairs)
    hint = (
        f"El programa tiene exactamente {len(motif)} operaciones." if exact_ops else ""
    )
    return SESSION1_PROMPT.format(ops=", ".join(OPS), examples=rows, hint=hint)


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
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        cwd=str(workdir),
        shell=True,
    )
    timed_out = False
    try:
        stdout, stderr = process.communicate(input=prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        # subprocess.run's timeout kills the shell but not the codex child that
        # keeps the pipes open; kill the whole tree.
        subprocess.run(
            ["taskkill", "/T", "/F", "/PID", str(process.pid)],
            capture_output=True,
            text=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
    raw = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    payload = None
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        payload = None
    return {
        "payload": payload,
        "raw": raw,
        "returncode": process.returncode,
        "timed_out": timed_out,
        "seconds": round(time.perf_counter() - started, 2),
    }


def verify(program: list[str] | None, motif: tuple[str, ...] = MOTIF) -> bool:
    if not program:
        return False
    for probe in PROBES:
        if apply_program(tuple(program), probe) != apply_program(motif, probe):
            return False
    return True


def wrong_program(motif: tuple[str, ...]) -> tuple[str, ...]:
    """A deterministic, non-reducible program of the same length."""
    rng = random.Random("v7placebo:" + ",".join(motif))
    shorter = {
        tuple(apply_program(candidate, probe) for probe in PROBES)
        for length in range(1, len(motif))
        for candidate in itertools.product(OPS, repeat=length)
    }
    while True:
        candidate = tuple(rng.choice(OPS) for _ in range(len(motif)))
        if any(candidate[i] == candidate[i + 1] for i in range(len(candidate) - 1)):
            continue
        signature = tuple(apply_program(candidate, probe) for probe in PROBES)
        if signature in shorter or verify(list(candidate), motif):
            continue
        return candidate


def transfer_tasks(
    seed: int, n: int, suffix: int = 3, motif: tuple[str, ...] = MOTIF
) -> list:
    rng = random.Random(f"v7tasks:{seed}")
    tasks = []
    for i in range(n):
        tail = tuple(rng.choice(OPS) for _ in range(suffix))
        program = motif + tail
        tasks.append(make_task(seed, "delta", 30_000 + i, program, "transfer"))
    return tasks


def build_conditions(
    program: list[str] | None,
    verified: bool,
    motif: tuple[str, ...] = MOTIF,
    placebo: tuple[str, ...] | None = None,
    history: list | None = None,
    include_oracle: bool = False,
    include_verified: bool = False,
) -> dict[str, str]:
    """Only a verified artifact may be delivered. No fallback to the true motif."""
    if not verified or not program:
        raise ValueError("artifact not verified; refusing to deliver memory")
    artifact = " -> ".join(program)
    placebo = placebo or (PLACEBO if motif == MOTIF else wrong_program(motif))
    conditions = {
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
            f"{' -> '.join(placebo)}. Verifícala contra los ejemplos y úsala si encaja; "
            "el programa completo puede tener más pasos.\n"
        ),
    }
    if include_verified:
        conditions["memory_verified"] = (
            "\nEl programa retenido y verificado es: "
            f"{artifact}. Aplícalo a la entrada.\n"
        )
        conditions["placebo_verified"] = (
            "\nEl programa retenido y verificado es: "
            f"{' -> '.join(placebo)}. Aplícalo a la entrada.\n"
        )
    if history is not None:
        rows = "\n".join(f"{list(x)} -> {list(y)}" for x, y in history)
        conditions["history"] = (
            "\nEstas son experiencias anteriores de la misma familia:\n"
            f"{rows}\nVerifícalas y usa lo que aprendiste si encaja; "
            "el programa completo puede tener más pasos.\n"
        )
    if include_oracle:
        conditions["oracle"] = (
            "\nEl programa completo de esta tarea es: {program}. "
            "Aplícalo a la entrada.\n"
        )
    return conditions


def write_json(path: str, data) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument("--suffix", type=int, default=3)
    parser.add_argument("--support", type=int, default=3)
    parser.add_argument("--session1-examples", type=int, default=6)
    parser.add_argument("--exact-ops", action="store_true")
    parser.add_argument("--session1-only", action="store_true")
    parser.add_argument("--motif", default=",".join(MOTIF))
    parser.add_argument("--placebo", default="")
    parser.add_argument("--conditions", default="clone,memory,placebo")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--out", default="v7-transfer.json")
    args = parser.parse_args()

    motif = tuple(x.strip() for x in args.motif.split(",") if x.strip())
    if not motif or any(op not in OPS for op in motif):
        parser.error(f"invalid motif: {args.motif}")
    placebo = tuple(x.strip() for x in args.placebo.split(",") if x.strip()) or None
    if placebo is not None and (
        len(placebo) != len(motif) or verify(list(placebo), motif)
    ):
        parser.error("placebo must have the same length and must not verify")
    selected = [x.strip() for x in args.conditions.split(",") if x.strip()]
    if not selected or any(
        c
        not in {
            "clone",
            "memory",
            "memory_verified",
            "placebo",
            "placebo_verified",
            "history",
            "oracle",
        }
        for c in selected
    ):
        parser.error(f"invalid conditions: {args.conditions}")

    # Session 1: learn and verify a procedure.
    learned = run_codex(
        session1_prompt(args.session1_examples, args.exact_ops, motif),
        SESSION1_SCHEMA,
        args.model,
        args.effort,
        args.timeout,
    )
    program = (learned["payload"] or {}).get("program")
    verified = verify(program, motif)
    print(
        f"session1 program={program} verified={verified} seconds={learned['seconds']}"
    )

    if args.session1_only:
        summary = {
            "model": args.model,
            "effort": args.effort,
            "motif": list(motif),
            "session1_examples": args.session1_examples,
            "exact_ops": args.exact_ops,
            "session1": {
                "program": program,
                "verified": verified,
                "timed_out": learned["timed_out"],
                "seconds": learned["seconds"],
            },
            "session1_only": True,
        }
        write_json(args.out, summary)
        print("session1 only")
        return

    if not verified:
        summary = {
            "model": args.model,
            "effort": args.effort,
            "seed": args.seed,
            "n": args.n,
            "support": args.support,
            "suffix": args.suffix,
            "motif": list(motif),
            "session1": {
                "program": program,
                "verified": False,
                "timed_out": learned["timed_out"],
                "seconds": learned["seconds"],
            },
            "error": "artifact not verified; experiment aborted before session 2",
            "conditions": {},
            "rows": [],
        }
        write_json(args.out, summary)
        print("artifact not verified; aborting before session 2")
        return

    tasks = transfer_tasks(args.seed, args.n, args.suffix, motif)
    history_pairs = (
        extra_examples(motif, args.session1_examples, "session1")
        if "history" in selected
        else None
    )
    conditions = build_conditions(
        program,
        verified,
        motif=motif,
        placebo=placebo,
        history=history_pairs,
        include_oracle="oracle" in selected,
        include_verified="memory_verified" in selected,
    )
    conditions = {k: v for k, v in conditions.items() if k in selected}
    rows = []
    for condition, extra in conditions.items():
        for index, task in enumerate(tasks):
            prompt_extra = (
                extra.format(program=" -> ".join(task.solution.program))
                if condition == "oracle"
                else extra
            )
            prompt = session2_prompt(task, prompt_extra, args.support)
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
                    "program": list(task.solution.program),
                    "expected": expected,
                    "answer": answer,
                    "correct": ok,
                    "prompt_chars": len(prompt),
                    "seconds": result["seconds"],
                    "returncode": result["returncode"],
                    "timed_out": result["timed_out"],
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
        "motif": list(motif),
        "placebo": list(
            placebo or (PLACEBO if motif == MOTIF else wrong_program(motif))
        ),
        "session1": {
            "program": program,
            "verified": verified,
            "timed_out": learned["timed_out"],
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
                "mean_prompt_chars": round(
                    sum(r["prompt_chars"] for r in rows if r["condition"] == condition)
                    / args.n
                ),
                "timeouts": sum(
                    1 for r in rows if r["condition"] == condition and r["timed_out"]
                ),
            }
            for condition in conditions
        },
        "rows": rows,
    }
    write_json(args.out, summary)
    print(json.dumps(summary["conditions"], indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
