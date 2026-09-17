from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

BASE_ROM = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
CLEAN_COMMON = Path("work/files/COMMON/MESFILE.DK4")
OUTPUT = Path("translations/common_placeholder_source_restore_v1.json")
FILE_PATH = "/COMMON/MESFILE.DK4"
OVERRIDE_BATCHES = (
    Path("translations/common_crew_join_wrap_v3.json"),
    Path("translations/common_square_shipyard_repair_v1.json"),
)

OK_TOKEN = re.compile(rb"(?<![a-z])ok(?![a-z])", re.IGNORECASE)
SEE_BELOW = b"see below"
CAPTAIN_FALLBACK = b"give the order from the captain's cabin."


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _records(data: bytes) -> list[list[bytes]]:
    return [block.split(b"\0") for block in IlnkContainer.parse(data).blocks]


def _placeholder_tags(record: bytes) -> list[str]:
    lowered = record.lower()
    tags: list[str] = []
    if OK_TOKEN.search(lowered):
        tags.append("literal ok")
    if SEE_BELOW in lowered:
        tags.append("see below")
    if CAPTAIN_FALLBACK in lowered:
        tags.append("unrelated captain-cabin fallback")
    return tags


def _overridden_ids() -> set[str]:
    ids: set[str] = set()
    for path in OVERRIDE_BATCHES:
        batch = json.loads(path.read_text(encoding="utf-8"))
        ids.update(str(record["id"]) for record in batch["records"])
    return ids


def materialize(base_rom: Path, clean_common: Path) -> dict[str, object]:
    accepted = NdsImage.open(base_rom).read_file(FILE_PATH)
    clean = clean_common.read_bytes()
    accepted_records = _records(accepted)
    clean_records = _records(clean)
    if [len(block) for block in accepted_records] != [len(block) for block in clean_records]:
        raise ValueError("accepted and clean COMMON record layouts differ")

    overridden = _overridden_ids()
    records: list[dict[str, object]] = []
    tag_counts: dict[str, int] = {}
    for block_index, (accepted_block, clean_block) in enumerate(
        zip(accepted_records, clean_records, strict=True)
    ):
        for record_index, (accepted_record, clean_record) in enumerate(
            zip(accepted_block, clean_block, strict=True)
        ):
            tags = _placeholder_tags(accepted_record)
            if not tags:
                continue
            record_id = f"DK4_MES_B{block_index:02d}_R{record_index:04d}"
            if record_id in overridden:
                continue
            if len(accepted_record) != len(clean_record):
                raise ValueError(f"{record_id}: clean allocation length changed")
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            records.append(
                {
                    "id": record_id,
                    "english": "Original Japanese restored; English translation pending.",
                    "replacement_hex": clean_record.hex().upper(),
                    "status": "source-restored",
                    "context": f"Shared gameplay block {block_index}, record {record_index}.",
                    "notes": (
                        "Removed misleading early-pass filler ("
                        + ", ".join(tags)
                        + ") while preserving the original allocation, controls, macros, "
                        "and packed internal entry points."
                    ),
                }
            )

    return {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "ilnk-source-restored-placeholder-cleanup-v1",
        "file_path": FILE_PATH,
        "source_file_sha256": _sha256(accepted),
        "target_locale": "ja-JP-source-safety",
        "scope": "All remaining known generic fallback records in accepted COMMON",
        "policy": (
            "Restore exact clean Japanese bytes wherever the early bulk pass inserted "
            "generic filler. Later source-faithful English batches intentionally override "
            "excluded records."
        ),
        "placeholder_counts": tag_counts,
        "override_batches": [path.as_posix() for path in OVERRIDE_BATCHES],
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Materialize exact-source restoration for generic COMMON fallbacks."
    )
    parser.add_argument("--base", type=Path, default=BASE_ROM)
    parser.add_argument("--clean-common", type=Path, default=CLEAN_COMMON)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = materialize(args.base, args.clean_common)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(payload['records'])} restored records to {args.out}")
    print(json.dumps(payload["placeholder_counts"], sort_keys=True))


if __name__ == "__main__":
    main()
