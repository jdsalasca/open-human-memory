"""External ceiling test: can a frozen LLM agent solve our synthetic tasks?

No history, no library, no retries: three input/output examples and one query.
If this agent solves the whole grid, the benchmark cannot discriminate memory
mechanisms, whatever our solvers do.

Usage (PowerShell):
    $env:PYTHONPATH="src"
    python -m ohmem.llm_ceiling --n 2 --out scratch.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

from .v3_tasks import Task, apply_program, make_depth3_grid

SCHEMA = {
    "type": "object",
    "properties": {"query_output": {"type": "array", "items": {"type": "integer"}}},
    "required": ["query_output"],
    "additionalProperties": False,
}

PROMPT = """Resuelve esta tarea de síntesis por ejemplos.

Tienes tres pares entrada -> salida. Infiere la transformación y aplícala a la
entrada final. No uses herramientas, ni el sistema de archivos, ni ejecutes
código: razona y responde.

{examples}

Entrada a transformar: {query}

Responde solo con la lista de enteros resultante."""


def prompt_for(task: Task) -> str:
    obs = task.observation
    examples = "\n".join(
        f"{list(x)} -> {list(y)}"
        for x, y in zip(obs.support_inputs, obs.support_outputs)
    )
    return PROMPT.format(examples=examples, query=list(obs.query))


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
        "raw": raw,
        "stderr_tail": (completed.stderr or "")[-600:],
        "returncode": completed.returncode,
        "seconds": round(elapsed, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
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
        result = run_codex(
            prompt_for(task), workdir, args.model, args.effort, args.timeout
        )
        expected = list(apply_program(task.solution.program, task.observation.query))
        ok = result["answer"] == expected
        correct += ok
        rows.append(
            {
                "index": index,
                "program": list(task.solution.program),
                "query": list(task.observation.query),
                "expected": expected,
                "answer": result["answer"],
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
        "n": len(tasks),
        "correct": correct,
        "accuracy": round(correct / len(tasks), 4),
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"accuracy={payload['accuracy']} -> {args.out}")


if __name__ == "__main__":
    main()
