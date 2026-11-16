"""Execution map analysis: accuracy by nominal depth and functional length."""

from __future__ import annotations

import itertools
import json
from collections import defaultdict
from pathlib import Path

from ohmem.v3_tasks import apply_program
from ohmem.v7_transfer import OPS, PROBES

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"


def signature(program: tuple[str, ...]) -> tuple:
    return tuple(apply_program(program, probe) for probe in PROBES)


def minimum_length(program: tuple[str, ...]) -> int:
    target = signature(program)
    for length in range(1, len(program)):
        for candidate in itertools.product(OPS, repeat=length):
            if signature(candidate) == target:
                return length
    return len(program)


def taxonomy(answer, expected) -> str:
    if answer == expected:
        return "correct"
    if not isinstance(answer, list):
        return "invalid"
    if sorted(answer) == sorted(expected):
        return "permutation"
    if len(answer) != len(expected):
        return "length"
    return "other"


def main() -> None:
    cache: dict[tuple[str, ...], int] = {}
    by_nominal: dict[int, list[dict]] = defaultdict(list)
    by_min: dict[int, list[dict]] = defaultdict(list)
    print(f"{'depth':>5} {'min':>4} {'correct':>7} {'accuracy':>8}  taxonomy")
    for path in sorted(RESULTS.glob("oracle-depth-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        depth = int(path.stem.split("-")[-1])
        rows = data["rows"]
        for row in rows:
            program = tuple(row["program"])
            if program not in cache:
                cache[program] = minimum_length(program)
            row["min_length"] = cache[program]
            by_nominal[depth].append(row)
            by_min[row["min_length"]].append(row)
        counts = defaultdict(int)
        for row in rows:
            counts[taxonomy(row["answer"], row["expected"])] += 1
        correct = counts["correct"]
        print(
            f"{depth:>5} {'-':>4} {correct:>3}/{len(rows):<3} "
            f"{correct / len(rows):>8.2f}  {dict(counts)}"
        )
        for row in rows:
            if not row["correct"]:
                print(
                    f"      min={row['min_length']} got={row['answer']} "
                    f"want={row['expected']} ({taxonomy(row['answer'], row['expected'])})"
                )

    print("\npor longitud minima:")
    for length in sorted(by_min):
        rows = by_min[length]
        correct = sum(1 for row in rows if row["correct"])
        print(f"  min={length}: {correct}/{len(rows)} ({correct / len(rows):.2f})")


if __name__ == "__main__":
    main()
