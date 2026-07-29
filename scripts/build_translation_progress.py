from __future__ import annotations

# The repository root is intentionally added before importing the local package.
# ruff: noqa: I001

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.script.arm9_profiles import PROFILES
from dk4tool.script.mesfile import export_mesfile_rows


TRACKED_FILES = (
    "/COMMON/MESFILE.DK4",
    "/COMMON/HELP.DK4",
    "/data/SC0.DK4",
    "/data/SC1.DK4",
    "/data/SC2.DK4",
    "/data/SC3.DK4",
)


def source_path(root: Path, internal_path: str) -> Path:
    return root.joinpath(*internal_path.strip("/").split("/"))


def load_translated_records(translations: Path) -> set[tuple[str, str]]:
    translated: set[tuple[str, str]] = set()
    for path in sorted(translations.glob("*.json")):
        batch = json.loads(path.read_text(encoding="utf-8"))
        if batch.get("format") != "dk4-ilnk-translation-batch-v1":
            continue
        file_path = str(batch.get("file_path", ""))
        for record in batch.get("records", []):
            if str(record.get("english", "")).strip():
                translated.add((file_path, str(record.get("id", ""))))
    for path in sorted(translations.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                if str(row.get("english", "")).strip():
                    translated.add((str(row.get("file_path", "")), str(row.get("id", ""))))
    return translated


def build_report(source_root: Path, translations: Path) -> str:
    translated = load_translated_records(translations)
    rows: list[tuple[str, int, int, float]] = []
    total_records = 0
    total_translated = 0

    for internal_path in TRACKED_FILES:
        path = source_path(source_root, internal_path)
        exported = export_mesfile_rows(path.read_bytes(), internal_path)
        ids = {str(row["id"]) for row in exported}
        done = sum((internal_path, row_id) in translated for row_id in ids)
        count = len(ids)
        percent = done * 100.0 / count if count else 0.0
        rows.append((internal_path, done, count, percent))
        total_records += count
        total_translated += done

    total_percent = total_translated * 100.0 / total_records if total_records else 0.0
    mapped_ui = len(PROFILES["all"])
    generated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")

    lines = [
        "# Translation progress",
        "",
        f"Generated: {generated}",
        "",
        (
            "This is a rough, record-based estimate. A translated record can be one short "
            "label or several dialogue lines, so the percentage is a navigation aid rather "
            "than a word-count claim."
        ),
        "",
        "| File | Translated records | Detected records | Approx. complete |",
        "|---|---:|---:|---:|",
    ]
    for internal_path, done, count, percent in rows:
        lines.append(f"| `{internal_path}` | {done} | {count} | {percent:.1f}% |")
    lines.extend(
        [
            f"| **Tracked text total** | **{total_translated}** | **{total_records}** | **{total_percent:.1f}%** |",
            "",
            "## Other tracked work",
            "",
            (
                f"- ARM9/UI dictionary: {mapped_ui} mapped slots have English replacements. "
                "This is not shown as a percentage because the full set of text-bearing ARM9 "
                "slots has not yet been exhaustively classified."
            ),
            (
                "- Redrawn graphics are tracked by the resource lists in "
                "`scripts/build_graphics_translation.py`; graphical text is not included in "
                "the table above."
            ),
            (
                "- An in-game save can retain old names and labels. Coverage is measured "
                "against the clean ROM and translation sources, not save-state contents."
            ),
            "",
            "## How to refresh",
            "",
            "Run `python scripts/build_translation_progress.py` after adding or revising translation batches.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a rough per-file translation coverage report")
    parser.add_argument("--source-root", type=Path, default=Path("work/extracted_clean"))
    parser.add_argument("--translations", type=Path, default=Path("translations"))
    parser.add_argument("--out", type=Path, default=Path("docs/translation_progress.md"))
    args = parser.parse_args()
    report = build_report(args.source_root, args.translations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
