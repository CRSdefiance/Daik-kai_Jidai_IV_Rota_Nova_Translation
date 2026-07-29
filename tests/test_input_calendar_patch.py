import struct

import pytest

from dk4tool.patch.input_calendar import (
    ARM9_LOAD_ADDRESS,
    PATCHES,
    InputCalendarPatchError,
    patch_nds_bytes,
)


def _synthetic_rom() -> bytes:
    arm9_offset = 0x200
    arm9_size = max(patch.offset + len(patch.replacement) for patch in PATCHES) + 0x20
    rom = bytearray(arm9_offset + arm9_size)
    struct.pack_into("<IIII", rom, 0x20, arm9_offset, ARM9_LOAD_ADDRESS, 0, arm9_size)
    for patch in PATCHES:
        start = arm9_offset + patch.offset
        rom[start : start + len(patch.replacement)] = patch.accepted[0]
    return bytes(rom)


def test_input_calendar_patch_applies_and_is_idempotent():
    patched, changes = patch_nds_bytes(_synthetic_rom())
    assert len(changes) == len(PATCHES)
    patched_again, repeated_changes = patch_nds_bytes(patched)
    assert patched_again == patched
    assert repeated_changes == changes


def test_input_calendar_patch_rejects_an_unknown_binary():
    rom = bytearray(_synthetic_rom())
    arm9_offset = struct.unpack_from("<I", rom, 0x20)[0]
    rom[arm9_offset + PATCHES[0].offset] ^= 0xFF
    with pytest.raises(InputCalendarPatchError, match="unexpected bytes"):
        patch_nds_bytes(bytes(rom))
