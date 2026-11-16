"""Paired analysis of MEM-002 (no LLM calls)."""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "results" / "pilot-depth3.json"
CONDITIONS = ["clone", "memory", "placebo", "history", "oracle"]


def sign_p(k: int, n: int) -> float | None:
    if n == 0:
        return None
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(k, n - k) + 1)) / 2**n)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rows = data["rows"]
    by_condition = {
        condition: {row["index"]: row for row in rows if row["condition"] == condition}
        for condition in CONDITIONS
    }
    print("acierto:")
    for condition in CONDITIONS:
        selected = by_condition[condition]
        correct = sum(1 for row in selected.values() if row["correct"])
        print(f"  {condition:<8} {correct}/{len(selected)}")

    print("pares:")
    for i, a in enumerate(CONDITIONS):
        for b in CONDITIONS[i + 1 :]:
            indexes = sorted(set(by_condition[a]) & set(by_condition[b]))
            a_only = sum(
                1
                for index in indexes
                if by_condition[a][index]["correct"]
                and not by_condition[b][index]["correct"]
            )
            b_only = sum(
                1
                for index in indexes
                if by_condition[b][index]["correct"]
                and not by_condition[a][index]["correct"]
            )
            p = sign_p(a_only, a_only + b_only)
            print(
                f"  {a} vs {b}: {a}_only={a_only} {b}_only={b_only} "
                f"p={p if p is not None else 'n/a'}"
            )

    print("prompt chars:")
    for condition in CONDITIONS:
        selected = by_condition[condition].values()
        print(
            f"  {condition:<8} "
            f"{sum(row.get('prompt_chars', 0) for row in selected) / len(selected):.0f}"
        )


if __name__ == "__main__":
    main()
