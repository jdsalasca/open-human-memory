"""Factorial analysis of MEM-005 (no LLM calls)."""

from __future__ import annotations

import json
import math
from pathlib import Path

from ohmem.mem_005 import CONDITIONS, SPECS

HERE = Path(__file__).resolve().parent
DATA = HERE / "results" / "factorial-seed1.json"


def sign_p(k: int, n: int) -> float | None:
    if n == 0:
        return None
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(k, n - k) + 1)) / 2**n)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rows = data["rows"]
    by = {
        condition: {row["index"]: row for row in rows if row["condition"] == condition}
        for condition in CONDITIONS
    }
    print("acierto:")
    for condition in CONDITIONS:
        selected = by[condition]
        correct = sum(1 for row in selected.values() if row["correct"])
        print(f"  {condition:<26} {correct}/{len(selected)}")

    print("\nfactorial (correcto / placebo):")
    for status in ("candidate", "verified"):
        for instruction in ("verify", "apply"):
            correct_key = next(
                c
                for c, spec in SPECS.items()
                if spec == (status, instruction, "correct")
            )
            placebo_key = next(
                c
                for c, spec in SPECS.items()
                if spec == (status, instruction, "placebo")
            )
            print(
                f"  {status:<9} {instruction:<5} "
                f"correct={sum(1 for r in by[correct_key].values() if r['correct'])} "
                f"placebo={sum(1 for r in by[placebo_key].values() if r['correct'])}"
            )

    print("\npares clave:")
    pairs = [
        ("correct_verified_apply", "placebo_verified_apply"),
        ("correct_verified_apply", "correct_candidate_apply"),
        ("correct_verified_apply", "correct_verified_verify"),
        ("correct_verified_apply", "written_verified_apply"),
        ("correct_verified_apply", "clone"),
        ("correct_candidate_verify", "placebo_candidate_verify"),
    ]
    for a, b in pairs:
        indexes = sorted(set(by[a]) & set(by[b]))
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
            f"p={p if p is not None else 'n/a'}"
        )


if __name__ == "__main__":
    main()
