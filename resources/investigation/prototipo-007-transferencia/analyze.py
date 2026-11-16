"""Paired analysis of Prototype 007 runs (no LLM calls)."""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"


def main() -> None:
    summary = {}
    for path in sorted(RESULTS.glob("*.json")):
        if path.name == "summary.json":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data["rows"]
        conditions = data["conditions"]
        paired = {}
        for condition in conditions:
            if condition == "clone":
                continue
            clone = {
                r["index"]: r["correct"] for r in rows if r["condition"] == "clone"
            }
            other = {
                r["index"]: r["correct"] for r in rows if r["condition"] == condition
            }
            paired[condition] = {
                "both": sum(1 for i in clone if clone[i] and other[i]),
                "clone_only": sum(1 for i in clone if clone[i] and not other[i]),
                "other_only": sum(1 for i in clone if other[i] and not clone[i]),
                "neither": sum(1 for i in clone if not clone[i] and not other[i]),
            }
        summary[path.name] = {
            "n": data["n"],
            "support": data.get("support", 1 if "support1" in path.name else 3),
            "suffix": data.get("suffix", 3),
            "session1": data["session1"],
            "conditions": conditions,
            "paired_vs_clone": paired,
        }
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
