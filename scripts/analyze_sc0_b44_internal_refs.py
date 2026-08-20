from __future__ import annotations

import argparse
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.inspect_desmume_savestate import (
    ARM9_MAIN_RAM,
    extract_wram,
    unpack_state,
)


def segment_layout(block: bytes) -> tuple[bytes, list[bytes], list[int]]:
    body_size = struct.unpack_from("<H", block, 4)[0]
    logical = block[: 8 + body_size]
    segments = logical.split(b"\0")
    offsets: list[int] = []
    cursor = 0
    for segment in segments:
        offsets.append(cursor)
        cursor += len(segment) + 1
    return logical, segments, offsets


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect possible offset references inside SC0 block 44."
    )
    parser.add_argument("rom", type=Path)
    parser.add_argument("--through-segment", type=int, default=45)
    parser.add_argument("--state", type=Path)
    args = parser.parse_args()

    image = NdsImage.open(args.rom)
    container = IlnkContainer.parse(image.read_file("/data/SC0.DK4"))
    block = container.blocks[44]
    logical, segments, offsets = segment_layout(block)
    offset_set = set(offsets)

    for index, (segment, offset) in enumerate(zip(segments, offsets, strict=True)):
        if index >= args.through_segment:
            break
        text = segment.decode("cp932", errors="replace").encode(
            "unicode_escape"
        ).decode("ascii")
        print(
            f"{index:03d} off=0x{offset:04X} len={len(segment):3d} "
            f"hex={segment.hex()} text={text!r}"
        )

    print("possible aligned 16-bit references to segment starts:")
    for position in range(0, len(logical) - 1, 2):
        value = struct.unpack_from("<H", logical, position)[0]
        if value in offset_set and value >= 8:
            print(
                f"  at 0x{position:04X}: 0x{value:04X} "
                f"-> segment {offsets.index(value)}"
            )

    print("possible aligned 32-bit references to segment starts:")
    for position in range(0, len(logical) - 3, 2):
        value = struct.unpack_from("<I", logical, position)[0]
        if value in offset_set and value >= 8:
            print(
                f"  at 0x{position:04X}: 0x{value:04X} "
                f"-> segment {offsets.index(value)}"
            )

    if args.state:
        wram = extract_wram(unpack_state(args.state))
        prefix = block[:45]
        block_offset = wram.find(prefix)
        if block_offset < 0:
            raise SystemExit("block-44 prefix not found in savestate WRAM")
        following = wram[block_offset + len(block) : block_offset + len(block) + 32]
        next_prefix = container.blocks[45][:32]
        zero_end = block_offset + len(block)
        while zero_end < len(wram) and wram[zero_end] == 0:
            zero_end += 1
        print(
            "runtime block base: "
            f"0x{ARM9_MAIN_RAM + block_offset:08X}; "
            f"bytes after source block match block 45: {following == next_prefix}"
        )
        print(f"runtime bytes after source block: {following.hex()}")
        print(f"SC0 block-45 prefix:            {next_prefix.hex()}")
        print(f"zero bytes available after block: {zero_end - block_offset - len(block)}")


if __name__ == "__main__":
    main()
