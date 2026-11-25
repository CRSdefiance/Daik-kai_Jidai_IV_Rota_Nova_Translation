"""Audit and register complete native COMMON record repacks."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.build_integrated_release import validate_fixed_allocation_policy


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--manuscript", required=True, type=Path)
    parser.add_argument("--parent-profile", required=True)
    parser.add_argument("--release-version", required=True, type=int)
    parser.add_argument("--reviewed", action="store_true")
    args = parser.parse_args()
    authored = json.loads(args.manuscript.read_text(encoding="utf-8"))
    if args.reviewed:
        validate_natural_dialogue_batch(authored)
    clean, base, current = (NdsImage.open(path) for path in
                            ("work/clean.nds", "out/raphael_natural_v2_accepted_base.nds", args.candidate))
    common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
    source_common = clean.read_file(common_path)
    source_blocks = IlnkContainer.parse(source_common).blocks
    source_entries = common_message_entries(source_common, clean.read_file(arm9_path))
    common, arm9 = current.read_file(common_path), current.read_file(arm9_path)
    encoded, prefixes, qa_rows = {}, {}, []
    qa_dir = Path(f"work/qa/common_native_repack_v{args.release_version}")
    for row in authored["records"]:
        entry = source_entries[row["message_id"]]
        if entry.text != bytes.fromhex(row["source_hex"]) or (entry.block, entry.record_index) != (row["block"], row["record"]):
            raise ValueError("Manuscript source does not match verified clean native entry")
        text = row["english"].removesuffix("{PAD}")
        if re.findall(r"%[sdi]", entry.text.decode("cp932")) != re.findall(r"%[sdi]", text):
            raise ValueError("Authored runtime substitutions differ from source")
        raw = text.encode("cp932")
        # The native loader terminates its copied output. Adjacent entries need
        # no artificial separator, which could advance a full final page.
        allocation = len(raw)
        audit = audit_native_common_entry(b" " * allocation, row["english"])
        preview = qa_dir / "previews" / f"{row['id']}.png"
        render_dialogue_preview(audit["formatted_markup"], get_dialogue_profile("shared"), preview,
                                arm9=arm9, kanji_font=base.read_file("/GRP/KANJI.FNT"))
        qa_rows.append({"id": row["id"], "source_hex": row["source_hex"],
                        "source": entry.text.decode("cp932"), "english": text,
                        "new_allocation_bytes": allocation, "issues": audit["issues"],
                        "preview": preview.as_posix(), "formatted_markup": audit["formatted_markup"]})
        encoded[entry.message_id] = raw
    target_owners = {(source_entries[i].block, source_entries[i].record_index) for i in encoded}
    for owner in target_owners:
        first = next(entry for entry in source_entries if (entry.block, entry.record_index) == owner)
        prefixes[owner] = source_blocks[owner[0]].split(b"\0")[owner[1]][:first.start]
    blockers = sum(issue["severity"] in {"error", "warning"} for row in qa_rows for issue in row["issues"])
    write_json(qa_dir / "report.json", {"blockers": blockers, "entries": qa_rows})
    if blockers:
        raise ValueError(f"{blockers} native QA blockers; inspect {qa_dir}")
    result = repack_native_records(common, arm9, encoded, prefixes)
    new_blocks = IlnkContainer.parse(result.common).blocks
    records = []
    for block, record in sorted(result.changed_records):
        raw = new_blocks[block].split(b"\0")[record]
        entries = [entry for entry in result.entries if (entry.block, entry.record_index) == (block, record)]
        paragraphs = [entry.text.rstrip(b" \n\r").decode("cp932") for entry in entries]
        records.append({
            "id": f"DK4_MES_B{block:02d}_R{record:04d}", "replacement_hex": raw.hex().upper(),
            "english": " | ".join(paragraphs), "display_entries": paragraphs,
            "allow_expand": True, "entry_offsets": [entry.start for entry in entries],
            "entry_ends": [entry.end for entry in entries],
            "native_table_offsets": [entry.table_offset for entry in entries],
            "translated_ranges": [[entry.start, entry.end] for entry in entries],
            "entry_guard_bytes": 0, "linebreak_guard_bytes": 1, "text_box_max_chars": 255,
            "safe_literal_latin_glyphs": sorted({c for text in paragraphs for c in text if c in {"Ｆ", "Ｉ"}}),
            "context": "Complete native record mapping; authored entries or unchanged padding donors.",
            "notes": "NUL identity and total native block allocation unchanged; all 3668 selections compared.",
        })
    version = args.release_version
    common_batch = Path(f"translations/common_native_repack_v{version}.json")
    common_payload = {"format": "dk4-ilnk-translation-batch-v1", "content_type": "common-fixed-dialogue-v2",
                      "file_path": common_path, "source_file_sha256": hashlib.sha256(base.read_file(common_path)).hexdigest(),
                      "editorial_batch": args.manuscript.as_posix(), "target_locale": "en-US",
                      "fixed_allocation_policy": "screen-entry-layout-v1",
                      "ascii_guard_exemption": "Native loader boundaries and automatic wrapping; complete repack updates every affected offset.",
                      "records": records}
    validate_fixed_allocation_policy(common_batch, common_payload)
    canonical_arm9 = base.read_file(arm9_path)
    offset_records = [{"id": f"COMMON_REPACK_OFFSET_{offset:06X}", "offset": offset,
                       "source_hex": canonical_arm9[offset:offset + 2].hex().upper(),
                       "replacement_hex": result.arm9[offset:offset + 2].hex().upper(),
                       "english": "Mapped COMMON native message offset"} for offset in sorted(result.changed_offsets)]
    offset_batch = Path(f"translations/common_native_repack_offsets_v{version}.json")
    offset_payload = {"format": "dk4-arm9-fixed-text-batch-v1", "content_type": "arm9-native-message-offset-v1",
                      "file_path": arm9_path, "source_file_sha256": hashlib.sha256(canonical_arm9).hexdigest(),
                      "records": offset_records}
    manifest = {"parent_candidate": args.candidate.as_posix(),
                "parent_common_sha256": hashlib.sha256(common).hexdigest(),
                "expected_common_sha256": hashlib.sha256(result.common).hexdigest(),
                "expected_arm9_sha256": hashlib.sha256(result.arm9).hexdigest(),
                "authored_ids": sorted(encoded), "changed_records": sorted(result.changed_records),
                "changed_offsets": sorted(result.changed_offsets), "all_native_entries_compared": len(result.entries),
                "expected_selected_hex": {str(i): raw.hex().upper() for i, raw in encoded.items()}}
    write_json(qa_dir / "repack_manifest.json", manifest)
    if not args.reviewed:
        print(f"QA/repack plan ready: {len(qa_rows)} previews, {len(records)} records, {len(offset_records)} offsets; registration awaits preview review")
        return
    write_json(common_batch, common_payload)
    write_json(offset_batch, offset_payload)
    write_json(Path(f"translations/common_native_repack_manifest_v{version}.json"), manifest)
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    parent = copy.deepcopy(stack["profiles"][args.parent_profile])
    replaced_ids = {row["id"] for row in records}
    batches = []
    for name in parent["batches"]:
        payload = json.loads(Path(name).read_text(encoding="utf-8"))
        original_count = len(payload.get("records", []))
        if payload.get("file_path") == common_path:
            payload["records"] = [row for row in payload["records"] if row["id"] not in replaced_ids]
        elif payload.get("file_path") == arm9_path:
            kept = []
            for row in payload["records"]:
                span = set(range(row["offset"], row["offset"] + len(bytes.fromhex(row["source_hex"]))))
                overlap = span & {pos for offset in result.changed_offsets for pos in (offset, offset + 1)}
                if overlap:
                    if len(span) != 2 or row["offset"] not in result.changed_offsets:
                        raise ValueError("Repack overlaps a larger ARM9 layer")
                else:
                    kept.append(row)
            payload["records"] = kept
        if len(payload.get("records", [])) != original_count:
            # Repeated suffixes exceed Windows' path limit in deep workspaces.
            # A digest identifies the exact parent; retain its path as provenance.
            parent_key = hashlib.sha256(name.encode("utf-8")).hexdigest()[:16]
            filtered = Path("translations") / f"filtered_native_v{version}_{parent_key}.json"
            payload["filtered_from_batch"] = name
            write_json(filtered, payload)
            if payload["records"]:
                batches.append(filtered.as_posix())
        else:
            batches.append(name)
    parent["batches"] = batches + [common_batch.as_posix(), offset_batch.as_posix()]
    parent["note"] = f"Extends {args.parent_profile} with {len(encoded)} faithful native translations and complete block-preserving pointer repacks; runtime pending."
    stack["profiles"][f"all-routes-unified-v{version}"] = parent
    write_json(stack_path, stack)
    print(f"Registered V{version}: {len(encoded)} authored native entries; all {len(result.entries)} selections verified")


if __name__ == "__main__":
    main()
