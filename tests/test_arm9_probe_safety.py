from __future__ import annotations

import struct

from scripts.arm9_probe_safety import (
    PROVEN_NEW_GAME_DATA,
    PROVEN_RAPHAEL_DATA,
    RUNTIME_OWNED_TAIL,
    read_arm9_layout,
    reject_runtime_owned_tail,
    require_exact_bytes,
    runtime_to_file_offset,
)


def synthetic_rom() -> bytes:
    arm9_offset = 0x200
    arm9_ram = 0x02000000
    arm9_size = 0x2000
    rom = bytearray(arm9_offset + arm9_size)
    struct.pack_into("<IIII", rom, 0x20, arm9_offset, arm9_ram + 0x800, arm9_ram, arm9_size)
    rom[arm9_offset + 0x100 : arm9_offset + 0x104] = bytes.fromhex("019089E2")
    return bytes(rom)


def test_runtime_to_file_mapping_uses_nds_header() -> None:
    rom = synthetic_rom()
    layout = read_arm9_layout(rom)
    assert layout.file_offset == 0x200
    assert layout.load_address == 0x02000000
    assert runtime_to_file_offset(rom, 0x02000100, 4) == 0x300
    assert require_exact_bytes(rom, 0x02000100, bytes.fromhex("019089E2")) == 0x300


def test_mapping_rejects_outside_arm9() -> None:
    rom = synthetic_rom()
    for address in (0x01FFFFFF, 0x02001FFF):
        try:
            runtime_to_file_offset(rom, address, 4)
        except ValueError as error:
            assert "outside ARM9" in str(error)
        else:
            raise AssertionError("out-of-range ARM9 address was accepted")


def test_all_proven_live_ranges_are_inside_conservative_block() -> None:
    tail_start, tail_end = RUNTIME_OWNED_TAIL
    for start, end in (PROVEN_RAPHAEL_DATA, PROVEN_NEW_GAME_DATA):
        assert tail_start <= start < end <= tail_end
        try:
            reject_runtime_owned_tail(start, end - start)
        except ValueError as error:
            assert "ROM zero padding is not a cave" in str(error)
        else:
            raise AssertionError("proven live ARM9 data was accepted as a code cave")


def test_overlap_guard_rejects_partial_overlap() -> None:
    start, end = RUNTIME_OWNED_TAIL
    for address, length in ((start - 4, 8), (end - 4, 8)):
        try:
            reject_runtime_owned_tail(address, length)
        except ValueError:
            pass
        else:
            raise AssertionError("partial overlap with runtime-owned tail was accepted")
