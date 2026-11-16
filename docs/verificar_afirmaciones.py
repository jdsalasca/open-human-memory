"""Check the claims ledger against the numbers quoted in the docs.

Usage: python docs/verificar_afirmaciones.py
Exits non-zero if a document quotes a different count.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "registro-de-afirmaciones.md"

ROW = re.compile(r"^\| ([A-Z][0-9]+) \|")
STATUS = re.compile(
    r"\| \*\*([^*]+)\*\* \||\| (Sostenida|Refutada|Abierta|Inválida)[^|]*\|"
)


def classify(line: str) -> str:
    low = line.lower()
    if "refutada" in low:
        return "refutada"
    if "inválida" in low or "invalida" in low:
        return "inválida"
    if "abierta" in low:
        return "abierta"
    if "declarada" in low:
        return "declarada"
    if "sostenida" in low:
        return "sostenida"
    return "otra"


def main() -> None:
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    rows = [line for line in lines if ROW.match(line)]
    counts = {
        "sostenida": 0,
        "refutada": 0,
        "abierta": 0,
        "inválida": 0,
        "declarada": 0,
        "otra": 0,
    }
    for line in rows:
        counts[classify(line)] += 1
    total = len(rows)
    print(f"filas: {total}")
    print(counts)

    quoted = re.compile(
        r"(\d+) afirmaciones(?! (?:sostenidas|refutadas|abiertas|inválidas|declaradas))"
    )
    mismatches = []
    for path in ROOT.rglob("*.md"):
        if "node_modules" in path.parts or "revision-externa" in path.parts:
            continue
        for number, match in (
            (match.group(1), match)
            for match in quoted.finditer(
                path.read_text(encoding="utf-8", errors="ignore")
            )
        ):
            if int(number) != total:
                mismatches.append(f"{path.relative_to(ROOT)}: dice {number}")
    if mismatches:
        print("INCONSISTENCIAS:")
        for item in sorted(set(mismatches)):
            print("  " + item)
        sys.exit(1)
    print("documentos: OK")


if __name__ == "__main__":
    main()
