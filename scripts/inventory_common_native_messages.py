"""Inventory remaining COMMON text at the actual native message pointers."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.common_message_table import common_message_entries


def inventory(candidate: Path, clean_rom: Path) -> dict:
    clean_image, current_image = NdsImage.open(clean_rom), NdsImage.open(candidate)
    clean_entries = common_message_entries(clean_image.read_file("/COMMON/MESFILE.DK4"),
                                           clean_image.read_file("/__arm9__.bin"))
    current_entries = common_message_entries(current_image.read_file("/COMMON/MESFILE.DK4"),
                                             current_image.read_file("/__arm9__.bin"), clean=False)
    rows = []
    changed_offsets = []
    leading_findings = []
    blank_findings = []
    source_blocks = IlnkContainer.parse(clean_image.read_file("/COMMON/MESFILE.DK4")).blocks
    current_blocks = IlnkContainer.parse(current_image.read_file("/COMMON/MESFILE.DK4")).blocks
    for source, current in zip(clean_entries, current_entries, strict=True):
        if source.message_id != current.message_id:
            raise ValueError("Native message identity changed")
        if (source.block, source.block_offset) != (current.block, current.block_offset):
            changed_offsets.append(current.message_id)
        text = current.text.decode("cp932")
        if source.text.strip(b' \n\r\t') and not text.strip(" \n\r\t"):
            blank_findings.append({
                "message_id": current.message_id, "block": current.block,
                "record": current.record_index, "source_hex": source.text.hex().upper(),
                "japanese_source": source.text.decode("cp932"),
                "native_start": current.start, "native_end": current.end,
                "interpretation": "Clean native message contains visible content, including punctuation; current native selection is blank. Translation/repair required.",
            })
        if source.start in (1, 2) and current.start in (1, 2):
            source_record = source_blocks[source.block].split(b"\0")[source.record_index]
            current_record = current_blocks[current.block].split(b"\0")[current.record_index]
            prefix = current_record[:current.start]
            if (not source_record[:source.start].strip(b" ")
                    and all(32 <= byte < 127 for byte in prefix)
                    and any(65 <= byte <= 90 or 97 <= byte <= 122 for byte in prefix)):
                leading_findings.append({
                    "message_id": current.message_id, "block": current.block,
                    "record": current.record_index, "native_start": current.start,
                    "prefix_hex": prefix.hex().upper(),
                    "record_text": current_record.decode("cp932"), "selected_text": text,
                    "interpretation": "Printable English precedes the native pointer where clean source has only alignment spaces; repair/review required.",
                })
        if contains_japanese(text):
            rows.append({
                "message_id": current.message_id, "block": current.block,
                "table_offset": current.table_offset, "block_offset": current.block_offset,
                "copy_end": current.copy_end, "record": current.record_index,
                "start": current.start, "end": current.end,
                "source_hex": source.text.hex().upper(), "japanese_source": source.text.decode("cp932"),
                "current_hex": current.text.hex().upper(), "current_text": text,
            })
    return {
        "format": "dk4-native-common-backlog-v1", "candidate": candidate.as_posix(),
        "candidate_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
        "native_message_count": len(current_entries), "japanese_bearing_entries": len(rows),
        "changed_native_offsets": changed_offsets,
        "odd_native_offsets": [entry.message_id for entry in current_entries if entry.block_offset % 2],
        "leading_prefix_finding_count": len(leading_findings),
        "leading_prefix_findings": leading_findings,
        "blank_native_message_count": len(blank_findings),
        "blank_native_messages": blank_findings,
        "counts_by_block": dict(sorted(Counter(row["block"] for row in rows).items())),
        "interpretation": "Proven loader boundaries establish message spans; player visibility and resource use still require classification.",
        "entries": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--clean", type=Path, default=Path("work/clean.nds"))
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = inventory(args.candidate, args.clean)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {"entries", "leading_prefix_findings", "blank_native_messages"}}, indent=2))


if __name__ == "__main__":
    main()
