from __future__ import annotations

import struct

from scripts.build_register_safe_dialogue_cursor_probe import (
    FLAG_ADDRESS,
    HELPER,
    HELPER_ADDRESS,
    PATCHES,
    SHARED_RENDERER,
    STANDARD_DIALOGUE_CALL,
    WRAPPER,
    WRAPPER_ADDRESS,
    apply_patches,
    arm_bl,
)


def synthetic_rom() -> bytes:
    arm9_offset = 0x200
    arm9_ram = 0x02000000
    arm9_size = max(p.address - arm9_ram + len(p.expected) for p in PATCHES) + 0x20
    rom = bytearray(arm9_offset + arm9_size)
    struct.pack_into("<IIII", rom, 0x20, arm9_offset, arm9_ram, arm9_ram, arm9_size)
    for patch in PATCHES:
        offset = arm9_offset + patch.address - arm9_ram
        rom[offset : offset + len(patch.expected)] = patch.expected
    return bytes(rom)


def test_only_declared_bytes_change() -> None:
    source = synthetic_rom()
    try:
        apply_patches(source, require_source_lock=False)
    except ValueError as error:
        assert "0x021723FC-0x02172463 is live structured ARM9 data" in str(error)
    else:
        raise AssertionError("retired unsafe probe unexpectedly built")


def test_wrapper_preserves_inputs_and_stack_alignment() -> None:
    assert WRAPPER.startswith(bytes.fromhex("1C402DE9"))
    assert bytes.fromhex("1C80BDE8") in WRAPPER
    assert PATCHES[1].expected == arm_bl(STANDARD_DIALOGUE_CALL, SHARED_RENDERER)
    assert PATCHES[1].replacement == arm_bl(STANDARD_DIALOGUE_CALL, WRAPPER_ADDRESS)


def test_helper_preserves_r12_and_retains_original_load() -> None:
    assert HELPER.startswith(bytes.fromhex("00102DE924309AE5"))
    assert bytes.fromhex("0010BDE8") in HELPER
    assert HELPER.endswith(struct.pack("<I", FLAG_ADDRESS))
    assert PATCHES[2].replacement != arm_bl(PATCHES[2].address, HELPER_ADDRESS)


def test_shared_hook_and_return_do_not_write_lr() -> None:
    # The hook must be B, never BL: BL destroys the enclosing renderer's LR.
    hook_word = struct.unpack("<I", PATCHES[2].replacement)[0]
    assert hook_word & 0x0F000000 == 0x0A000000
    # The helper returns with another B to the instruction after the hook.
    return_word = struct.unpack("<I", HELPER[0x38:0x3C])[0]
    assert return_word & 0x0F000000 == 0x0A000000


def test_code_cave_ends_before_existing_data() -> None:
    assert HELPER_ADDRESS + len(HELPER) == 0x02172464


def test_rejects_wrong_source_instruction() -> None:
    source = bytearray(synthetic_rom())
    arm9_offset = struct.unpack_from("<I", source, 0x20)[0]
    offset = arm9_offset + PATCHES[1].address - 0x02000000
    source[offset] ^= 0xFF
    try:
        apply_patches(bytes(source), require_source_lock=False)
    except ValueError as error:
        assert "retired unsafe probe" in str(error)
    else:
        raise AssertionError("unexpected source instruction was accepted")
