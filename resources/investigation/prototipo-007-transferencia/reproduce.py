"""Reproduce Prototype 007 (retention, reset, transfer) with the frozen settings."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

COMMAND = [
    sys.executable,
    "-m",
    "ohmem.v7_transfer",
    "--n",
    "12",
    "--model",
    "gpt-6.1-terra",
    "--effort",
    "medium",
    "--out",
    str(HERE / "results" / "terra-medium-seed0.json"),
]


def main() -> None:
    env = {"PYTHONPATH": str(ROOT / "src")}
    completed = subprocess.run(COMMAND, cwd=str(ROOT), env={**env})
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
