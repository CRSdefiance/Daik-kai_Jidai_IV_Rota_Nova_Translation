"""Inventory Japanese still present in a saved combined ROM, with clean context."""
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
from scripts.build_translation_progress import load_translated_records

FILE_PATH = "/COMMON/MESFILE.DK4"


def inventory(candidate_path: Path, clean_path: Path, translations: Path) -> dict:
    candidate_bytes = candidate_path.read_bytes()
    candidate_image, clean_image = NdsImage.open(candidate_path), NdsImage.open(clean_path)
    candidate = candidate_image.read_file(FILE_PATH)
    clean = clean_image.read_file(FILE_PATH)
    source_entries = common_message_entries(clean, clean_image.read_file('/__arm9__.bin'))
    current_entries = common_message_entries(candidate, candidate_image.read_file('/__arm9__.bin'), clean=False)
    source_owners = {}
    for source, current in zip(source_entries, current_entries, strict=True):
        if source.message_id != current.message_id:
            raise ValueError('Native global identity changed')
        owner = (current.block, current.record_index)
        previous = source_owners.setdefault(owner, (source.block, source.record_index))
        if previous != (source.block, source.record_index):
            raise ValueError('Current whole record combines distinct source owners')
    current_blocks = IlnkContainer.parse(candidate).blocks
    clean_blocks = IlnkContainer.parse(clean).blocks
    if len(current_blocks) != len(clean_blocks):
        raise ValueError("COMMON block count changed; index comparison is unsafe")
    tracked = load_translated_records(translations)
    classifications: dict[str, list[dict]] = {}
    for path in sorted(translations.glob("common*blocked*.json")):
        batch = json.loads(path.read_text(encoding="utf-8"))
        if batch.get("file_path") != FILE_PATH:
            continue
        for row in batch.get("records", []):
            classifications.setdefault(str(row["id"]), []).append({
                "inventory": path.as_posix(),
                "classification": row.get("classification", "unclassified"),
                "reason": row.get("blocker", row.get("reason", "")),
            })
    records = []
    for block_index, current_block in enumerate(current_blocks):
        current_rows = current_block.split(b"\0")
        for index, raw in enumerate(current_rows):
            text = raw.decode("cp932", errors="replace")
            if not contains_japanese(text):
                continue
            row_id = f"DK4_MES_B{block_index:02d}_R{index:04d}"
            source_owner = source_owners.get((block_index, index))
            if source_owner is None:
                raise ValueError('Japanese-bearing record lacks a verified native source owner')
            source_block, source_index = source_owner
            source_rows = clean_blocks[source_block].split(b'\0')
            source = source_rows[source_index]
            source_id = f'DK4_MES_B{source_block:02d}_R{source_index:04d}'
            records.append({
                "id": row_id,
                "block": block_index,
                "record": index,
                "source_id": source_id,
                "source_length": len(source),
                "current_length": len(raw),
                "source_hex": source.hex().upper(),
                "current_hex": raw.hex().upper(),
                "japanese_source": source.decode("cp932", errors="replace"),
                "current_text": text,
                "changed_from_clean": raw != source,
                "has_translation_record": (FILE_PATH, source_id) in tracked,
                "previous_source": source_rows[source_index - 1].decode("cp932", errors="replace") if source_index else None,
                "next_source": source_rows[source_index + 1].decode("cp932", errors="replace") if source_index + 1 < len(source_rows) else None,
                "prior_classifications": classifications.get(source_id, []),
            })
    return {
        "format": "dk4-current-common-backlog-v1",
        "candidate": candidate_path.as_posix(),
        "candidate_sha256": hashlib.sha256(candidate_bytes).hexdigest(),
        "clean_rom": clean_path.as_posix(),
        "clean_common_sha256": hashlib.sha256(clean).hexdigest(),
        "candidate_common_sha256": hashlib.sha256(candidate).hexdigest(),
        "japanese_bearing_records": len(records),
        "changed_japanese_records": sum(row["changed_from_clean"] for row in records),
        "tracked_but_still_japanese": [row["id"] for row in records if row["has_translation_record"]],
        "counts_by_block": dict(sorted(Counter(row["block"] for row in records).items())),
        "interpretation": "Japanese-bearing records require classification: packed display entries, resource identifiers and partial translations are not interchangeable. Prior classifications are leads, not insertion authorization.",
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--clean", type=Path, default=Path("work/clean.nds"))
    parser.add_argument("--translations", type=Path, default=Path("translations"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = inventory(args.rom, args.clean, args.translations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "records"}, indent=2))


if __name__ == "__main__":
    main()
