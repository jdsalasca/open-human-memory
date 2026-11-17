"""MEM-006 analysis: retrieval, execution, symbolic baseline, and costs."""

from __future__ import annotations

import itertools
import json
import math
import statistics
from pathlib import Path

from ohmem.mem_006 import library_text, symbolic_solve
from ohmem.v3_tasks import apply_program, make_task
from ohmem.v7_transfer import OPS

HERE = Path(__file__).resolve().parent
DATA = HERE / "results" / "retrieval-seed1.json"
CONDITIONS = [
    "clone",
    "oracle_skill",
    "retrieval",
    "random_skill",
    "expert_written",
    "symbolic_solver",
]


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
    print(f"skills verificadas: {data['n_skills']}")
    print(f"tareas: {len(by['retrieval'])}")
    print("\nacierto:")
    for condition in CONDITIONS:
        selected = by[condition]
        correct = sum(1 for row in selected.values() if row["correct"])
        skill = sum(1 for row in selected.values() if row["skill_correct"])
        print(
            f"  {condition:<16} {correct}/{len(selected)} "
            f"(selección {skill}/{len(selected)})"
        )

    print("\npares:")
    pairs = [
        ("retrieval", "clone"),
        ("retrieval", "random_skill"),
        ("retrieval", "expert_written"),
        ("retrieval", "oracle_skill"),
        ("retrieval", "symbolic_solver"),
        ("expert_written", "clone"),
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

    print("\nidentificabilidad (2 operaciones, 2 ejemplos):")
    library = data["library"]
    per_skill = data["tasks_per_skill"]
    determined = 0
    counts = []
    for task_index in range(len(by["retrieval"])):
        skill = library[task_index // per_skill]
        j = task_index % per_skill
        task = make_task(
            data["seed"],
            "delta",
            50_000 + int(skill["id"][1:]) * 10 + j,
            tuple(skill["program"]),
            "mem006",
        )
        pairs_support = list(
            zip(
                task.observation.support_inputs[: data["support"]],
                task.observation.support_outputs[: data["support"]],
            )
        )
        consistent = [
            program
            for program in itertools.product(OPS, repeat=2)
            if all(apply_program(program, x) == y for x, y in pairs_support)
        ]
        answers = {
            tuple(apply_program(program, task.observation.query))
            for program in consistent
        }
        counts.append(len(consistent))
        if len(answers) == 1:
            determined += 1
    print(f"  tareas con respuesta determinada: {determined}/{len(by['retrieval'])}")
    print(
        f"  programas consistentes por tarea: "
        f"min={min(counts)} mediana={statistics.median(counts)} max={max(counts)}"
    )

    print("\ncoste (input_tokens, mediana):")
    for condition in CONDITIONS:
        values = [
            row["input_tokens"]
            for row in by[condition].values()
            if row.get("input_tokens")
        ]
        if values:
            print(f"  {condition:<16} {statistics.median(values):.0f}")
        else:
            print(f"  {condition:<16} n/a")
    acquisition = [
        item["input_tokens"] for item in data["acquisition"] if item.get("input_tokens")
    ]
    if acquisition:
        print(
            f"  adquisición (8 llamadas): "
            f"mediana={statistics.median(acquisition):.0f} "
            f"total={sum(acquisition)}"
        )


if __name__ == "__main__":
    main()
