"""LIRE-001: the same rule, five representations, real token counts.

The rule has a condition and an exception, so fidelity matters:

    if the list has duplicates: sort ascending
    else: reverse and add 1 to each element

Representations: Spanish prose, English prose, Chinese prose, concise Spanish,
and a compact symbolic DSL. The instruction is identical (English) in every
condition; only the rule changes. Real token usage comes from Codex's `--json`
events, not from character counts.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

SCHEMA = {
    "type": "object",
    "properties": {"query_output": {"type": "array", "items": {"type": "integer"}}},
    "required": ["query_output"],
    "additionalProperties": False,
}

INSTRUCTION = "Apply the rule to the case. Return only the resulting list."

RULES = {
    "es": (
        "Regla: 1) Si la lista tiene duplicados y su primer elemento es par, "
        "ordénala de menor a mayor y suma 1 a cada elemento. "
        "2) Si tiene duplicados y el primero es impar, ordénala de mayor a menor. "
        "3) Si no tiene duplicados y el último elemento es negativo, invierte el "
        "orden y duplica cada elemento. "
        "4) En cualquier otro caso, invierte el orden, suma 1 a cada elemento y "
        "elimina el último."
    ),
    "en": (
        "Rule: 1) If the list has duplicates and its first element is even, sort it "
        "ascending and add 1 to each element. "
        "2) If it has duplicates and the first element is odd, sort it descending. "
        "3) If it has no duplicates and the last element is negative, reverse the "
        "order and double each element. "
        "4) Otherwise, reverse the order, add 1 to each element and drop the last."
    ),
    "zh": (
        "规则：1) 如果列表有重复元素且第一个元素为偶数，按从小到大排序并将每个元素加 1。"
        "2) 如果有重复元素且第一个元素为奇数，按从大到小排序。"
        "3) 如果没有重复元素且最后一个元素为负数，反转顺序并将每个元素乘以 2。"
        "4) 其他情况：反转顺序，将每个元素加 1，并删除最后一个元素。"
    ),
    "es_concise": (
        "Dup + 1.º par → orden asc +1. Dup + 1.º impar → orden desc. "
        "Sin dup + último < 0 → invertir y ×2. Otro → invertir, +1, quitar último."
    ),
    "dsl": (
        "IF has_duplicates(x) AND even(x[0]): ADD1(SORT_ASC(x))\n"
        "ELIF has_duplicates(x) AND odd(x[0]): SORT_DESC(x)\n"
        "ELIF NOT has_duplicates(x) AND x[-1] < 0: DOUBLE(REVERSE(x))\n"
        "ELSE: DROP_LAST(ADD1(REVERSE(x)))"
    ),
}

CASES = (
    [4, 1, 4, 2],
    [2, 9, 2, 5],
    [3, 1, 3, 7],
    [5, 5, 2, 8],
    [7, 2, 0, -1],
    [9, 4, 1, -3],
    [8, 3, 6, 2],
    [1, 0, 5, 4],
)


def expected(case: list[int]) -> list[int]:
    duplicates = len(set(case)) < len(case)
    if duplicates and case[0] % 2 == 0:
        return [value + 1 for value in sorted(case)]
    if duplicates and case[0] % 2 == 1:
        return sorted(case, reverse=True)
    if not duplicates and case[-1] < 0:
        return [value * 2 for value in reversed(case)]
    return [value + 1 for value in reversed(case)][:-1]


def prompt_for(rule: str, case: list[int]) -> str:
    return f"{rule}\n\nCase: {case}\n\n{INSTRUCTION}"


def run_codex(
    prompt: str,
    model: str,
    effort: str,
    timeout: int,
    schema: dict | None = None,
    answer_key: str = "query_output",
) -> dict:
    workdir = Path(tempfile.mkdtemp(prefix="lire-"))
    schema_path = workdir / "schema.json"
    schema_path.write_text(json.dumps(schema or SCHEMA), encoding="utf-8")
    out_path = workdir / "last.json"
    command = (
        "codex exec --ephemeral --skip-git-repo-check -s read-only --color never "
        f'-m {model} -c model_reasoning_effort="{effort}" '
        f'--output-schema "{schema_path}" -o "{out_path}" --json -'
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
    seconds = round(time.perf_counter() - started, 2)
    usage = {}
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed":
            usage = event.get("usage") or {}
    raw = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, AttributeError):
        payload = None
    answer = payload.get(answer_key) if isinstance(payload, dict) else None
    return {
        "answer": answer,
        "payload": payload,
        "parsed": answer is not None,
        "usage": usage,
        "timed_out": timed_out,
        "seconds": seconds,
        "returncode": process.returncode,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--out", default="lire-001.json")
    args = parser.parse_args()

    cases = CASES[: args.limit] if args.limit else CASES
    rows = []
    for name, rule in RULES.items():
        for index, case in enumerate(cases):
            result = run_codex(
                prompt_for(rule, case), args.model, args.effort, args.timeout
            )
            want = expected(case)
            ok = result["answer"] == want
            usage = result["usage"]
            rows.append(
                {
                    "representation": name,
                    "case": case,
                    "expected": want,
                    "answer": result["answer"],
                    "correct": ok,
                    "chars": len(rule),
                    "bytes": len(rule.encode("utf-8")),
                    "words": len(rule.split()),
                    "input_tokens": usage.get("input_tokens"),
                    "cached_tokens": usage.get("cached_input_tokens"),
                    "output_tokens": usage.get("output_tokens"),
                    "reasoning_tokens": usage.get("reasoning_output_tokens"),
                    "seconds": result["seconds"],
                }
            )
            print(
                f"{name:<11} [{index + 1}/{len(cases)}] {'OK ' if ok else 'FAIL'} "
                f"in={usage.get('input_tokens')} out={usage.get('output_tokens')} "
                f"{result['seconds']}s"
            )

    summary = {}
    for name in RULES:
        selected = [r for r in rows if r["representation"] == name]
        correct = sum(1 for r in selected if r["correct"])
        summary[name] = {
            "correct": correct,
            "n": len(selected),
            "accuracy": round(correct / len(selected), 4),
            "chars": selected[0]["chars"],
            "bytes": selected[0]["bytes"],
            "words": selected[0]["words"],
            "mean_input_tokens": round(
                sum(r["input_tokens"] or 0 for r in selected) / len(selected), 1
            ),
            "mean_output_tokens": round(
                sum(r["output_tokens"] or 0 for r in selected) / len(selected), 1
            ),
            "mean_seconds": round(
                sum(r["seconds"] for r in selected) / len(selected), 2
            ),
        }
    payload = {
        "model": args.model,
        "effort": args.effort,
        "n_cases": len(cases),
        "rules": RULES,
        "summary": summary,
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
