"""Factorial analysis of MEM-005 (no LLM calls)."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

from ohmem.mem_005 import CONDITIONS, SPECS

HERE = Path(__file__).resolve().parent
DATA = HERE / "results" / "factorial-seed1.json"


def sign_p(k: int, n: int) -> float | None:
    if n == 0:
        return None
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(k, n - k) + 1)) / 2**n)


def condition_for(content: str, status: str, instruction: str) -> str:
    return next(
        condition
        for condition, spec in SPECS.items()
        if spec == (status, instruction, content)
    )


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

    # Task-level table for the interaction bootstrap.
    task_correct = {
        index: {condition: by[condition][index]["correct"] for condition in CONDITIONS}
        for index in range(data["n"])
    }

    def interaction(indices: list[int]) -> float:
        def content_effect(status: str, instruction: str) -> float:
            correct = condition_for("correct", status, instruction)
            placebo = condition_for("placebo", status, instruction)
            return sum(
                task_correct[i][correct] - task_correct[i][placebo] for i in indices
            ) / len(indices)

        return (
            content_effect("verified", "apply")
            - content_effect("candidate", "apply")
            - content_effect("verified", "verify")
            + content_effect("candidate", "verify")
        )

    observed = interaction(list(range(data["n"])))
    rng = random.Random(0)
    boot = []
    for _ in range(10_000):
        sample = [rng.randrange(data["n"]) for _ in range(data["n"])]
        boot.append(interaction(sample))
    boot.sort()
    low = boot[int(0.025 * len(boot))]
    high = boot[int(0.975 * len(boot)) - 1]
    print(f"\ninteracción triple (contenido×estado×instrucción): {observed:.3f}")
    print(f"bootstrap 95% (10.000 remuestreos, semilla 0): [{low:.3f}, {high:.3f}]")

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
