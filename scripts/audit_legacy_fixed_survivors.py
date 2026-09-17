from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch


DEFAULT_ROM = Path("out/hodram_market_inn_sea_v2_candidate.nds")
CLEAN_COMMON = Path("work/files/COMMON/MESFILE.DK4")
LEGACY_BATCH = Path("translations/common_shared_50pct.json")
DEFAULT_OUTPUT = Path("out/hodram_market_inn_sea_v2_legacy_fixed_audit.json")
FILE_PATH = "/COMMON/MESFILE.DK4"


def _records(data: bytes) -> list[list[bytes]]:
    return [block.split(b"\0") for block in IlnkContainer.parse(data).blocks]


def audit(rom: Path, clean_common: Path, legacy_batch: Path) -> dict[str, object]:
    clean = clean_common.read_bytes()
    batch = json.loads(legacy_batch.read_text(encoding="utf-8"))
    legacy = rebuild_mesfile(clean, materialize_translation_batch(batch, clean))
    current = NdsImage.open(rom).read_file(FILE_PATH)
    clean_records = _records(clean)
    legacy_records = _records(legacy)
    current_records = _records(current)

    survivors: list[dict[str, object]] = []
    for row in batch["records"]:
        record_id = str(row["id"])
        tail = record_id.split("_B", 1)[1]
        block_text, record_text = tail.split("_R", 1)
        block = int(block_text)
        record = int(record_text)
        if legacy_records[block][record] != current_records[block][record]:
            continue
        survivors.append(
            {
                "id": record_id,
                "block": block,
                "record": record,
                "allocation_bytes": len(clean_records[block][record]),
                "legacy_english": str(row["english"]),
                "clean_japanese": clean_records[block][record].decode("cp932", "replace"),
                "current_hex": current_records[block][record].hex().upper(),
            }
        )

    blocks = Counter(int(row["block"]) for row in survivors)
    phrases = Counter(str(row["legacy_english"]) for row in survivors)
    return {
        "format": "dk4-legacy-fixed-survivor-audit-v1",
        "rom": rom.as_posix(),
        "legacy_batch": legacy_batch.as_posix(),
        "clean_source": clean_common.as_posix(),
        "legacy_record_count": len(batch["records"]),
        "survivor_count": len(survivors),
        "survivors_by_block": {str(key): value for key, value in sorted(blocks.items())},
        "survivors_by_legacy_phrase": [
            {"legacy_english": phrase, "count": count}
            for phrase, count in phrases.most_common()
        ],
        "records": survivors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find COMMON records still byte-identical to the legacy fixed-allocation pass."
    )
    parser.add_argument("--rom", type=Path, default=DEFAULT_ROM)
    parser.add_argument("--clean-common", type=Path, default=CLEAN_COMMON)
    parser.add_argument("--legacy-batch", type=Path, default=LEGACY_BATCH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report = audit(args.rom, args.clean_common, args.legacy_batch)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"{report['survivor_count']} of {report['legacy_record_count']} legacy "
        f"fixed-allocation records remain; wrote {args.out}"
    )


if __name__ == "__main__":
    main()
