"""Verify every selected COMMON span after native offset repairs."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.build_integrated_release import rom_files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--previous", required=True, type=Path)
    parser.add_argument("--batch", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    current, previous = NdsImage.open(args.candidate), NdsImage.open(args.previous)
    payload = json.loads(args.batch.read_text(encoding="utf-8"))
    records = {row["message_id"]: row for row in payload["records"]}
    old_arm9, new_arm9 = previous.read_file("/__arm9__.bin"), current.read_file("/__arm9__.bin")
    expected_arm9 = bytearray(old_arm9)
    for row in records.values():
        offset = row["offset"]
        expected_arm9[offset:offset + 2] = bytes.fromhex(row["replacement_hex"])
    if new_arm9 != bytes(expected_arm9):
        raise ValueError("ARM9 changes exceed or omit declared two-byte native offsets")
    before = common_message_entries(previous.read_file("/COMMON/MESFILE.DK4"), old_arm9, clean=False)
    after = common_message_entries(current.read_file("/COMMON/MESFILE.DK4"), new_arm9, clean=False)
    checks = []
    for old, new in zip(before, after, strict=True):
        row = records.get(new.message_id)
        expected = bytes.fromhex(row["expected_selected_hex"]) if row else old.text
        if new.text != expected:
            raise ValueError(f"Native message {new.message_id}: selected text differs")
        if row:
            if new.block_offset != row["new_block_offset"] or new.table_offset != row["offset"]:
                raise ValueError("Saved table offset differs from native mapping")
            checks.append({"message_id": new.message_id, "first_characters_intact": True,
                           "selected_english": new.text.rstrip(b" ").decode("ascii")})
    old_files, new_files = rom_files(previous), rom_files(current)
    if old_files.keys() != new_files.keys():
        raise ValueError("ROM file inventory differs")
    changed = [name for name in old_files if old_files[name] != new_files[name]]
    if changed != ["/__arm9__.bin"]:
        raise ValueError(f"Unexpected changed ROM paths: {changed}")
    report = {"status": "pass", "candidate": args.candidate.as_posix(),
              "candidate_sha256": hashlib.sha256(args.candidate.read_bytes()).hexdigest(),
              "repaired_entries": len(checks), "all_native_spans_checked": len(after),
              "common_and_unrelated_files_unchanged": True, "changed_paths": changed, "checks": checks}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "checks"}, indent=2))


if __name__ == "__main__":
    main()
