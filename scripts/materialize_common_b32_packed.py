"""Audit and encode clean-source B32 entries at their native table offsets."""
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
from dk4tool.script.common_entry_tables import B32_ENTRY_COUNT, B32_TABLE_OFFSET, b32_item_entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign-version", type=int, choices=(1, 2), default=1)
    args = parser.parse_args()
    version = args.campaign_version
    release_version = 93 if version == 1 else 94
    manuscript = Path(f"translations/common_b32_packed_manuscript_v{version}.json")
    authored = json.loads(manuscript.read_text(encoding="utf-8"))
    validate_natural_dialogue_batch(authored)
    clean = NdsImage.open(Path("work/clean.nds"))
    base = NdsImage.open(Path("out/raphael_natural_v2_accepted_base.nds"))
    path = "/COMMON/MESFILE.DK4"
    source = base.read_file(path)
    clean_source = clean.read_file(path)
    arm9 = base.read_file("/__arm9__.bin")
    clean_arm9 = clean.read_file("/__arm9__.bin")
    span = slice(B32_TABLE_OFFSET, B32_TABLE_OFFSET + B32_ENTRY_COUNT * 2)
    if arm9[span] != clean_arm9[span]:
        raise ValueError("canonical B32 native table changed")
    entries = {entry.item_index: entry for entry in b32_item_entries(clean_source, clean_arm9)}
    source_rows = IlnkContainer.parse(source).blocks[32].split(b"\0")
    clean_rows = IlnkContainer.parse(clean_source).blocks[32].split(b"\0")
    profile = get_dialogue_profile("shared")
    out = Path(f"work/qa/common_b32_packed_v{version}")
    out.mkdir(parents=True, exist_ok=True)
    (out / "previews").mkdir(exist_ok=True)
    groups = defaultdict(list)
    report = []
    for row in authored["records"]:
        entry = entries[row["item_index"]]
        raw = source_rows[entry.record_index]
        if bytes.fromhex(row["source_hex"]) != entry.source:
            raise ValueError(f"{row['id']}: manuscript clean source mismatch")
        if raw[entry.start:entry.end] != entry.source and row.get("canonical_record_hex") != raw.hex().upper():
            raise ValueError(f"{row['id']}: translated canonical entry lacks an exact source lock")
        text = row["english"].removesuffix("{PAD}")
        if "{" in text or "\n" in text:
            raise ValueError("native adapter requires plain prose, without authored breaks")
        encoded = text.encode("cp932")
        audit = audit_native_common_entry(entry.source, row["english"])
        formatted = audit["formatted_markup"]
        issues = audit["issues"]
        preview = out / "previews" / f"{row['id']}.png"
        render_dialogue_preview(formatted, profile, preview, arm9=arm9, kanji_font=base.read_file("/GRP/KANJI.FNT"))
        report.append({"id": row["id"], "native_table_offset": entry.table_offset,
                       "source": entry.source.decode("cp932"), "english": text,
                       "entry_start": entry.start, "entry_end": entry.end,
                       "formatted_markup": formatted, "issues": issues,
                       "preview": preview.as_posix()})
        groups[entry.record_index].append((entry, text, encoded))
    blockers = sum(issue["severity"] in {"error", "warning"} for row in report for issue in row["issues"])
    (out / "report.json").write_text(json.dumps({"blockers": blockers, "entries": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if blockers:
        for row in report:
            blocking_issues = [issue for issue in row["issues"] if issue["severity"] in {"error", "warning"}]
            if blocking_issues:
                print(row["id"], blocking_issues)
        raise SystemExit(f"{blockers} unresolved native-entry issues")
    records = []
    for record_index, values in sorted(groups.items()):
        expected = [entry for entry in entries.values() if entry.record_index == record_index]
        if {entry.item_index for entry, _, _ in values} != {entry.item_index for entry in expected}:
            raise ValueError("packed record must include every native entry")
        replacement = bytearray(source_rows[record_index])
        # An older translation may have written its first letter into the
        # alignment byte before the native entry. Restore that clean prefix.
        first_start = min(entry.start for entry, _, _ in values)
        replacement[:first_start] = clean_rows[record_index][:first_start]
        for entry, _, encoded in values:
            replacement[entry.start:entry.end] = encoded.ljust(entry.end - entry.start, b" ")
        records.append({
            "id": f"DK4_MES_B32_R{record_index:04d}",
            "english": " | ".join(text for _, text, _ in values),
            "display_entries": [text for _, text, _ in values],
            "replacement_hex": replacement.hex().upper(),
            "entry_offsets": [entry.start for entry, _, _ in values],
            "entry_ends": [entry.end for entry, _, _ in values],
            "entry_guard_bytes": 0, "linebreak_guard_bytes": 1,
            "translated_ranges": [[entry.start, entry.end] for entry, _, _ in values],
            "text_box_max_chars": 255,
            "native_table_offsets": [entry.table_offset for entry, _, _ in values],
            "safe_literal_latin_glyphs": sorted({character for _, text, _ in values for character in text if character in {"Ｆ", "Ｉ"}}),
            "context": "Source-reviewed item descriptions with ARM9-proven entry offsets.",
            "notes": "Preserves every native offset, source alignment byte and NUL boundary. English uses native automatic wrapping; no stored LF.",
        })
    batch = {
        "format": "dk4-ilnk-translation-batch-v1", "content_type": "common-fixed-dialogue-v2",
        "file_path": path, "source_file_sha256": hashlib.sha256(source).hexdigest(),
        "target_locale": "en-US", "editorial_batch": manuscript.as_posix(),
        "scope": f"Source-reviewed native B32 item campaign version {version}, including exact entry alignment repairs",
        "ascii_guard_exemption": "Uses exact ARM9-selected even block offsets and the established COMMON native automatic wrapper. Retains alignment bytes outside entry spans.",
        "fixed_allocation_policy": "screen-entry-layout-v1", "records": records,
    }
    batch_path = Path(f"translations/common_b32_packed_layout_v{version + 1}.json")
    batch_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    profile_config = dict(stack["profiles"]["all-routes-unified-v91"])
    legacy_path = Path("translations/common_global_layout_v1.json")
    legacy = json.loads(legacy_path.read_text(encoding="utf-8"))
    replacement_ids = {record["id"] for record in records}
    legacy["records"] = [record for record in legacy["records"] if record["id"] not in replacement_ids]
    legacy["scope"] += "; three B32 descriptions superseded by native-pointer-aware repairs"
    filtered_path = Path(f"translations/common_global_layout_v{version + 1}_b32_preserved.json")
    filtered_path.write_text(json.dumps(legacy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    profile_config["batches"] = [filtered_path.as_posix() if path == legacy_path.as_posix() else path for path in profile_config["batches"]]
    if version == 2:
        filtered_paths = []
        for name in profile_config["batches"]:
            payload = json.loads(Path(name).read_text(encoding="utf-8"))
            if payload.get("file_path") == path and any(record.get("id") in replacement_ids for record in payload.get("records", [])):
                payload["records"] = [record for record in payload["records"] if record.get("id") not in replacement_ids]
                payload["scope"] = str(payload.get("scope", "")) + "; superseded B32 entries removed for V94"
                filtered = Path("translations") / f"{Path(name).stem}_b32_v94.json"
                filtered.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                if payload["records"]:
                    filtered_paths.append(filtered.as_posix())
            else:
                filtered_paths.append(name)
        profile_config["batches"] = filtered_paths
    profile_config["batches"] += [batch_path.as_posix()]
    profile_config["note"] = "Full V91 four-route stack plus sixteen newly translated packed item descriptions and three fresh source-reviewed repairs of older B32 entries. Preserves every mapped native pointer. Experimental; runtime verification pending."
    if version == 2:
        profile_config["note"] = "Full four-route stack with all 46 native B32 item-description entries translated and correctly aligned. Experimental; runtime verification pending."
    stack["profiles"][f"all-routes-unified-v{release_version}"] = profile_config
    stack_path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Registered V{release_version}: {len(report)} entries, {len(records)} records, zero QA blockers")


if __name__ == "__main__":
    main()
