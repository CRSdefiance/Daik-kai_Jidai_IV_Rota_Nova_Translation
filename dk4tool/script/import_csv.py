from __future__ import annotations

import csv
from pathlib import Path

from .model import CSV_COLUMNS


class ScriptCsvError(ValueError):
    pass


def read_script_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = [column for column in CSV_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ScriptCsvError(f"missing CSV columns: {', '.join(missing)}")
        rows = list(reader)
    for number, row in enumerate(rows, start=2):
        if not row["id"] or not row["file_path"]:
            raise ScriptCsvError(f"row {number}: id and file_path are required")
    return rows

