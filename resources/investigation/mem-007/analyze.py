"""MEM-007 analysis: applicability and rejection (no LLM calls)."""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "results" / "pilot-seed1-corrected.json"
CONDITIONS = ["clone", "skill_no_meta", "skill_meta", "symbolic_solver"]


def sign_p(k: int, n: int) -> float | None:
    if n == 0:
        return None
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(k, n - k) + 1)) / 2**n)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rows = data["rows"]
    by = {
        condition: {
            row["task_index"]: row for row in rows if row["condition"] == condition
        }
        for condition in CONDITIONS
    }
    print("acierto (total / aplicables / inaplicables):")
    for condition in CONDITIONS:
        selected = by[condition]
        total = sum(1 for row in selected.values() if row["correct"])
        applicable = [row for row in selected.values() if row["applicable"]]
        inapplicable = [row for row in selected.values() if not row["applicable"]]
        print(
            f"  {condition:<16} {total}/{len(selected)}  "
            f"{sum(1 for row in applicable if row['correct'])}/{len(applicable)}  "
            f"{sum(1 for row in inapplicable if row['correct'])}/{len(inapplicable)}"
        )

    print("\nfalsos positivos en inaplicables (status APPLY):")
    for condition in CONDITIONS:
        selected = [row for row in by[condition].values() if not row["applicable"]]
        false_apply = sum(1 for row in selected if row["status"] == "APPLY")
        print(f"  {condition:<16} {false_apply}/{len(selected)}")

    print("\npares (solo inaplicables salvo indicación):")
    pairs = [
        ("skill_meta", "skill_no_meta"),
        ("skill_meta", "clone"),
        ("skill_meta", "symbolic_solver"),
        ("skill_no_meta", "clone"),
    ]
    for a, b in pairs:
        indexes = [
            index
            for index in sorted(set(by[a]) & set(by[b]))
            if not by[a][index]["applicable"]
        ]
        a_only = sum(
            1
            for index in indexes
            if by[a][index]["correct"] and not by[b][index]["correct"]
        )
        b_only = sum(
            1
            for index in indexes
            if by[b][index]["correct"] and not by[a][index]["correct"]
        )
        p = sign_p(a_only, a_only + b_only)
        print(
            f"  {a} vs {b}: {a}_only={a_only} {b}_only={b_only} "
            f"n={len(indexes)} p={p if p is not None else 'n/a'}"
        )

    print("\naplicables (skill_meta vs skill_no_meta):")
    indexes = [
        index
        for index in sorted(set(by["skill_meta"]) & set(by["skill_no_meta"]))
        if by["skill_meta"][index]["applicable"]
    ]
    a_only = sum(
        1
        for index in indexes
        if by["skill_meta"][index]["correct"]
        and not by["skill_no_meta"][index]["correct"]
    )
    b_only = sum(
        1
        for index in indexes
        if by["skill_no_meta"][index]["correct"]
        and not by["skill_meta"][index]["correct"]
    )
    print(f"  meta_only={a_only} no_meta_only={b_only} n={len(indexes)}")

    print("\ntokens de entrada (mediana):")
    for condition in CONDITIONS:
        values = [
            row["input_tokens"]
            for row in by[condition].values()
            if row.get("input_tokens")
        ]
        if values:
            print(f"  {condition:<16} {statistics.median(values):.0f}")


if __name__ == "__main__":
    main()
