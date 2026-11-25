"""Check saved native prefix repairs, unchanged prose, tables and ROM files."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.build_integrated_release import rom_files


def verify(candidate_path: Path, previous_path: Path, batch_path: Path) -> dict:
    candidate, previous = NdsImage.open(candidate_path), NdsImage.open(previous_path)
    payload = json.loads(batch_path.read_text(encoding="utf-8"))
    path = "/COMMON/MESFILE.DK4"
    before, after = previous.read_file(path), candidate.read_file(path)
    before_blocks, after_blocks = IlnkContainer.parse(before).blocks, IlnkContainer.parse(after).blocks
    entries = {entry.message_id: entry for entry in common_message_entries(
        after, candidate.read_file("/__arm9__.bin"), clean=False)}
    expected_changes = set()
    checks = []
    for row in payload["records"]:
        entry = entries[row["migration_message_id"]]
        block, record = entry.block, entry.record_index
        if row["id"] != f"DK4_MES_B{block:02d}_R{record:04d}":
            raise ValueError("Native message identity differs from migration metadata")
        old = before_blocks[block].split(b"\0")[record]
        new = after_blocks[block].split(b"\0")[record]
        if old != bytes.fromhex(row["migration_original_hex"]) or new != bytes.fromhex(row["replacement_hex"]):
            raise ValueError(f"{row['id']}: saved migration bytes do not match")
        if entry.start != row["entry_offsets"][0] or entry.end != row["entry_ends"][0]:
            raise ValueError(f"{row['id']}: saved pointer differs from declared native start/end")
        if entry.text.rstrip(b" ") != old.rstrip(b" ") or len(old) != len(new):
            raise ValueError(f"{row['id']}: selected English or allocation changed")
        expected_changes.add((block, record))
        checks.append({"id": row["id"], "message_id": entry.message_id,
                       "selected_english": entry.text.rstrip(b" ").decode("ascii"),
                       "first_characters_intact": True})
    actual_changes = set()
    for block, (old_block, new_block) in enumerate(zip(before_blocks, after_blocks, strict=True)):
        old_rows, new_rows = old_block.split(b"\0"), new_block.split(b"\0")
        if [len(row) for row in old_rows] != [len(row) for row in new_rows]:
            raise ValueError(f"B{block}: NUL allocations changed")
        actual_changes.update((block, index) for index, pair in enumerate(zip(old_rows, new_rows, strict=True))
                              if pair[0] != pair[1])
    if actual_changes != expected_changes:
        raise ValueError("Changes exceed or omit declared migration records")
    before_files, after_files = rom_files(previous), rom_files(candidate)
    if before_files.keys() != after_files.keys():
        raise ValueError("ROM file inventory changed")
    changed_paths = [name for name in before_files if before_files[name] != after_files[name]]
    if changed_paths != [path]:
        raise ValueError(f"Unexpected ROM changes: {changed_paths}")
    return {"status": "pass", "candidate": candidate_path.as_posix(),
            "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
            "repaired_native_entries": len(checks), "native_tables_unchanged": True,
            "nul_allocations_unchanged": True, "unchanged_prose_and_controls": True,
            "changed_paths": changed_paths, "checks": checks}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--previous", required=True, type=Path)
    parser.add_argument("--batch", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = verify(args.candidate, args.previous, args.batch)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "checks"}, indent=2))


if __name__ == "__main__":
    main()
