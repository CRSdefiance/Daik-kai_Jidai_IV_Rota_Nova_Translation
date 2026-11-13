"""Preserve raw portrait interpretations and bounded paired-section evidence."""

import hashlib
import json
import struct
from itertools import pairwise
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE = Path("out/all_routes_combined_v189_candidate.nds")
ROOT = Path("work/qa/embedded_masks_v190")
REPORT = Path("work/analysis/embedded_structures_v190.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def paired_sections(data):
    first_table, extent = struct.unpack_from("<2I", data)
    second_start = 4 + extent
    assert first_table == 8 and extent % 4 == 0 and 12 < second_start < len(data)
    first_offset = struct.unpack_from("<I", data, 8)[0]
    assert first_offset % 4 == 0 and 4 <= first_offset <= second_start - 8
    count = first_offset // 4
    first_stored = list(struct.unpack_from(f"<{count}I", data, 8))
    second_stored = list(struct.unpack_from(f"<{count}I", data, second_start))
    assert first_stored[0] == second_stored[0] == 4 * count
    groups = []
    rebuilt = bytearray(data[:8])
    for start, end, stored in ((8, second_start, first_stored), (second_start, len(data), second_stored)):
        # Native 02008A10 adds the table entry's own index*4 origin.
        offsets = [value + index * 4 for index, value in enumerate(stored)]
        assert all(left < right for left, right in pairwise(offsets))
        assert offsets[-1] < end - start
        limits = offsets + [end - start]
        payloads = [data[start + left : start + right] for left, right in pairwise(limits)]
        table = struct.pack(f"<{count}I", *stored)
        assert table + b"".join(payloads) == data[start:end]
        rebuilt.extend(table)
        rebuilt.extend(b"".join(payloads))
        groups.append({
            "table_start": start,
            "section_end_exclusive": end,
            "relative_offsets": offsets,
            "stored_self_relative_offsets": stored,
            "offset_origin": "each entry's own address, as executed by native 02008A10",
            "payloads": [{"bytes": len(payload), "sha256": sha(payload)} for payload in payloads],
        })
    assert bytes(rebuilt) == data
    return {"first_table_offset": first_table, "second_table_self_relative_offset": extent, "paired_records": count, "groups": groups, "whole_block_roundtrip_exact": True, "native_self_relative_entry_origin_applied": True}


def main():
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(CANDIDATE.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    base, candidate = NdsImage.open(BASE), NdsImage.open(CANDIDATE)
    ROOT.mkdir(parents=True, exist_ok=True)
    source = IlnkContainer.parse(base.read_file("/GRP/SLACKIMG.DK4")).blocks
    saved = IlnkContainer.parse(candidate.read_file("/GRP/SLACKIMG.DK4")).blocks
    portraits = []
    sheet = Image.new("RGB", (960, 340), "#333333")
    draw = ImageDraw.Draw(sheet)
    for index, block in enumerate((14, 15, 16, 17)):
        raw = source[block]
        assert len(raw) == 104 * 136 and saved[block] == raw
        preview = Image.frombytes("L", (104, 136), raw)
        assert preview.tobytes() == raw
        path = ROOT / f"block{block}_104x136.png"
        preview.save(path)
        assert Image.open(path).tobytes() == raw
        x = index * 240
        draw.text((x + 4, 4), f"Raw block {block}: L interpretation", fill="white")
        sheet.paste(preview.resize((208, 272), Image.Resampling.NEAREST), (x + 4, 24))
        portraits.append({
            "path": "/GRP/SLACKIMG.DK4",
            "block_index": block,
            "source_block_sha256": sha(raw),
            "bytes": len(raw),
            "hypothesis_dimensions": [104, 136],
            "display_interpretation": "One byte per pixel displayed as grayscale L; native palette/encoding unknown.",
            "preview": str(path),
            "preview_sha256": sha(path.read_bytes()),
            "whole_block_byte_roundtrip_exact": True,
            "candidate_block_unchanged": True,
            "visual_review": "pending",
            "native_geometry_palette_usage_proved": False,
        })
    sheet_path = ROOT / "portrait_review.png"
    sheet.save(sheet_path)
    source = IlnkContainer.parse(base.read_file("/GRP/CHARA.DK4")).blocks
    saved = IlnkContainer.parse(candidate.read_file("/GRP/CHARA.DK4")).blocks
    structures = []
    for index in range(6, 14):
        raw = source[index]
        assert raw == saved[index]
        row = paired_sections(raw)
        row.update({"path": "/GRP/CHARA.DK4", "block_index": index, "source_block_sha256": sha(raw), "bytes": len(raw), "candidate_block_unchanged": True, "encoding_and_native_semantics_proved": False})
        structures.append(row)
    result = {
        "status": "bounded-storage-evidence-native-format-unproved",
        "canonical_base_sha256": sha(BASE.read_bytes()),
        "candidate_sha256": sha(CANDIDATE.read_bytes()),
        "raw_portraits": portraits,
        "portrait_review_sheet": str(sheet_path),
        "portrait_review_sheet_sha256": sha(sheet_path.read_bytes()),
        "paired_section_blocks": structures,
        "paired_subrecords": sum(row["paired_records"] for row in structures),
        "image_encoding_not_inferred_from_first_payload_bytes": True,
        "historical_unclassified_counts_unchanged": True,
        "rom_changed": False,
    }
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Saved four complete portrait interpretations and eight exact paired-section structures.")
    print("Paired records:", result["paired_subrecords"], "; native encoding and all runtime gates remain open.")


if __name__ == "__main__":
    main()
