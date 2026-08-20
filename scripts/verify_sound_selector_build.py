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
    BGM_TAIL_OFFSET,
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
    title_map = bgm_batch.get("pointer_map")
    if not isinstance(title_map, list):
        raise SystemExit("BGM batch does not contain its pointer map")
    if len(pointers) != len(title_map):
        raise SystemExit("BGM pointer/title count mismatch")
    block = container.blocks[BGM_BLOCK]
    for pointer, title in zip(pointers, title_map, strict=True):
        expected_offset = int(title["new_offset"])
        expected = str(title["english"]).encode("ascii")
        if pointer != expected_offset:
            raise SystemExit(f"BGM pointer for {title['english']!r} is {pointer:#x}; expected {expected_offset:#x}")
        if block[pointer : pointer + len(expected)] != expected:
            raise SystemExit(f"BGM title {title['english']!r} does not match at {pointer:#x}")
    if pointers[-1] >= BGM_TAIL_OFFSET:
        raise SystemExit("final BGM title pointer reaches the protected tail")

    print(f"sound selector verified: {len(title_map)} BGM + {len(arm9_batch['records']) - 1} SFX titles")
    print(f"BGM pointer table: {BGM_POINTER_TABLE_OFFSET:#x}, terminal offset {BGM_TAIL_OFFSET}")


if __name__ == "__main__":
    main()
