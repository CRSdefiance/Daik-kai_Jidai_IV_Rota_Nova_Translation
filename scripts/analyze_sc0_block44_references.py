from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.inspect_desmume_savestate import (
    ARM9_MAIN_RAM,
    extract_wram,
    unpack_state,
)

CANONICAL_ROM_SHA256 = (
    "8e61fd4e8c444b25566cc273dd676b3e5bea5d683ad167db2f92444c10df9764"
)
SC0_SHA256 = "2daae625c81572e02b62b91f11ad1a6138eff05bceb66dd74231be9d0fb74c21"
SC0_PATH = "/data/SC0.DK4"
BLOCK_INDEX = 44
MESSAGE_COMMAND = b"\x40\xFF\xFF"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_all(data: bytes, needle: bytes) -> list[int]:
    hits: list[int] = []
    cursor = 0
    while (hit := data.find(needle, cursor)) >= 0:
        hits.append(hit)
        cursor = hit + 1
    return hits


def segment_layout(block: bytes) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    cursor = 0
    segments = block.split(b"\0")
    for index, segment in enumerate(segments):
        records.append(
            {
                "segment_index": index,
                "offset": cursor,
                "length": len(segment),
                "message_text": index > 0 and segments[index - 1] == MESSAGE_COMMAND,
            }
        )
        cursor += len(segment) + (1 if index < len(segments) - 1 else 0)
    return records


def scan_runtime_pointers(wram: bytes, start: int, end: int) -> list[dict[str, object]]:
    pointers: list[dict[str, object]] = []
    for offset in range(len(wram) - 3):
        value = struct.unpack_from("<I", wram, offset)[0]
        if start <= value < end:
            pointers.append(
                {
                    "stored_at": f"0x{ARM9_MAIN_RAM + offset:08X}",
                    "points_to": f"0x{value:08X}",
                    "block_offset": value - start,
                    "storage_aligned": offset % 4 == 0,
                }
            )
    return pointers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory static and savestate-visible references to SC0 block 44."
    )
    parser.add_argument("rom", type=Path)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    rom_bytes = args.rom.read_bytes()
    if sha256(rom_bytes) != CANONICAL_ROM_SHA256:
        raise SystemExit("ROM is not the canonical integration baseline")
    image = NdsImage.open(args.rom)
    sc0 = image.read_file(SC0_PATH)
    if sha256(sc0) != SC0_SHA256:
        raise SystemExit("canonical SC0 source hash mismatch")

    container = IlnkContainer.parse(sc0)
    block = container.blocks[BLOCK_INDEX]
    if block[:4] != b"CS\0\x01":
        raise SystemExit("block 44 does not have the expected CS v1 header")
    declared_body_size = struct.unpack_from("<H", block, 4)[0]
    logical_end = 8 + declared_body_size
    if logical_end > len(block) or any(block[logical_end:]):
        raise SystemExit("block 44 CS length or zero alignment padding is invalid")

    header_size = 8 + (len(container.blocks) + 1) * 4
    block_start_in_sc0 = header_size + sum(
        len(item) for item in container.blocks[:BLOCK_INDEX]
    )
    block_start_bytes = struct.pack("<I", block_start_in_sc0)
    static_hits: list[dict[str, object]] = []
    for path, data in image.iter_components():
        for hit in find_all(data, block_start_bytes):
            static_hits.append({"path": path, "offset": hit})
    for _, path, data in image.iter_files():
        for hit in find_all(data, block_start_bytes):
            static_hits.append({"path": path, "offset": hit})

    runtime: dict[str, object] | None = None
    if args.state:
        wram = extract_wram(unpack_state(args.state))
        prefix = block[:0x2D]
        bases = find_all(wram, prefix)
        runtime = {
            "state": str(args.state),
            "prefix_length": len(prefix),
            "block_base_candidates": [
                f"0x{ARM9_MAIN_RAM + offset:08X}" for offset in bases
            ],
            "pointers": [],
        }
        if len(bases) == 1:
            base = ARM9_MAIN_RAM + bases[0]
            runtime["pointers"] = scan_runtime_pointers(wram, base, base + len(block))

    report = {
        "format": "dk4-sc0-block44-reference-analysis-v1",
        "canonical_rom_sha256": sha256(rom_bytes),
        "source_file_sha256": sha256(sc0),
        "block_sha256": sha256(block),
        "block_index": BLOCK_INDEX,
        "block_start_in_sc0": block_start_in_sc0,
        "block_size": len(block),
        "cs_declared_body_size": declared_body_size,
        "cs_logical_end": logical_end,
        "alignment_padding": len(block) - logical_end,
        "segments": segment_layout(block),
        "static_block_offset_hits": static_hits,
        "runtime": runtime,
        "conclusion": (
            "Analysis only. These observations do not by themselves authorize relocation."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
