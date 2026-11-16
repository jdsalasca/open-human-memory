"""Reproduce Prototype 004-A and write raw results.

Verifies the frozen protocol hash first: if the protocol changed after the
freeze, this script refuses to run.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v4_experiment import run  # noqa: E402

SEEDS = (0, 1, 2)


def verify_protocol(out_dir: Path) -> str:
    expected = (out_dir / "protocolo.sha256").read_text(encoding="ascii").split()[0]
    actual = hashlib.sha256((HERE / "protocolo-congelado.md").read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit("protocol changed after freeze; refusing to run")
    return actual


def mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 4)


def main() -> None:
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    sha = verify_protocol(out_dir)

    results = []
    for seed in SEEDS:
        result = run(seed=seed, n_train=60)
        results.append(result)
        (out_dir / f"seed-{seed}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        print(f"wrote seed-{seed}.json")

    conditions = []
    for name in [c["condition"] for c in results[0]["conditions"]]:
        rows = [c for r in results for c in r["conditions"] if c["condition"] == name]
        conditions.append(
            {
                "condition": name,
                "max_steps": rows[0]["max_steps"],
                "library_size": rows[0]["library_size"],
                "mean_accuracy": mean([r["accuracy"] for r in rows]),
                "mean_correct": mean([r["correct"] for r in rows]),
                "mean_macro_tasks": mean([r["macro_tasks"] for r in rows]),
                "mean_harmful_macro_tasks": mean(
                    [r["harmful_macro_tasks"] for r in rows]
                ),
                "mean_abstained": mean([r["abstained"] for r in rows]),
                "mean_candidates": mean([r["cost"]["candidates"] for r in rows]),
                "mean_primitive_ops": mean([r["cost"]["primitive_ops"] for r in rows]),
            }
        )

    by = {c["condition"]: c for c in conditions}
    grid = {
        "n_libraries": results[0]["sweep_grid"]["n_libraries"],
        "mean_accuracy": mean([r["sweep_grid"]["mean_accuracy"] for r in results]),
        "mean_median_accuracy": mean(
            [r["sweep_grid"]["median_accuracy"] for r in results]
        ),
        "max_accuracy": max(r["sweep_grid"]["max_accuracy"] for r in results),
        "min_accuracy": min(r["sweep_grid"]["min_accuracy"] for r in results),
        "perfect": sum(r["sweep_grid"]["perfect"] for r in results) // len(results),
        "at_or_above_learned": mean(
            [
                sum(
                    1
                    for row in r["sweep_grid"]["rows"]
                    if row["accuracy"] >= by["A3-learned-d2"]["mean_accuracy"]
                )
                for r in results
            ]
        ),
    }
    selected = {
        "mean_accuracy": mean(
            [r["sweep_selected_d3"]["mean_accuracy"] for r in results]
        ),
        "mean_perfect": mean([r["sweep_selected_d3"]["perfect"] for r in results]),
        "n_libraries": results[0]["sweep_selected_d3"]["n_libraries"],
    }

    acquisition = []
    n_values = [row["n_train"] for row in results[0]["acquisition"]["rows"]]
    for n in n_values:
        rows = [
            r
            for res in results
            for r in res["acquisition"]["rows"]
            if r["n_train"] == n
        ]
        acquisition.append(
            {
                "n_train": n,
                "mean_macros": mean([r["n_macros"] for r in rows]),
                "mean_accuracy": mean([r["accuracy"] for r in rows]),
            }
        )

    train_candidates = mean([r["training"]["cost"]["candidates"] for r in results])
    train_ops = mean([r["training"]["cost"]["primitive_ops"] for r in results])

    per_solved = {
        name: round(c["mean_candidates"] / c["mean_correct"], 2)
        for name, c in by.items()
    }

    decisions = {
        "D1_no_new_capability": by["A1-nolearn-d3"]["mean_accuracy"]
        >= by["A3-learned-d2"]["mean_accuracy"],
        "D2_coverage_deficit": round(
            by["A1-nolearn-d3"]["mean_accuracy"] - by["A3-learned-d2"]["mean_accuracy"],
            4,
        ),
        "D3_candidate_saving": round(
            1
            - by["A3-learned-d2"]["mean_candidates"]
            / by["A1-nolearn-d3"]["mean_candidates"],
            4,
        ),
        "D4_random_control_invalid": (
            selected["mean_perfect"] / selected["n_libraries"]
        )
        > 0.05,
        "D5_saturation_n": next(
            row["n_train"]
            for row in acquisition
            if row["mean_accuracy"] == acquisition[-1]["mean_accuracy"]
        ),
        "D6_deeper_search_dominates_at_equal_budget": results[0]["budget"][
            "A1-nolearn-d3"
        ][-1]["correct"]
        >= results[0]["budget"]["A3-learned-d2"][-1]["correct"],
        "D7_lossy_compilation": by["A3-learned-d2"]["mean_correct"]
        < by["A1-nolearn-d3"]["mean_correct"],
        "D8_library_raises_search_cost_at_depth3": by["A4-learned-d3"][
            "mean_candidates"
        ]
        > by["A1-nolearn-d3"]["mean_candidates"],
    }

    summary = {
        "protocol_sha256": sha,
        "seeds": list(SEEDS),
        "n_tasks": results[0]["n_tasks"],
        "learned_macros": results[0]["learned_macros"],
        "training": {
            "n_train": results[0]["n_train"],
            "shared_candidates": train_candidates,
            "shared_primitive_ops": train_ops,
        },
        "conditions": conditions,
        "per_solved_task_candidates": per_solved,
        "sweep_grid": grid,
        "sweep_selected_d3": selected,
        "acquisition": acquisition,
        "budget": results[0]["budget"],
        "decisions": decisions,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("wrote summary.json")
    print(json.dumps(decisions, indent=2))


if __name__ == "__main__":
    main()
