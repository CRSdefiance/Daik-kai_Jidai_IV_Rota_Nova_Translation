"""Extract clean source for each missing native message and its packed neighbors."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.inventory_common_native_messages import inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--clean", type=Path, default=Path("work/clean.nds"))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = inventory(args.candidate, args.clean)
    owners = {(row["block"], row["record"]) for row in report["blank_native_messages"]}
    clean = NdsImage.open(args.clean)
    entries = common_message_entries(clean.read_file("/COMMON/MESFILE.DK4"),
                                     clean.read_file("/__arm9__.bin"))
    rows = [{"message_id": entry.message_id, "block": entry.block,
             "record": entry.record_index, "source_hex": entry.text.hex().upper(),
             "japanese": entry.text.decode("cp932")}
            for entry in entries if (entry.block, entry.record_index) in owners]
    missing_ids = {row["message_id"] for row in report["blank_native_messages"]}
    if not missing_ids <= {row["message_id"] for row in rows}:
        raise ValueError("Missing native entry is absent from the clean owning record")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate": args.candidate.as_posix(),
                      "candidate_sha256": report["candidate_sha256"],
                      "missing_native_messages": len(missing_ids),
                      "owning_records": len(owners), "source_entries_with_neighbors": len(rows),
                      "source_counts_by_block": dict(sorted(Counter(row["block"] for row in rows).items())),
                      "out": args.out.as_posix()}, indent=2))


if __name__ == "__main__":
    main()
