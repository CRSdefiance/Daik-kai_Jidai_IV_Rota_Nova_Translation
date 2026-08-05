from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.build_sound_selector_batches import (
    BGM_BLOCK,
    BGM_POINTER_TABLE_OFFSET,
    BGM_RECORDS,
    BGM_TAIL_OFFSET,
    encode_fullwidth_label,
)


ARM9_BATCH = Path("translations/sound_selector_arm9.json")
BGM_BATCH = Path("translations/sound_bgm_titles.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify the complete English sound selector.")
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    image = NdsImage.open(args.candidate)
    arm9 = image.read_file("/__arm9__.bin")
    mesfile = image.read_file("/COMMON/MESFILE.DK4")
    arm9_batch = json.loads(ARM9_BATCH.read_text(encoding="utf-8"))
    bgm_batch = json.loads(BGM_BATCH.read_text(encoding="utf-8"))

    pointer_record = arm9_batch["records"][0]
    pointer_bytes = bytes.fromhex(pointer_record["replacement_hex"])
    pointer_offset = int(pointer_record["offset"])
    if arm9[pointer_offset : pointer_offset + len(pointer_bytes)] != pointer_bytes:
        raise SystemExit("candidate BGM interior pointer table does not match the batch")

    for record in arm9_batch["records"][1:]:
        offset = int(record["offset"])
        slot_size = len(bytes.fromhex(record["source_hex"]))
        expected = record["english"].encode("ascii").ljust(slot_size, b"\0")
        if arm9[offset : offset + slot_size] != expected:
            raise SystemExit(f"candidate SFX slot {record['id']} does not match")

    container = IlnkContainer.parse(mesfile)
    records = container.blocks[BGM_BLOCK].split(b"\0")
    for record in bgm_batch["records"]:
        index = int(record["id"].rsplit("R", 1)[1])
        expected = bytes.fromhex(record["replacement_hex"])
        if records[index] != expected:
            raise SystemExit(f"candidate BGM record {record['id']} does not match")

    pointers = [
        struct.unpack_from("<H", pointer_bytes, offset)[0]
        for offset in range(0, len(pointer_bytes), 2)
    ]
    expected_titles = [
        (english, encode_fullwidth_label(english, len(japanese.encode("cp932")) // 2))
        for spec in BGM_RECORDS
        for japanese, english in spec.titles
    ]
    if len(pointers) != len(expected_titles):
        raise SystemExit("BGM pointer/title count mismatch")
    if any(pointer % 2 for pointer in pointers):
        raise SystemExit("candidate contains an odd-aligned BGM interior pointer")
    block = container.blocks[BGM_BLOCK]
    boundaries = pointers[1:] + [BGM_TAIL_OFFSET]
    for start, end, (title, expected) in zip(
        pointers, boundaries, expected_titles, strict=True
    ):
        raw = block[start:end].split(b"\0", 1)[0]
        if raw != expected:
            raise SystemExit(
                f"BGM title {title!r} does not occupy its exact double-byte cell range"
            )

    print(f"sound selector verified: {len(expected_titles)} BGM + {len(arm9_batch['records']) - 1} SFX titles")
    print(f"BGM pointer table: {BGM_POINTER_TABLE_OFFSET:#x}, terminal offset {BGM_TAIL_OFFSET}")


if __name__ == "__main__":
    main()
