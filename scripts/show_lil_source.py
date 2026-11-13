from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Show clean Lil source with reviewed lead states removed.")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument(
        "--strip-lead",
        action="append",
        default=[],
        help="Hex presentation byte to remove for this inspected scene (repeatable).",
    )
    args = parser.parse_args()
    states = {int(value, 16) for value in args.strip_lead}
    with (ROOT / "work/sc2/script.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        row_id = row["id"]
        block = int(row_id.split("_B", 1)[1].split("_R", 1)[0])
        if not args.start <= block <= args.end:
            continue
        raw = bytes.fromhex(row["source_hex"])
        lead = raw[0]
        body = raw[1:] if lead in states else raw
        text = body.decode("cp932", errors="replace").replace("\n", "{LB}")
        print(f"{row_id} [{lead:02X}, {len(raw)}b] {text}")


if __name__ == "__main__":
    main()
