from __future__ import annotations

import struct

from scripts.arm9_probe_safety import reject_runtime_owned_tail
from scripts.build_protected_newline_renderer_probe import (
    CODE_CAVE,
    CODE_CAVE_ADDRESS,
    PATCHES,
    apply_patches,
    arm_bl,
)


def synthetic_rom() -> bytes:
    arm9_offset = 0x200
    arm9_ram = 0x02000000
    arm9_size = max(patch.address - arm9_ram + 4 for patch in PATCHES) + 0x20
    rom = bytearray(arm9_offset + arm9_size)
    struct.pack_into("<IIII", rom, 0x20, arm9_offset, arm9_ram, arm9_ram, arm9_size)
    for patch in PATCHES:
        offset = arm9_offset + patch.address - arm9_ram
        rom[offset : offset + len(patch.expected)] = patch.expected
    return bytes(rom)


def test_retired_probe_hard_fails_before_writing() -> None:
    source = synthetic_rom()
    try:
        apply_patches(source, require_source_lock=False)
    except ValueError as error:
        assert "0x02172300 is live structured ARM9 data" in str(error)
    else:
        raise AssertionError("retired unsafe probe unexpectedly built")


def test_probe_rejects_unexpected_instruction_bytes() -> None:
    source = bytearray(synthetic_rom())
    arm9_offset = struct.unpack_from("<I", source, 0x20)[0]
    offset = arm9_offset + PATCHES[0].address - 0x02000000
    source[offset] ^= 0xFF

    try:
        apply_patches(bytes(source), require_source_lock=False)
    except ValueError as error:
        assert "retired unsafe probe" in str(error)
    else:
        raise AssertionError("unexpected instruction bytes were accepted")


def test_arm_branch_encoding_targets_guard_helper() -> None:
    assert arm_bl(0x0207CFC4, CODE_CAVE_ADDRESS) == PATCHES[0].replacement
    assert arm_bl(0x0207D038, CODE_CAVE_ADDRESS, condition=0) == PATCHES[1].replacement
    assert PATCHES[2].replacement == CODE_CAVE


def test_old_code_cave_is_in_runtime_owned_tail() -> None:
    try:
        reject_runtime_owned_tail(CODE_CAVE_ADDRESS, len(CODE_CAVE))
    except ValueError as error:
        assert "runtime-owned ARM9 data" in str(error)
    else:
        raise AssertionError("known live-data range was accepted as a code cave")
