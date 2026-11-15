"""Apply the established COMMON native-wrap adapter to reviewed B32 prose."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_entry_tables import b32_item_entries
from dk4tool.script.mesfile import iter_mesfile_records


def main() -> None:
    prose_path = Path("translations/common_remaining_b32_single_v1.json")
    prose = json.loads(prose_path.read_text(encoding="utf-8"))
    validate_natural_dialogue_batch(prose)
    source = NdsImage.open(Path("out/raphael_natural_v2_accepted_base.nds")).read_file(prose["file_path"])
    if hashlib.sha256(source).hexdigest() != prose["source_file_sha256"]:
        raise ValueError("prose source lock mismatch")
    by_id = {r.row_id: r for r in iter_mesfile_records(source, include_non_japanese=True)}
    clean_rom = NdsImage.open(Path("work/clean.nds"))
    entry_map = b32_item_entries(clean_rom.read_file(prose["file_path"]), clean_rom.read_file("/__arm9__.bin"))
    records = []
    for row in prose["records"]:
        raw = by_id[row["id"]].raw_bytes
        audit = audit_fixed_dialogue_record(raw, row["english"], get_dialogue_profile(prose["dialogue_profile"]))
        if any(issue["severity"] in {"error", "warning"} for issue in audit["issues"]):
            raise ValueError(f"{row['id']}: unresolved prose QA")
        text = row["english"].removesuffix("{PAD}")
        if "{" in text or "\n" in text:
            raise ValueError("native-wrap adapter requires plain, single-entry prose")
        native_entries = [entry for entry in entry_map if entry.record_index == by_id[row["id"]].segment_index]
        if len(native_entries) != 1:
            raise ValueError("single-entry adapter encountered a packed record")
        entry = native_entries[0]
        encoded = text.encode("ascii")
        if len(encoded) > entry.end - entry.start:
            raise ValueError("native-wrap allocation overflow")
        replacement = raw[:entry.start] + encoded.ljust(entry.end - entry.start, b" ") + raw[entry.end:]
        records.append({
            "id": row["id"], "english": text, "display_entries": [text],
            "replacement_hex": replacement.hex().upper(),
            "entry_offsets": [entry.start], "entry_ends": [entry.end],
            "entry_guard_bytes": 0, "linebreak_guard_bytes": 1,
            "translated_ranges": [[entry.start, entry.end]], "text_box_max_chars": 255,
            "context": row["context"], "source_meaning": row["source_meaning"],
            "native_table_offset": entry.table_offset,
            "native_block_offset": entry.block_offset,
            "notes": "Native automatic wrapping with the exact ARM9-selected entry. Alignment bytes preceding the native entry remain outside its text span.",
        })
    result = {
        "format": "dk4-ilnk-translation-batch-v1", "content_type": "common-fixed-dialogue-v2",
        "file_path": prose["file_path"], "source_file_sha256": prose["source_file_sha256"],
        "target_locale": "en-US", "scope": "Native-wrap layout for seven reviewed B32 descriptions",
        "editorial_batch": prose_path.as_posix(),
        "ascii_guard_exemption": "Uses the established COMMON native automatic wrapping adapter; exact single-entry allocations are preserved without stored continuation bytes.",
        "fixed_allocation_policy": "screen-entry-layout-v1", "records": records,
    }
    Path("translations/common_remaining_b32_layout_v2.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stack_path = Path("translations/release_stack.json")
    stack = json.loads(stack_path.read_text(encoding="utf-8"))
    profile = dict(stack["profiles"]["all-routes-unified-v89"])
    # The layout adapter contains the final bytes for the same seven IDs.
    # Keep the editorial manuscript as its audited input, not a second layer.
    profile["batches"] = profile["batches"] + ["translations/common_remaining_b32_layout_v2.json"]
    profile["note"] = "Complete four-route V89 stack plus seven source-reviewed residual COMMON B32 descriptions and the established native automatic wrapping adapter. Experimental; runtime acceptance pending."
    profile["note"] += " B32 native table offsets are now explicit; preserves the one-byte source alignment before six descriptions. Supersedes V90."
    stack["profiles"]["all-routes-unified-v91"] = profile
    stack_path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Registered all-routes-unified-v91 with {len(records)} descriptions at native entry offsets")


if __name__ == "__main__":
    main()
