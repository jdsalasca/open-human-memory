"""LIRE-001b: a long skill, five representations, real token counts.

120 rules, one per code, each with a threshold. Six cases: three satisfy the
rule, three do not and must return NONE. The skill is long enough that the
representation cost should be visible above the Codex harness overhead
(~26k tokens). We report the **minimum** input_tokens per representation, which
is the cleanest harness path; medians are reported too.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .lire_001 import run_codex

SCHEMA = {
    "type": "object",
    "properties": {"status": {"type": "string"}},
    "required": ["status"],
    "additionalProperties": False,
}

N_RULES = 120
CODES = [3, 27, 51, 78, 99, 117]
CASES = [
    (3, 2),  # satisfies -> S003
    (27, 20),  # satisfies -> S027
    (99, 90),  # satisfies -> S099
    (15, 10),  # satisfies -> S015
    (64, 60),  # satisfies -> S064
    (110, 100),  # satisfies -> S110
    (51, 60),  # does not satisfy -> NONE
    (78, 90),  # does not satisfy -> NONE
    (117, 120),  # does not satisfy -> NONE
    (40, 50),  # does not satisfy -> NONE
    (88, 95),  # does not satisfy -> NONE
    (105, 110),  # does not satisfy -> NONE
]

HEADER = {
    "es": "Habilidad: cada regla aplica a un código. Si el importe es menor que el umbral, devuelve el estado; si no, la regla no aplica.",
    "en": "Skill: each rule applies to one code. If the amount is less than the threshold, return the status; otherwise the rule does not apply.",
    "zh": "技能：每条规则对应一个代码。如果金额小于阈值，返回状态；否则该规则不适用。",
    "es_concise": "Reglas: código & importe<umbral → estado.",
    "dsl": "RULES: code, threshold -> status",
}

LINES = {
    "es": "Regla {i}: si el código es C{i:03d} y el importe es menor que {i}, devuelve S{i:03d}.",
    "en": "Rule {i}: if the code is C{i:03d} and the amount is less than {i}, return S{i:03d}.",
    "zh": "规则 {i}：如果代码为 C{i:03d} 且金额小于 {i}，返回 S{i:03d}。",
    "es_concise": "C{i:03d} & importe<{i} → S{i:03d}",
    "dsl": "IF code==C{i:03d} AND amount<{i}: RETURN S{i:03d}",
}

INSTRUCTION = (
    "Apply the skill to the case. If no rule applies, return NONE. "
    "Return only the status."
)


def skill_for(representation: str) -> str:
    template = LINES[representation]
    body = "\n".join(template.format(i=i) for i in range(N_RULES))
    return f"{HEADER[representation]}\n\n{body}"


def expected(code: int, amount: int) -> str:
    return f"S{code:03d}" if amount < code else "NONE"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--out", default="lire-001b.json")
    args = parser.parse_args()

    cases = CASES[: args.limit] if args.limit else CASES
    rows = []
    for representation in LINES:
        skill = skill_for(representation)
        for code, amount in cases:
            prompt = (
                f"{skill}\n\nCase: code C{code:03d}, amount {amount}.\n\n{INSTRUCTION}"
            )
            result = run_codex(
                prompt,
                args.model,
                args.effort,
                args.timeout,
                schema=SCHEMA,
                answer_key="status",
            )
            answer = result["answer"]
            want = expected(code, amount)
            usage = result["usage"]
            rows.append(
                {
                    "representation": representation,
                    "code": code,
                    "amount": amount,
                    "expected": want,
                    "answer": answer,
                    "correct": answer == want,
                    "chars": len(skill),
                    "bytes": len(skill.encode("utf-8")),
                    "input_tokens": usage.get("input_tokens"),
                    "output_tokens": usage.get("output_tokens"),
                    "seconds": result["seconds"],
                }
            )
            print(
                f"{representation:<11} C{code:03d} {'OK ' if answer == want else 'FAIL'} "
                f"in={usage.get('input_tokens')} got={answer} want={want} {result['seconds']}s"
            )

    summary = {}
    for representation in LINES:
        selected = [r for r in rows if r["representation"] == representation]
        tokens = sorted(r["input_tokens"] for r in selected if r["input_tokens"])
        summary[representation] = {
            "correct": sum(1 for r in selected if r["correct"]),
            "n": len(selected),
            "accuracy": round(
                sum(1 for r in selected if r["correct"]) / len(selected), 4
            ),
            "chars": selected[0]["chars"],
            "bytes": selected[0]["bytes"],
            "min_input_tokens": tokens[0] if tokens else None,
            "median_input_tokens": (tokens[len(tokens) // 2] if tokens else None),
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
        "n_rules": N_RULES,
        "cases": cases,
        "summary": summary,
        "rows": rows,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
