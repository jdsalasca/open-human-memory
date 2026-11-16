"""Combine 007 support-2 rows with 007B history/oracle rows (no LLM calls)."""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = (
    HERE.parent
    / "prototipo-007-transferencia"
    / "results"
    / "luna-low-support2-12ex.json"
)
NEW = HERE / "results" / "luna-low-support2-history-oracle.json"
CONDITIONS = ["clone", "memory", "placebo", "history", "oracle"]


def sign_p(k: int, n: int) -> float | None:
    if n == 0:
        return None
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(k, n - k) + 1)) / 2**n)


def main() -> None:
    rows: dict[str, dict[int, dict]] = {}
    for path in (BASE, NEW):
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data["rows"]:
            rows.setdefault(row["condition"], {})[row["index"]] = row

    print("acierto:")
    for condition in CONDITIONS:
        if condition not in rows:
            continue
        correct = sum(1 for row in rows[condition].values() if row["correct"])
        print(f"  {condition:<8} {correct}/{len(rows[condition])}")

    print("pares:")
    for i, a in enumerate(CONDITIONS):
        for b in CONDITIONS[i + 1 :]:
            if a not in rows or b not in rows:
                continue
            indexes = sorted(set(rows[a]) & set(rows[b]))
            a_only = sum(
                1
                for k in indexes
                if rows[a][k]["correct"] and not rows[b][k]["correct"]
            )
            b_only = sum(
                1
                for k in indexes
                if rows[b][k]["correct"] and not rows[a][k]["correct"]
            )
            p = sign_p(a_only, a_only + b_only)
            p_text = "n/a" if p is None else f"{p:.3f}"
            print(f"  {a} vs {b}: {a}_only={a_only} {b}_only={b_only} p={p_text}")

    print("prompt chars (media):")
    for condition in CONDITIONS:
        if condition not in rows:
            continue
        values = [
            row["prompt_chars"]
            for row in rows[condition].values()
            if row.get("prompt_chars")
        ]
        if values:
            print(f"  {condition:<8} {sum(values) / len(values):.0f}")


if __name__ == "__main__":
    main()
