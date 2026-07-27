from __future__ import annotations

import csv
from pathlib import Path

from .model import CSV_COLUMNS


def write_script_csv(path: str | Path, rows: list[dict[str, object]]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

