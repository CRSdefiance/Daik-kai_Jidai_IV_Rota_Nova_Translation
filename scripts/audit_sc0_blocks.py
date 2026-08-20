from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from dk4tool.script.mesfile import export_mesfile_rows

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "work" / "extracted_clean" / "data" / "SC0.DK4"
TRANSLATIONS = ROOT / "translations"
OUT = ROOT / "docs" / "sc0_block_map.md"


def block_number(block: str) -> int:
    return int(block.rsplit("B", 1)[1])


def known_description(number: int) -> tuple[str, str]:
    if 43 <= number <= 48:
        return "Raphael", "Raphael prologue/opening scenes"
    if 137 <= number <= 141:
        return "Raphael", "Raphael Mediterranean/route scenes"
    return "Unmapped", "Scene ownership and purpose not yet correlated"


NAME_CUES = {
    "ラファエル": "Raphael",
    "クラウディオ": "Claudio",
    "ジェナス": "Jenas",
    "フリオ": "Julio",
    "クロード": "Claude",
    "マルティン": "Martin",
    "エンリケ": "Henry",
    "レオン": "Leon",
    "パシャ": "Pasha",
}


def main() -> None:
    rows = export_mesfile_rows(SOURCE.read_bytes(), "/data/SC0.DK4")
    by_block: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_block[row["id"].split("_R", 1)[0]].append(row)

    translated: set[str] = set()
    for path in sorted(TRANSLATIONS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("file_path") == "/data/SC0.DK4":
            translated.update(str(record["id"]) for record in data.get("records", []))
    csv_path = TRANSLATIONS / "raphael_opening.csv"
    if csv_path.exists():
        with csv_path.open(encoding="utf-8-sig", newline="") as stream:
            translated.update(row["id"] for row in csv.DictReader(stream) if row.get("id"))

    total = len(rows)
    translated_total = sum(row["id"] in translated for row in rows)
    known_total = sum(
        len(block_rows)
        for block, block_rows in by_block.items()
        if known_description(block_number(block))[0] != "Unmapped"
    )
    lines = [
        "# SC0.DK4 block map",
        "",
        (
            "This inventory separates the identified Raphael blocks from the remaining SC0 scene groups. "
            "A block is an internal message group, not necessarily a complete story chapter. "
            "Unmapped groups require emulator/playthrough correlation before assigning them to a character or route."
        ),
        "",
        f"- Total SC0 records: **{total}**",
        f"- Records covered by current SC0 translation batches: **{translated_total}**",
        f"- Identified Raphael records: **{known_total}**",
        f"- Remaining records requiring ownership mapping: **{total - known_total}**",
        "",
        "| Block | Records | Translated | Coverage | Classification | Description |",
        "|---:|---:|---:|---:|---|---|",
    ]
    for block in sorted(by_block, key=block_number):
        number = block_number(block)
        block_rows = by_block[block]
        done = sum(row["id"] in translated for row in block_rows)
        classification, description = known_description(number)
        cues = sorted({english for row in block_rows for japanese, english in NAME_CUES.items() if japanese in row["japanese"]})
        if cues:
            description += "; name cues: " + ", ".join(cues)
        coverage = f"{done / len(block_rows) * 100:.1f}%" if block_rows else "0.0%"
        lines.append(f"| B{number:03d} | {len(block_rows)} | {done} | {coverage} | {classification} | {description} |")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(by_block)} blocks, {total} records)")


if __name__ == "__main__":
    main()
