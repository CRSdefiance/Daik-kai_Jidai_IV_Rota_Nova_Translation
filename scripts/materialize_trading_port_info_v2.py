from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage


BASE_ROM = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
BASE_SHA256 = "d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf"
ARM9_SHA256 = "249860ab1d29ecfa8e149fd04b5cbff3c3414fb192f81459cfaf469d6c83fa52"
ARM9_LOAD_ADDRESS = 0x02000000

REGIONS = (
    ("NORDIC", 0x15B898, 8, "Nordic"),
    ("PORTUGAL", 0x15D22C, 12, "Portugal"),
    ("SPAIN", 0x15C650, 12, "Spain"),
    ("ITALY", 0x15C668, 12, "Italy"),
    ("GREECE", 0x15C680, 12, "Greece"),
    ("TURKEY", 0x15BE80, 8, "Turkey"),
    ("EGYPT", 0x15C6B0, 12, "Egypt"),
    ("WEST_AFRICA", 0x15D2C8, 12, "West Africa"),
    ("EAST_AFRICA", 0x15D2D4, 12, "East Africa"),
    ("ARAB", 0x15BEB0, 8, "Arab"),
    ("INDIA", 0x15BEC0, 8, "India"),
    ("INDOCHINA", 0x15D334, 12, "Indochina"),
    ("INDONESIA", 0x15DC44, 12, "Indonesia"),
    ("CHINA", 0x15B990, 8, "China"),
    ("KOREA", 0x15B918, 8, "Korea"),
    ("JAPAN", 0x15B9C8, 8, "Japan"),
    ("CARIBBEAN", 0x15C77C, 12, "Caribbean"),
    ("MEXICO", 0x15C788, 12, "Mexico"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_row(record_id: str, arm9: bytes, offset: int, size: int, english: str, context: str) -> dict[str, object]:
    if len(english.encode("ascii")) >= size:
        raise ValueError(f"{record_id}: replacement must leave a terminator")
    return {
        "id": record_id,
        "offset": offset,
        "source_hex": arm9[offset : offset + size].hex().upper(),
        "english": english,
        "context": context,
        "notes": "Source-locked, null-terminated port-information text.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize complete port-information runtime text.")
    parser.add_argument("--rom", type=Path, default=BASE_ROM)
    parser.add_argument(
        "--out", type=Path, default=Path("translations/trading_port_info_arm9_v2.json")
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    arm9 = NdsImage.open(args.rom).read_file("/__arm9__.bin")
    if sha256(arm9) != ARM9_SHA256:
        raise SystemExit("wrong canonical accepted ARM9 component")

    pool_offset = 0x1565E0
    pool_source = arm9[pool_offset : pool_offset + 10]
    if pool_source != b"Prt\0City\0\0":
        raise SystemExit(f"unexpected city-type pool: {pool_source!r}")
    city_pointer_offset = 0x0B5214
    old_city_pointer = struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1565E4)
    if arm9[city_pointer_offset : city_pointer_offset + 4] != old_city_pointer:
        raise SystemExit("unexpected City type pointer")

    rows: list[dict[str, object]] = [
        {
            "id": "DK4_CITY_TYPE_PORT_AND_CITY_POOL_V2",
            "offset": pool_offset,
            "source_hex": pool_source.hex().upper(),
            "replacement_hex": b"Port\0City\0".hex().upper(),
            "context": "Moves City one byte within its own padding so Port can be shown without abbreviation.",
        },
        {
            "id": "DK4_CITY_TYPE_CITY_POINTER_V2",
            "offset": city_pointer_offset,
            "source_hex": old_city_pointer.hex().upper(),
            "replacement_hex": struct.pack("<I", ARM9_LOAD_ADDRESS + 0x1565E5).hex().upper(),
            "context": "Retargets the City value to its one-byte-shifted, terminated string.",
        },
        text_row(
            "DK4_TRADER_SAILOR_NAMEPLATE",
            arm9,
            0x1484D4,
            8,
            "Sailor",
            "Generic sailor portrait nameplate used during trade confirmation.",
        ),
    ]
    for suffix, offset, size, english in REGIONS:
        rows.append(
            text_row(
                f"DK4_PORT_REGION_{suffix}",
                arm9,
                offset,
                size,
                english,
                "Cultural-region name selected by the live port-information table.",
            )
        )

    batch = {
        "format": "dk4-arm9-fixed-text-batch-v1",
        "file_path": "/__arm9__.bin",
        "source_file_sha256": ARM9_SHA256,
        "target_locale": "en-US",
        "scope": "Unabbreviated port type, sailor nameplate, and all 19 live cultural-region names",
        "records": rows,
    }
    args.out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(rows)} port-information records")


if __name__ == "__main__":
    main()
