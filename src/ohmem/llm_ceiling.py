"""External ceiling test: can a frozen LLM agent solve our synthetic tasks?

Conditions (one call per task, no history between calls):

- `base`          three support examples.
- `more_examples` six support examples: tests whether the failure is information.
- `vocabulary`    three examples plus the operation language: tests representation.
- `retrieved`     three examples plus one previously solved task with the same
                  transformation and different numbers: tests retrieval memory.

Usage (PowerShell):
    $env:PYTHONPATH="src"
    python -m ohmem.llm_ceiling --condition retrieved --n 24 --out out.json
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import tempfile
import time
from pathlib import Path

from .v3_tasks import Task, apply_program, make_depth3_grid, make_task

SCHEMA = {
    "type": "object",
    "properties": {"query_output": {"type": "array", "items": {"type": "integer"}}},
    "required": ["query_output"],
    "additionalProperties": False,
}

VOCABULARY = (
    "Las transformaciones posibles son, en cualquier orden y de 1 a 3 pasos: "
    "ordenar ascendente, ordenar descendente, sumar 1 a cada elemento, "
    "duplicar cada elemento."
)

PROMPT = """Resuelve esta tarea de síntesis por ejemplos.

Tienes pares entrada -> salida. Infiere la transformación y aplícala a la entrada
final. No uses herramientas, ni el sistema de archivos, ni ejecutes código:
razona y responde.

{examples}
{extra}
Entrada a transformar: {query}

Responde solo con la lista de enteros resultante."""


def extra_examples(task: Task, k: int) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    rng = random.Random(f"extra:{task.observation.id}")
    pairs = []
    for _ in range(k):
        x = tuple(rng.randint(1, 9) for _ in range(4))
        pairs.append((x, apply_program(task.solution.program, x)))
    return pairs


def prompt_for(task: Task, condition: str, memory: Task | None = None) -> str:
    obs = task.observation
    pairs = list(zip(obs.support_inputs, obs.support_outputs))
    if condition == "more_examples":
        pairs = pairs + extra_examples(task, 3)
    examples = "\n".join(f"{list(x)} -> {list(y)}" for x, y in pairs)
    extra = ""
    if condition == "vocabulary":
        extra = "\n" + VOCABULARY + "\n"
    elif condition == "retrieved" and memory is not None:
        mem_pairs = "\n".join(
            f"{list(x)} -> {list(y)}"
            for x, y in zip(
                memory.observation.support_inputs, memory.observation.support_outputs
            )
        )
        mem_answer = list(
            apply_program(memory.solution.program, memory.observation.query)
        )
        extra = (
            "\nUna tarea parecida ya resuelta (misma transformación, otros números):\n"
            f"{mem_pairs}\n"
            f"Su entrada era {list(memory.observation.query)} "
            f"y su respuesta correcta fue {mem_answer}.\n"
        )
    return PROMPT.format(examples=examples, extra=extra, query=list(obs.query))


def run_codex(
    prompt: str, workdir: Path, model: str, effort: str, timeout: int
) -> dict:
    schema_path = workdir / "schema.json"
    schema_path.write_text(json.dumps(SCHEMA), encoding="utf-8")
    out_path = workdir / "last.json"
    if out_path.exists():
        out_path.unlink()
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
    elapsed = time.perf_counter() - started
    raw = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    answer = None
    try:
        answer = json.loads(raw)["query_output"]
    except (json.JSONDecodeError, KeyError, TypeError):
        answer = None
    return {
        "answer": answer,
        "parsed": answer is not None,
        "raw": raw,
        "stderr_tail": (completed.stderr or "")[-600:],
        "returncode": completed.returncode,
        "seconds": round(elapsed, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=24)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--condition",
        default="base",
        choices=("base", "more_examples", "vocabulary", "retrieved"),
    )
    parser.add_argument("--model", default="gpt-6-luna")
    parser.add_argument("--effort", default="low")
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--out", default="llm-ceiling.json")
    args = parser.parse_args()

    tasks = make_depth3_grid(args.seed)[: args.n]
    workdir = Path(tempfile.mkdtemp(prefix="llm-ceiling-"))
    rows = []
    correct = 0
    for index, task in enumerate(tasks):
        memory = None
        if args.condition == "retrieved":
            memory = make_task(900, "delta", 7000 + index, task.solution.program, "mem")
        result = run_codex(
            prompt_for(task, args.condition, memory),
            workdir,
            args.model,
            args.effort,
            args.timeout,
        )
        expected = list(apply_program(task.solution.program, task.observation.query))
        ok = result["answer"] == expected
        correct += ok
        rows.append(
            {
                "index": index,
                "condition": args.condition,
                "program": list(task.solution.program),
                "query": list(task.observation.query),
                "expected": expected,
                "answer": result["answer"],
                "parsed": result["parsed"],
                "correct": ok,
                "seconds": result["seconds"],
                "returncode": result["returncode"],
                "raw": result["raw"],
                "stderr_tail": result["stderr_tail"],
            }
        )
        print(
            f"[{index + 1}/{len(tasks)}] {'OK ' if ok else 'FAIL'} "
            f"{result['seconds']:>6.2f}s program={task.solution.program} "
            f"answer={result['answer']} expected={expected}"
        )

    payload = {
        "model": args.model,
        "effort": args.effort,
        "condition": args.condition,
        "n": len(tasks),
        "correct": correct,
        "parsed": sum(1 for r in rows if r["parsed"]),
        "accuracy": round(correct / len(tasks), 4),
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"accuracy={payload['accuracy']} parsed={payload['parsed']} -> {args.out}")


if __name__ == "__main__":
    main()
