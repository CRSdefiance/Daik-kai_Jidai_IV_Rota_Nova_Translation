"""Verify saved block-preserving COMMON repacks against every native message."""
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


def verify(candidate_path: Path, previous_path: Path, manifest_path: Path) -> dict:
    current, previous = NdsImage.open(candidate_path), NdsImage.open(previous_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
    old_common, new_common = previous.read_file(common_path), current.read_file(common_path)
    old_arm9, new_arm9 = previous.read_file(arm9_path), current.read_file(arm9_path)
    for raw, key in ((old_common, "parent_common_sha256"), (new_common, "expected_common_sha256"),
                     (new_arm9, "expected_arm9_sha256")):
        if hashlib.sha256(raw).hexdigest() != manifest[key]:
            raise ValueError(f"Saved repack hash differs: {key}")
    before = common_message_entries(old_common, old_arm9, clean=False)
    after = common_message_entries(new_common, new_arm9, clean=False)
    checks = []
    expected = {int(key): bytes.fromhex(value) for key, value in manifest["expected_selected_hex"].items()}
    for old, new in zip(before, after, strict=True):
        if (old.message_id, old.block, old.record_index) != (new.message_id, new.block, new.record_index):
            raise ValueError("Native global ID/block/NUL identity changed")
        if new.text.rstrip(b" ") != expected.get(new.message_id, old.text.rstrip(b" ")):
            raise ValueError(f"Native message {new.message_id}: text differs or leading/end characters dropped")
        if new.message_id in expected:
            checks.append({"message_id": new.message_id, "first_and_last_characters_intact": True,
                           "english": new.text.rstrip(b" ").decode("cp932")})
    old_blocks, new_blocks = IlnkContainer.parse(old_common).blocks, IlnkContainer.parse(new_common).blocks
    if [len(block) for block in old_blocks] != [len(block) for block in new_blocks]:
        raise ValueError("Native cache block sizes changed")
    if [block.count(b"\0") for block in old_blocks] != [block.count(b"\0") for block in new_blocks]:
        raise ValueError("Native NUL record counts changed")
    actual_records = {(block, index) for block, (old_block, new_block) in enumerate(zip(old_blocks, new_blocks, strict=True))
                      for index, (old, new) in enumerate(zip(old_block.split(b"\0"), new_block.split(b"\0"), strict=True))
                      if old != new}
    if actual_records != {tuple(pair) for pair in manifest["changed_records"]}:
        raise ValueError("Unexpected changed NUL records")
    expected_arm9 = bytearray(old_arm9)
    for offset in manifest["changed_offsets"]:
        expected_arm9[offset:offset + 2] = new_arm9[offset:offset + 2]
    if bytes(expected_arm9) != new_arm9:
        raise ValueError("ARM9 changes beyond mapped uint16 offsets")
    old_files, new_files = rom_files(previous), rom_files(current)
    if old_files.keys() != new_files.keys():
        raise ValueError("ROM file inventory changed")
    changed_paths = [name for name in old_files if old_files[name] != new_files[name]]
    if set(changed_paths) != {common_path, arm9_path}:
        raise ValueError(f"Unexpected changed files: {changed_paths}")
    return {"status": "pass", "candidate": candidate_path.as_posix(),
            "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
            "authored_entries": len(checks), "all_native_messages_checked": len(after),
            "changed_records": len(actual_records), "changed_uint16_offsets": len(manifest["changed_offsets"]),
            "native_cache_sizes_unchanged": True, "nul_record_identity_unchanged": True,
            "all_unrelated_selected_text_unchanged": True, "changed_paths": changed_paths, "checks": checks}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--previous", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = verify(args.candidate, args.previous, args.manifest)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "checks"}, indent=2))


if __name__ == "__main__":
    main()
