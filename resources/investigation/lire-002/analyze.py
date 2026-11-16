"""Analysis of LIRE-002 results (no LLM calls)."""

from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "results" / "luna-low-12cases.json"
REPRESENTATIONS = ["es", "en", "zh", "es_concise", "dsl", "json", "table"]
NO_TABLE = "none"


def sign_p(k: int, n: int) -> float | None:
    if n == 0:
        return None
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(k, n - k) + 1)) / 2**n)


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rows = data["rows"]
    bits = data["table_bits"]

    def selected(representation: str, primary: bool | None = None) -> list[dict]:
        return [
            row
            for row in rows
            if row["representation"] == representation
            and (primary is None or row["primary"] == primary)
        ]

    none_tokens = {
        row["case_index"]: row["input_tokens"]
        for row in selected(NO_TABLE)
        if row["input_tokens"]
    }

    print(f"table_bits: {bits}")
    print(
        f"{'rep':<11} {'prim':>5} {'sec':>5} {'all':>5} "
        f"{'med_inc':>8} {'min_inc':>8} {'prim/1k':>8} {'bits/tok':>8}"
    )
    for representation in REPRESENTATIONS + [NO_TABLE]:
        primary = selected(representation, True)
        secondary = selected(representation, False)
        all_rows = selected(representation)
        deltas = [
            row["input_tokens"] - none_tokens[row["case_index"]]
            for row in all_rows
            if row["input_tokens"] and row["case_index"] in none_tokens
        ]
        median_delta = statistics.median(deltas) if deltas else 0
        primary_correct = sum(1 for row in primary if row["correct"])
        print(
            f"{representation:<11} "
            f"{primary_correct}/{len(primary):<3} "
            f"{sum(1 for row in secondary if row['correct'])}/{len(secondary):<3} "
            f"{sum(1 for row in all_rows if row['correct'])}/{len(all_rows):<3} "
            f"{median_delta:>8.0f} "
            f"{min(deltas) if deltas else 0:>8.0f} "
            f"{1000 * primary_correct / len(primary) / median_delta if median_delta > 0 else 0:>8.2f} "
            f"{bits / median_delta if median_delta > 0 else 0:>8.2f}"
        )

    print("\npares primarios:")
    for representation in REPRESENTATIONS:
        base = {
            row["case_index"]: row["correct"]
            for row in selected("es" if representation != "es" else NO_TABLE, True)
        }
        own = {
            row["case_index"]: row["correct"] for row in selected(representation, True)
        }
        indexes = sorted(set(own) & set(base))
        a_only = sum(1 for i in indexes if own[i] and not base[i])
        b_only = sum(1 for i in indexes if base[i] and not own[i])
        p = sign_p(a_only, a_only + b_only)
        label = "vs none" if representation == "es" else "vs es"
        print(
            f"  {representation:<11} {label:<8} "
            f"a_only={a_only} b_only={b_only} p={p if p is not None else 'n/a'}"
        )


if __name__ == "__main__":
    main()
