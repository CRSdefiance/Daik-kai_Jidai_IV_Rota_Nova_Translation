"""Build reviewed B29-B31 item descriptions at source-locked native pointers."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.dialogue.preview import render_dialogue_preview
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_entry_tables import ITEM_TABLES, native_item_entries


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--block", type=int, choices=(29, 30, 31), required=True)
    parser.add_argument("--release-version", type=int, required=True)
    parser.add_argument("--parent-profile", required=True)
    parser.add_argument("--manuscript-version", type=int, default=1)
    args = parser.parse_args()
    block = args.block
    version = args.release_version
    manuscript_version = args.manuscript_version
    manuscript = Path(f"translations/common_b{block}_manuscript_v{manuscript_version}.json")
    authored = json.loads(manuscript.read_text(encoding="utf-8"))
    validate_natural_dialogue_batch(authored)
    clean = NdsImage.open("work/clean.nds")
    base = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    file_path = "/COMMON/MESFILE.DK4"
    clean_common = clean.read_file(file_path)
    canonical_common = base.read_file(file_path)
    arm9 = base.read_file("/__arm9__.bin")
    clean_arm9 = clean.read_file("/__arm9__.bin")
    table_offset, count, _, _, _ = ITEM_TABLES[block]
    span = slice(table_offset, table_offset + count * 2)
    if arm9[span] != clean_arm9[span]:
        raise ValueError("canonical native item table changed")
    entries = native_item_entries(clean_common, clean_arm9, block)
    if {row["item_index"] for row in authored["records"]} != {entry.item_index for entry in entries}:
        raise ValueError("manuscript must account for every native item")
    by_item = {entry.item_index: entry for entry in entries}
    canonical_rows = IlnkContainer.parse(canonical_common).blocks[block].split(b"\0")
    clean_rows = IlnkContainer.parse(clean_common).blocks[block].split(b"\0")
    qa_dir = Path(f"work/qa/common_b{block}_native_v{manuscript_version}")
    groups = defaultdict(list)
    report = []
    for row in authored["records"]:
        entry = by_item[row["item_index"]]
        raw = canonical_rows[entry.record_index]
        if bytes.fromhex(row["source_hex"]) != entry.source:
            raise ValueError(f"{row['id']}: clean entry source mismatch")
        if raw[entry.start:entry.end] != entry.source and row.get("canonical_record_hex") != raw.hex().upper():
            raise ValueError(f"{row['id']}: canonical source lock missing")
        text = row["english"].removesuffix("{PAD}")
        audit = audit_native_common_entry(entry.source, row["english"])
        preview = qa_dir / "previews" / f"{row['id']}.png"
        render_dialogue_preview(audit["formatted_markup"], get_dialogue_profile("shared"), preview,
                                arm9=arm9, kanji_font=base.read_file("/GRP/KANJI.FNT"))
        report.append({"id": row["id"], "source": entry.source.decode("cp932"), "english": text,
                       "native_table_offset": entry.table_offset, "entry_start": entry.start,
                       "entry_end": entry.end, "formatted_markup": audit["formatted_markup"],
                       "issues": audit["issues"], "preview": preview.as_posix()})
        groups[entry.record_index].append((entry, text))
    blockers = sum(issue["severity"] in {"error", "warning"} for row in report for issue in row["issues"])
    write_json(qa_dir / "report.json", {"blockers": blockers, "entries": report})
    if blockers:
        raise ValueError(f"{blockers} native QA blockers; inspect {qa_dir}")
    records = []
    for record_index, group in sorted(groups.items()):
        group.sort(key=lambda pair: pair[0].start)
        replacement = bytearray(canonical_rows[record_index])
        first = group[0][0].start
        replacement[:first] = clean_rows[record_index][:first]
        for entry, text in group:
            replacement[entry.start:entry.end] = text.encode("cp932").ljust(entry.end - entry.start, b" ")
        records.append({
            "id": f"DK4_MES_B{block:02d}_R{record_index:04d}",
            "english": " | ".join(text for _, text in group),
            "display_entries": [text for _, text in group], "replacement_hex": replacement.hex().upper(),
            "entry_offsets": [entry.start for entry, _ in group],
            "entry_ends": [entry.end for entry, _ in group],
            "translated_ranges": [[entry.start, entry.end] for entry, _ in group],
            "native_table_offsets": [entry.table_offset for entry, _ in group],
            "entry_guard_bytes": 0, "linebreak_guard_bytes": 1, "text_box_max_chars": 255,
            "safe_literal_latin_glyphs": sorted({c for _, text in group for c in text if c in {"Ｆ", "Ｉ"}}),
            "context": "Clean-source item descriptions with native ARM9 entry mapping.",
            "notes": "Preserves native pointers, source alignment and NUL boundaries; native automatic wrapping.",
        })
    batch_path = Path(f"translations/common_b{block}_native_layout_v{manuscript_version}.json")
    write_json(batch_path, {
        "format": "dk4-ilnk-translation-batch-v1", "content_type": "common-fixed-dialogue-v2",
        "file_path": file_path, "source_file_sha256": hashlib.sha256(canonical_common).hexdigest(),
        "target_locale": "en-US", "editorial_batch": manuscript.as_posix(),
        "scope": f"All {count} source-reviewed native B{block} item descriptions",
        "fixed_allocation_policy": "screen-entry-layout-v1",
        "ascii_guard_exemption": "Source-locked even block offsets with native automatic wrapping; preserves source alignment.",
        "records": records,
    })
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    profile = dict(stack["profiles"][args.parent_profile])
    replacement_ids = {record["id"] for record in records}
    batches = []
    for name in profile["batches"]:
        payload = json.loads(Path(name).read_text(encoding="utf-8"))
        if payload.get("file_path") == file_path and any(row.get("id") in replacement_ids for row in payload.get("records", [])):
            payload["records"] = [row for row in payload["records"] if row.get("id") not in replacement_ids]
            payload["scope"] = str(payload.get("scope", "")) + f"; B{block} superseded by native pointer-aware V{version}"
            filtered = Path("translations") / f"{Path(name).stem}_b{block}_v{version}.json"
            write_json(filtered, payload)
            if payload["records"]:
                batches.append(filtered.as_posix())
        else:
            batches.append(name)
    profile["batches"] = batches + [batch_path.as_posix()]
    profile["note"] = f"Complete {args.parent_profile} stack plus all native B{block} item descriptions. Experimental; runtime pending."
    stack["profiles"][f"all-routes-unified-v{version}"] = profile
    write_json(stack_path, stack)
    print(f"Registered V{version}: {len(report)} native entries, {len(records)} records, zero QA blockers")


if __name__ == "__main__":
    main()
