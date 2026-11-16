"""Longitudinal diagnostic: accuracy and gain G(n) as experience grows."""

from __future__ import annotations

import argparse
import json

from .v2_experiment import run


def run_curve(
    seed: int = 0, n_values: tuple[int, ...] = (50, 100, 200, 400), n_eval: int = 50
) -> dict:
    rows = []
    for n in n_values:
        result = run(seed=seed, n_train=n, n_eval=n_eval)
        baseline = {
            row["distribution"]: row["accuracy"]
            for row in result["rows"]
            if row["condition"] == "A-no-memory"
        }
        for row in result["rows"]:
            rows.append(
                {
                    "n": n,
                    "condition": row["condition"],
                    "distribution": row["distribution"],
                    "accuracy": row["accuracy"],
                    "gain_vs_no_memory": round(
                        row["accuracy"] - baseline[row["distribution"]], 4
                    ),
                }
            )
    return {"seed": seed, "n_values": list(n_values), "n_eval": n_eval, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--eval", type=int, default=50)
    parser.add_argument("--n", type=str, default="50,100,200,400")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    n_values = tuple(int(x) for x in args.n.split(","))
    result = run_curve(args.seed, n_values, args.eval)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"seed={result['seed']} eval={result['n_eval']}")
    print(f"{'n':>5} {'condition':<28} {'dist':<4} {'acc':>6} {'G(n)':>7}")
    for row in result["rows"]:
        print(
            f"{row['n']:>5} {row['condition']:<28} {row['distribution']:<4} "
            f"{row['accuracy']:>6.3f} {row['gain_vs_no_memory']:>7.3f}"
        )


if __name__ == "__main__":
    main()
