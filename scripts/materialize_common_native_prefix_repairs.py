"""Restore single-entry English starts without changing prose or native tables."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.build_integrated_release import validate_fixed_allocation_policy
from scripts.inventory_common_native_messages import inventory


def repair_prefix(source: bytes, current: bytes, start: int) -> bytes:
    """Move an unchanged paragraph past its verified alignment prefix.

    Only unused terminal spaces fund the move. No words, controls or line breaks
    are removed. Caller must prove there is only one native entry in this record.
    """
    if len(source) != len(current) or start not in (1, 2) or source[:start] != b" " * start:
        raise ValueError("Source alignment/allocation is not proven")
    if b"\0" in current or any(byte > 127 for byte in current):
        raise ValueError("Repair requires a single English NUL allocation")
    paragraph = current.rstrip(b" ")
    if len(paragraph) + start > len(current):
        raise ValueError("Insufficient unused padding; relocation required")
    return (source[:start] + paragraph).ljust(len(current), b" ")


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--parent-profile", required=True)
    parser.add_argument("--release-version", required=True, type=int)
    parser.add_argument("--blocks", nargs="+", type=int)
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()
    clean = NdsImage.open("work/clean.nds")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    candidate = NdsImage.open(args.candidate)
    file_path = "/COMMON/MESFILE.DK4"
    current_common = candidate.read_file(file_path)
    clean_common = clean.read_file(file_path)
    clean_blocks = IlnkContainer.parse(clean_common).blocks
    current_blocks = IlnkContainer.parse(current_common).blocks
    canonical_blocks = IlnkContainer.parse(canonical.read_file(file_path)).blocks
    entries = common_message_entries(current_common, candidate.read_file("/__arm9__.bin"), clean=False)
    owners = defaultdict(list)
    for entry in entries:
        owners[entry.block, entry.record_index].append(entry)
    report = inventory(args.candidate, Path("work/clean.nds"))
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    parent = stack["profiles"][args.parent_profile]
    active = {}
    for name in parent["batches"]:
        batch = json.loads(Path(name).read_text(encoding="utf-8"))
        if batch.get("file_path") == file_path:
            active.update({row["id"]: row for row in batch.get("records", [])})
    records, skipped = [], []
    for finding in report["leading_prefix_findings"]:
        block, record = finding["block"], finding["record"]
        if args.blocks and block not in args.blocks:
            continue
        row_id = f"DK4_MES_B{block:02d}_R{record:04d}"
        try:
            if len(owners[block, record]) != 1:
                raise ValueError("Packed neighbors require full entry mapping")
            old_row = active.get(row_id)
            raw = current_blocks[block].split(b"\0")[record]
            if old_row is None:
                if canonical_blocks[block].split(b"\0")[record] != raw:
                    raise ValueError("Undeclared text differs from canonical source")
                continuation_lines = raw.rstrip(b" ").split(b"\n")[1:]
                if any(not line.startswith(b" ") for line in continuation_lines):
                    raise ValueError("Canonical continuation lacks a protective guard")
                old_row = {
                    "id": row_id, "replacement_hex": raw.hex().upper(),
                    "entry_offsets": [0], "entry_guard_bytes": 0,
                    "linebreak_guard_bytes": 1 if continuation_lines else 0,
                    "text_box_max_chars": 36,
                    "english": raw.rstrip(b" ").decode("ascii"),
                }
            if old_row.get("entry_offsets") != [0]:
                raise ValueError("Single declared entry at zero not established")
            if bytes.fromhex(old_row["replacement_hex"]) != raw:
                raise ValueError("Active layout does not match saved candidate")
            entry = owners[block, record][0]
            source = clean_blocks[block].split(b"\0")[record]
            replacement = repair_prefix(source, raw, entry.start)
            row = copy.deepcopy(old_row)
            row.update({
                "replacement_hex": replacement.hex().upper(),
                "entry_offsets": [entry.start], "entry_ends": [entry.end],
                "translated_ranges": [[entry.start, entry.end]],
                "native_table_offsets": [entry.table_offset],
                "entry_guard_bytes": int(old_row.get("entry_guard_bytes", 0)),
                "migration_original_hex": raw.hex().upper(),
                "migration_message_id": entry.message_id,
                "display_entries": [raw[int(old_row.get("entry_guard_bytes", 0)):].rstrip(b" ").decode("ascii")],
                "context": "Unchanged reviewed English moved to its executable-loader-selected start.",
                "notes": "Restores clean alignment prefix using only terminal padding. Prose, controls, LF guards, table and NUL allocations are unchanged.",
            })
            validate_fixed_allocation_policy(Path("single-native-repair"), {
                "fixed_allocation_policy": "screen-entry-layout-v1", "records": [row],
            })
            records.append(row)
        except (ValueError, KeyError) as exc:
            skipped.append({"id": row_id, "reason": str(exc)})
    version = args.release_version
    batch_path = Path(f"translations/common_native_prefix_repairs_v{version}.json")
    payload = {
        "format": "dk4-ilnk-translation-batch-v1", "content_type": "common-fixed-dialogue-v2",
        "file_path": file_path,
        "source_file_sha256": hashlib.sha256(canonical.read_file(file_path)).hexdigest(),
        "target_locale": "en-US", "scope": "Layout migration only: restore proven single-entry native starts without editing English.",
        "fixed_allocation_policy": "screen-entry-layout-v1",
        "ascii_guard_exemption": "Loader-verified native start; restores source alignment outside the copied message and preserves existing continuation guards.",
        "records": records,
    }
    validate_fixed_allocation_policy(batch_path, payload)
    plan = {"candidate": args.candidate.as_posix(), "parent_profile": args.parent_profile,
            "repair_count": len(records), "skipped_count": len(skipped), "skipped": skipped,
            "repairs": [{"id": row["id"], "message_id": row["migration_message_id"],
                         "start": row["entry_offsets"][0], "text": row["display_entries"][0]} for row in records]}
    write_json(Path(f"work/analysis/common_prefix_v{version}_plan.json"), plan)
    if not args.plan_only:
        write_json(batch_path, payload)
        replacement_ids = {row["id"] for row in records}
        batches = []
        for name in parent["batches"]:
            batch = json.loads(Path(name).read_text(encoding="utf-8"))
            if batch.get("file_path") == file_path and any(row["id"] in replacement_ids for row in batch.get("records", [])):
                batch["records"] = [row for row in batch["records"] if row["id"] not in replacement_ids]
                filtered = Path("translations") / f"{Path(name).stem}_native_v{version}.json"
                write_json(filtered, batch)
                if batch["records"]:
                    batches.append(filtered.as_posix())
            else:
                batches.append(name)
        profile = copy.deepcopy(parent)
        profile["batches"] = batches + [batch_path.as_posix()]
        profile["note"] = f"Extends {args.parent_profile} with {len(records)} native single-entry start repairs; unchanged prose. Experimental, runtime pending."
        stack["profiles"][f"all-routes-unified-v{version}"] = profile
        write_json(stack_path, stack)
    print(json.dumps({"repairs": len(records), "skipped": len(skipped), "plan_only": args.plan_only}))


if __name__ == "__main__":
    main()
