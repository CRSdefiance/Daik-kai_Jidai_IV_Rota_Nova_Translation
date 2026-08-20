"""Locate byte strings in ARM9 RAM stored in a DeSmuME 0.9.13 savestate."""

from __future__ import annotations

import argparse
import struct
import zlib
from pathlib import Path

MAGIC = b"DeSmuME SState\x00\x00"
ARM9_MAIN_RAM = 0x02000000


def read_u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def unpack_state(path: Path) -> bytes:
    data = path.read_bytes()
    if not data.startswith(MAGIC):
        raise ValueError(f"not a DeSmuME savestate: {path}")
    return zlib.decompress(data[32:])


def extract_wram(state: bytes) -> bytes:
    cursor = 0
    while cursor + 8 <= len(state):
        chunk_type, chunk_size = struct.unpack_from("<II", state, cursor)
        cursor += 8
        if chunk_type == 0xFFFFFFFF:
            break
        chunk_end = cursor + chunk_size
        if chunk_type == 4:
            while cursor + 12 <= chunk_end:
                tag = state[cursor : cursor + 4]
                item_size, count = struct.unpack_from("<II", state, cursor + 4)
                cursor += 12
                payload_size = item_size * count
                if tag == b"WRAM":
                    return state[cursor : cursor + payload_size]
                cursor += payload_size
            break
        cursor = chunk_end
    raise ValueError("WRAM record not found in savestate")


def find_all(haystack: bytes, needle: bytes) -> list[int]:
    hits: list[int] = []
    cursor = 0
    while (hit := haystack.find(needle, cursor)) >= 0:
        hits.append(hit)
        cursor = hit + 1
    return hits


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("state", type=Path)
    parser.add_argument("text", nargs="+", help="ASCII strings to locate")
    args = parser.parse_args()

    wram = extract_wram(unpack_state(args.state))
    for text in args.text:
        hits = find_all(wram, text.encode("ascii"))
        addresses = ", ".join(f"0x{ARM9_MAIN_RAM + hit:08X}" for hit in hits)
        print(f"{text!r}: {addresses or 'not found'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
