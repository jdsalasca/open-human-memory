"""Reproduce Prototype 006 and write raw results.

Freeze first (`--freeze`), then run. The script refuses to run if the protocol,
the code or the task data changed after the freeze. Seeds 1 and 2 are the
evaluation; seed 0 was used to develop the design and is not reported.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from ohmem.v6_policy import build_library, novel_tasks, run, similar_tasks  # noqa: E402

SEEDS = (1, 2)
CODE = (
    "src/ohmem/v6_policy.py",
    "src/ohmem/v3_solver.py",
    "src/ohmem/v3_library.py",
    "src/ohmem/v3_tasks.py",
    "src/ohmem/v4_experiment.py",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def task_payload(task) -> dict:
    return {
        "id": task.observation.id,
        "inputs": [list(x) for x in task.observation.support_inputs],
        "outputs": [list(y) for y in task.observation.support_outputs],
        "query": list(task.observation.query),
        "program": list(task.solution.program),
    }


def freeze() -> None:
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    lines = [f"{sha(HERE / 'protocolo-congelado.md')}  protocolo-congelado.md"]
    for relative in CODE:
        lines.append(f"{sha(ROOT / relative)}  {relative}")
    for seed in SEEDS:
        library = build_library(seed)
        payload = {
            "library": [list(m.body) for m in library.macros],
            "similar": [task_payload(t) for t in similar_tasks(seed)],
            "novel": [task_payload(t) for t in novel_tasks(seed, library)],
        }
        digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
        lines.append(f"{digest}  data-seed-{seed}.json")
    (out_dir / "frozen.sha256").write_text("\n".join(lines) + "\n", encoding="ascii")
    print("\n".join(lines))


def verify() -> None:
    frozen = (HERE / "results" / "frozen.sha256").read_text(encoding="ascii")
    expected = {}
    for line in frozen.strip().splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    checks = {"protocolo-congelado.md": HERE / "protocolo-congelado.md"}
    for relative in CODE:
        checks[relative] = ROOT / relative
    for seed in SEEDS:
        library = build_library(seed)
        payload = {
            "library": [list(m.body) for m in library.macros],
            "similar": [task_payload(t) for t in similar_tasks(seed)],
            "novel": [task_payload(t) for t in novel_tasks(seed, library)],
        }
        checks[f"data-seed-{seed}.json"] = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()
    for name, value in checks.items():
        actual = value if isinstance(value, str) else sha(value)
        if expected.get(name) != actual:
            raise SystemExit(f"frozen hash mismatch: {name}")


def mean(values):
    values = [v for v in values if v is not None]
    return round(sum(values) / len(values), 4) if values else None


def main() -> None:
    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    verify()
    results = []
    for seed in SEEDS:
        result = run(seed)
        results.append(result)
        (out_dir / f"seed-{seed}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        print(f"wrote seed-{seed}.json")

    summary = {"seeds": list(SEEDS), "policies": {}, "decisions": {}}
    for label in ("policy-applicability", "policy-blind"):
        block = {"sets": {}}
        for set_name in ("similar", "novel", "mixed"):
            conditions = {}
            for condition in results[0]["policies"][label]["conditions"][set_name]:
                rows = [
                    r["policies"][label]["conditions"][set_name][condition]
                    for r in results
                ]
                conditions[condition] = {
                    "accuracy": mean([r["accuracy"] for r in rows]),
                    "mean_steps": mean([r["mean_steps"] for r in rows]),
                    "mean_reward": mean([r.get("mean_reward") for r in rows]),
                }
            block["sets"][set_name] = conditions
        block["weights"] = results[0]["policies"][label]["weights"]
        summary["policies"][label] = block

    def acc(policy, set_name, condition):
        return summary["policies"][policy]["sets"][set_name][condition]["accuracy"]

    app = "policy-applicability"
    blind = "policy-blind"
    decisions = {
        "P1_policy_beats_best_fixed_on_mixed": acc(app, "mixed", "learned-policy")
        >= max(acc(app, "mixed", "memory"), acc(app, "mixed", "search")),
        "P1_margin_vs_search": round(
            acc(app, "mixed", "learned-policy") - acc(app, "mixed", "search"), 4
        ),
        "P2_recovers_on_novel": round(
            acc(app, "novel", "learned-policy") - acc(app, "novel", "memory"), 4
        )
        >= 0.05,
        "P2_gap": round(
            acc(app, "novel", "learned-policy") - acc(app, "novel", "memory"), 4
        ),
        "P3_probe_matters": acc(app, "mixed", "learned-policy")
        > acc(blind, "mixed", "learned-policy"),
        "P4_saves_steps_on_similar": summary["policies"][app]["sets"]["similar"][
            "learned-policy"
        ]["mean_steps"]
        < summary["policies"][app]["sets"]["similar"]["search"]["mean_steps"],
    }
    summary["decisions"] = decisions
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("wrote summary.json")
    for key, value in decisions.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    if "--freeze" in sys.argv:
        freeze()
    else:
        main()
