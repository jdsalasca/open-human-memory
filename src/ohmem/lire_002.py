"""LIRE-002: independent-information table, seven representations, no-table control.

The previous LIRE-001b used 120 rules of the form C{i} / threshold {i} / S{i},
which one formula reconstructs. This experiment removes that redundancy:

- codes are random 4-character strings;
- thresholds are random and independent of the code;
- statuses are random labels, independent of both;
- 12 rules have an independent exception with priority;
- queries include positive, boundary, exception, negative and unknown-code cases.

The no-table control measures what the model can answer without the table. The
primary endpoint is the positive cases, which cannot be answered by an all-NONE
strategy. Token cost is the paired difference against the no-table call on the
same case, which cancels the Codex harness overhead.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from pathlib import Path

from .lire_001 import run_codex

SCHEMA = {
    "type": "object",
    "properties": {"status": {"type": "string"}},
    "required": ["status"],
    "additionalProperties": False,
}

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
LABELS = [
    "ALPHA",
    "BETA",
    "GAMMA",
    "DELTA",
    "EPSILON",
    "ZETA",
    "ETA",
    "THETA",
    "IOTA",
    "KAPPA",
    "LAMBDA",
    "MU",
]
N_RULES = 120
N_EXCEPTIONS = 12
REPRESENTATIONS = ["es", "en", "zh", "es_concise", "dsl", "json", "table"]
NO_TABLE = "none"

INSTRUCTION = (
    "CASE code={code} amount={amount}.\n"
    "If a rule applies, return its status. If no rule applies or the code is "
    "unknown, return NONE. Return only the status or NONE."
)


def make_rules(seed: int = 20261116) -> list[dict]:
    rng = random.Random(f"lire2rules:{seed}")
    codes: set[str] = set()
    while len(codes) < N_RULES:
        codes.add("".join(rng.choice(ALPHABET) for _ in range(4)))
    rules = []
    for code in sorted(codes):
        rules.append(
            {
                "code": code,
                "threshold": rng.randint(5, 99),
                "status": rng.choice(LABELS),
                "exception": None,
            }
        )
    for rule in rng.sample(rules, N_EXCEPTIONS):
        rule["exception"] = {
            "threshold": rng.randint(1, rule["threshold"] - 1),
            "status": rng.choice(
                [label for label in LABELS if label != rule["status"]]
            ),
        }
    return rules


def expected(rules: dict[str, dict], code: str, amount: int) -> str:
    rule = rules.get(code)
    if rule is None:
        return "NONE"
    exception = rule["exception"]
    if exception is not None and amount < exception["threshold"]:
        return exception["status"]
    if amount < rule["threshold"]:
        return rule["status"]
    return "NONE"


def make_cases(rules: list[dict], seed: int = 20261116) -> list[dict]:
    rng = random.Random(f"lire2cases:{seed}")
    plain = [rule for rule in rules if rule["exception"] is None]
    exceptional = [rule for rule in rules if rule["exception"] is not None]
    chosen = rng.sample(plain, 8)
    chosen_exc = rng.sample(exceptional, 2)
    by_code = {rule["code"]: rule for rule in rules}

    cases: list[dict] = []

    def add(kind: str, rule: dict, amount: int) -> None:
        cases.append(
            {
                "kind": kind,
                "code": rule["code"],
                "amount": amount,
                "expected": expected(by_code, rule["code"], amount),
                "primary": kind
                in {"positive", "positive_boundary", "positive_exception"},
            }
        )

    for rule in chosen[:4]:
        add("positive", rule, rng.randint(0, rule["threshold"] - 1))
    add("positive_boundary", chosen[4], chosen[4]["threshold"] - 1)
    for rule in chosen_exc:
        add(
            "positive_exception",
            rule,
            rng.randint(0, rule["exception"]["threshold"] - 1),
        )
    add("negative_boundary", chosen[5], chosen[5]["threshold"])
    for rule in chosen[6:8]:
        add("negative", rule, min(120, rule["threshold"] + rng.randint(1, 10)))

    used = set(by_code)
    for _ in range(2):
        while True:
            code = "".join(rng.choice(ALPHABET) for _ in range(4))
            if code not in used:
                used.add(code)
                break
        cases.append(
            {
                "kind": "unknown",
                "code": code,
                "amount": rng.randint(0, 120),
                "expected": "NONE",
                "primary": False,
            }
        )

    rng.shuffle(cases)
    return cases


def _line_es(rule: dict, index: int) -> str:
    exception = rule["exception"]
    text = (
        "sin excepción"
        if exception is None
        else (
            f"excepción: si el importe es menor que {exception['threshold']}, "
            f"devuelve {exception['status']}"
        )
    )
    return (
        f"Regla {index}: código {rule['code']}; umbral {rule['threshold']}; "
        f"estado {rule['status']}; {text}."
    )


def _line_en(rule: dict, index: int) -> str:
    exception = rule["exception"]
    text = (
        "no exception"
        if exception is None
        else (
            f"exception: if the amount is less than {exception['threshold']}, "
            f"return {exception['status']}"
        )
    )
    return (
        f"Rule {index}: code {rule['code']}; threshold {rule['threshold']}; "
        f"status {rule['status']}; {text}."
    )


def _line_zh(rule: dict, index: int) -> str:
    exception = rule["exception"]
    text = (
        "无例外"
        if exception is None
        else f"例外：如果金额小于 {exception['threshold']}，返回 {exception['status']}"
    )
    return (
        f"规则 {index}：代码 {rule['code']}；阈值 {rule['threshold']}；"
        f"状态 {rule['status']}；{text}。"
    )


HEADERS = {
    "es": (
        "Habilidad: cada regla tiene un código, un umbral y un estado. Algunas "
        "reglas tienen una excepción con prioridad. Si el importe es menor que el "
        "umbral de excepción, devuelve el estado de excepción; si no, si el importe "
        "es menor que el umbral, devuelve el estado; si no, la regla no aplica."
    ),
    "en": (
        "Skill: each rule has a code, a threshold and a status. Some rules have an "
        "exception with priority. If the amount is less than the exception "
        "threshold, return the exception status; otherwise, if the amount is less "
        "than the threshold, return the status; otherwise the rule does not apply."
    ),
    "zh": (
        "技能：每条规则有一个代码、一个阈值和一个状态。有些规则有一个优先的例外。"
        "如果金额小于例外阈值，返回例外状态；否则，如果金额小于阈值，返回状态；"
        "否则规则不适用。"
    ),
    "es_concise": (
        "Habilidad: tabla de reglas. La excepción tiene prioridad sobre el umbral."
    ),
    "dsl": "RULES (exception first):",
    "json": "RULES (JSON):",
    "table": "RULES (TSV): code\tthreshold\tstatus\texception_threshold\texception_status",
    NO_TABLE: "No rule table is provided.",
}


def build_skill(representation: str, rules: list[dict]) -> str:
    if representation in {"es", "en", "zh"}:
        builder = {"es": _line_es, "en": _line_en, "zh": _line_zh}[representation]
        body = "\n".join(
            builder(rule, index) for index, rule in enumerate(rules, start=1)
        )
        return f"{HEADERS[representation]}\n\n{body}"
    if representation == "es_concise":
        body = "\n".join(
            (
                f"{rule['code']} | <{rule['threshold']} | {rule['status']} | "
                + (
                    "—"
                    if rule["exception"] is None
                    else (
                        f"<{rule['exception']['threshold']}→"
                        f"{rule['exception']['status']}"
                    )
                )
            )
            for rule in rules
        )
        return f"{HEADERS['es_concise']}\n\n{body}"
    if representation == "dsl":
        lines = []
        for rule in rules:
            if rule["exception"] is not None:
                lines.append(
                    f'IF code == "{rule["code"]}" AND amount < '
                    f"{rule['exception']['threshold']}: "
                    f'RETURN "{rule["exception"]["status"]}"'
                )
            lines.append(
                f'IF code == "{rule["code"]}" AND amount < {rule["threshold"]}: '
                f'RETURN "{rule["status"]}"'
            )
        return f"{HEADERS['dsl']}\n" + "\n".join(lines)
    if representation == "json":
        payload = [
            {
                "code": rule["code"],
                "threshold": rule["threshold"],
                "status": rule["status"],
                "exception": rule["exception"],
            }
            for rule in rules
        ]
        return f"{HEADERS['json']}\n{json.dumps(payload, ensure_ascii=False, separators=(',', ':'))}"
    if representation == "table":
        body = "\n".join(
            (
                f"{rule['code']}\t{rule['threshold']}\t{rule['status']}\t"
                + (
                    "-\t-"
                    if rule["exception"] is None
                    else (
                        f"{rule['exception']['threshold']}\t"
                        f"{rule['exception']['status']}"
                    )
                )
            )
            for rule in rules
        )
        return f"{HEADERS['table']}\n{body}"
    if representation == NO_TABLE:
        return HEADERS[NO_TABLE]
    raise ValueError(f"unknown representation: {representation}")


def build_prompt(skill: str, case: dict) -> str:
    return f"{skill}\n\n{INSTRUCTION.format(code=case['code'], amount=case['amount'])}"


def table_bits(rules: list[dict]) -> int:
    per_rule = math.log2(len(ALPHABET) ** 4) + math.log2(99) + math.log2(len(LABELS))
    per_exception = 1 + math.log2(99) + math.log2(len(LABELS) - 1)
    return round(
        len(rules) * per_rule
        + sum(per_exception for rule in rules if rule["exception"] is not None)
    )


def sign_p(k: int, n: int) -> float | None:
    if n == 0:
        return None
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(k, n - k) + 1)) / 2**n)


def summarize(rows: list[dict], n_cases: int) -> dict:
    none_tokens = {
        row["case_index"]: row["input_tokens"]
        for row in rows
        if row["representation"] == NO_TABLE and row["input_tokens"]
    }
    summary = {}
    for representation in REPRESENTATIONS + [NO_TABLE]:
        selected = [row for row in rows if row["representation"] == representation]
        primary = [row for row in selected if row["primary"]]
        secondary = [row for row in selected if not row["primary"]]
        tokens = [row["input_tokens"] for row in selected if row["input_tokens"]]
        deltas = [
            row["input_tokens"] - none_tokens[row["case_index"]]
            for row in selected
            if row["input_tokens"] and row["case_index"] in none_tokens
        ]
        median_delta = statistics.median(deltas) if deltas else None
        primary_correct = sum(1 for row in primary if row["correct"])
        summary[representation] = {
            "correct": sum(1 for row in selected if row["correct"]),
            "n": len(selected),
            "accuracy": round(
                sum(1 for row in selected if row["correct"]) / len(selected), 4
            ),
            "primary_correct": primary_correct,
            "primary_n": len(primary),
            "primary_accuracy": (
                round(primary_correct / len(primary), 4) if primary else None
            ),
            "secondary_correct": sum(1 for row in secondary if row["correct"]),
            "secondary_n": len(secondary),
            "secondary_accuracy": (
                round(sum(1 for row in secondary if row["correct"]) / len(secondary), 4)
                if secondary
                else None
            ),
            "chars": selected[0]["chars"],
            "bytes": selected[0]["bytes"],
            "min_input_tokens": min(tokens) if tokens else None,
            "median_input_tokens": (statistics.median(tokens) if tokens else None),
            "median_incremental_tokens": median_delta,
            "min_incremental_tokens": min(deltas) if deltas else None,
            "primary_correct_per_1k_tokens": (
                round(1000 * primary_correct / len(primary) / median_delta, 2)
                if primary and median_delta and median_delta > 0
                else None
            ),
            "mean_output_tokens": round(
                sum(row["output_tokens"] or 0 for row in selected) / len(selected), 1
            ),
            "mean_seconds": round(
                sum(row["seconds"] for row in selected) / len(selected), 2
            ),
            "timeouts": sum(1 for row in selected if row["timed_out"]),
        }

    by_case = {
        representation: {
            row["case_index"]: row["correct"]
            for row in rows
            if row["representation"] == representation
        }
        for representation in REPRESENTATIONS
    }
    none_by_case = {
        row["case_index"]: row["correct"]
        for row in rows
        if row["representation"] == NO_TABLE
    }
    for representation in REPRESENTATIONS:
        for base in ["es", NO_TABLE]:
            base_correct = by_case[base] if base != NO_TABLE else none_by_case
            indexes = sorted(set(by_case[representation]) & set(base_correct))
            a_only = sum(
                1
                for index in indexes
                if by_case[representation][index] and not base_correct[index]
            )
            b_only = sum(
                1
                for index in indexes
                if base_correct[index] and not by_case[representation][index]
            )
            summary[representation][f"vs_{base}"] = {
                "a_only": a_only,
                "b_only": b_only,
                "p": sign_p(a_only, a_only + b_only),
            }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gpt-6.1-terra")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--seed", type=int, default=20261116)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--out", default="lire-002.json")
    args = parser.parse_args()

    rules = make_rules(args.seed)
    by_code = {rule["code"]: rule for rule in rules}
    cases = make_cases(rules, args.seed)
    if args.limit:
        cases = cases[: args.limit]

    order_rng = random.Random(f"lire2order:{args.seed}")
    rows = []
    for case_index, case in enumerate(cases):
        order = REPRESENTATIONS + [NO_TABLE]
        order_rng.shuffle(order)
        for position, representation in enumerate(order):
            skill = build_skill(representation, rules)
            prompt = build_prompt(skill, case)
            result = run_codex(
                prompt,
                args.model,
                args.effort,
                args.timeout,
                schema=SCHEMA,
                answer_key="status",
            )
            answer = result["answer"]
            usage = result["usage"]
            rows.append(
                {
                    "representation": representation,
                    "case_index": case_index,
                    "kind": case["kind"],
                    "primary": case["primary"],
                    "code": case["code"],
                    "amount": case["amount"],
                    "expected": case["expected"],
                    "answer": answer,
                    "correct": answer == case["expected"],
                    "order": position,
                    "chars": len(skill),
                    "bytes": len(skill.encode("utf-8")),
                    "input_tokens": usage.get("input_tokens"),
                    "cached_tokens": usage.get("cached_input_tokens"),
                    "output_tokens": usage.get("output_tokens"),
                    "timed_out": result["timed_out"],
                    "seconds": result["seconds"],
                }
            )
            print(
                f"{representation:<11} [{case_index + 1}/{len(cases)}] "
                f"{'OK ' if answer == case['expected'] else 'FAIL'} "
                f"{case['kind']:<18} got={json.dumps(answer, ensure_ascii=True)} "
                f"want={case['expected']} in={usage.get('input_tokens')} "
                f"{result['seconds']}s"
            )

    summary = summarize(rows, len(cases))
    payload = {
        "model": args.model,
        "effort": args.effort,
        "seed": args.seed,
        "n_rules": N_RULES,
        "n_exceptions": N_EXCEPTIONS,
        "table_bits": table_bits(rules),
        "cases": cases,
        "rules": rules,
        "summary": summary,
        "rows": rows,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
