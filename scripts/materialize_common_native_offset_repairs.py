"""Restore full single-entry messages by correcting source-locked native offsets."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import struct
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.inventory_common_native_messages import inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--parent-profile", required=True)
    parser.add_argument("--release-version", required=True, type=int)
    args = parser.parse_args()
    image = NdsImage.open(args.candidate)
    base = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    common = image.read_file("/COMMON/MESFILE.DK4")
    arm9 = image.read_file("/__arm9__.bin")
    canonical_arm9 = base.read_file("/__arm9__.bin")
    before = common_message_entries(common, arm9, clean=False)
    owners = Counter((entry.block, entry.record_index) for entry in before)
    blocks = IlnkContainer.parse(common).blocks
    report = inventory(args.candidate, Path("work/clean.nds"))
    patched = bytearray(arm9)
    records, expected, skipped = [], {}, []
    for finding in report["leading_prefix_findings"]:
        entry = before[finding["message_id"]]
        if owners[entry.block, entry.record_index] != 1:
            skipped.append({"message_id": entry.message_id, "reason": "Packed entry requires complete interior layout"})
            continue
        raw = blocks[entry.block].split(b"\0")[entry.record_index]
        start = entry.block_offset - entry.start
        old_bytes = arm9[entry.table_offset:entry.table_offset + 2]
        if old_bytes != canonical_arm9[entry.table_offset:entry.table_offset + 2]:
            raise ValueError("Repair would overlap an accepted remapped pointer")
        replacement = struct.pack("<H", start)
        patched[entry.table_offset:entry.table_offset + 2] = replacement
        expected[entry.message_id] = raw
        records.append({
            "id": f"COMMON_NATIVE_OFFSET_{entry.message_id:04d}",
            "offset": entry.table_offset, "source_hex": old_bytes.hex().upper(),
            "replacement_hex": replacement.hex().upper(),
            "message_id": entry.message_id, "block": entry.block, "record": entry.record_index,
            "old_block_offset": entry.block_offset, "new_block_offset": start,
            "expected_selected_hex": raw.hex().upper(),
            "english": f"Native message {entry.message_id} offset repair",
            "context": "Single-entry record's complete English begins at its NUL allocation start; executable loader copies bytes without an alignment requirement.",
        })
    after = common_message_entries(common, bytes(patched), clean=False)
    for old, new in zip(before, after, strict=True):
        target = expected.get(new.message_id, old.text)
        if new.text != target:
            raise ValueError(f"Message {new.message_id}: repair changes or truncates selected text")
    version = args.release_version
    path = Path(f"translations/common_native_offset_repairs_v{version}.json")
    payload = {"format": "dk4-arm9-fixed-text-batch-v1",
               "content_type": "arm9-native-message-offset-v1", "file_path": "/__arm9__.bin",
               "source_file_sha256": hashlib.sha256(canonical_arm9).hexdigest(),
               "scope": "Native offset migration only; all COMMON bytes, prose and executable code unchanged.",
               "records": records}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    profile = copy.deepcopy(stack["profiles"][args.parent_profile])
    profile["batches"].append(path.as_posix())
    profile["note"] = f"Extends {args.parent_profile} with {len(records)} loader-proven native start corrections. All 3668 selected spans checked; runtime pending."
    stack["profiles"][f"all-routes-unified-v{version}"] = profile
    stack_path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(f"work/analysis/common_offset_v{version}_plan.json").write_text(json.dumps({
        "repaired": len(records), "skipped": skipped, "all_native_entries_compared": len(after),
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"repaired": len(records), "skipped": len(skipped), "all_entries_checked": len(after)}))


if __name__ == "__main__":
    main()
