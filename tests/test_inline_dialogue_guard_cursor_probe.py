from __future__ import annotations

import itertools
import random
import struct

from scripts.build_inline_dialogue_guard_cursor_probe import (
    BLOCK_ADDRESS,
    BLOCK_SIZE,
    BRANCHES,
    BYTE_LOOP,
    CONTINUE_TARGET,
    EXIT_TARGET,
    HELPER_ADDRESS,
    LOOP_BRANCH_ADDRESS,
    ORIGINAL_BLOCK,
    ORIGINAL_LOOP_BRANCH,
    REPLACEMENT_BLOCK,
    REPLACEMENT_LOOP_BRANCH,
    RETIRED_REASON,
    apply_patch,
    decode_arm_branch,
    verify_replacement,
)


def synthetic_rom() -> bytes:
    arm9_offset = 0x200
    arm9_ram = 0x02000000
    arm9_size = LOOP_BRANCH_ADDRESS - arm9_ram + 0x24
    rom = bytearray(arm9_offset + arm9_size)
    struct.pack_into("<IIII", rom, 0x20, arm9_offset, arm9_ram, arm9_ram, arm9_size)
    block_offset = arm9_offset + BLOCK_ADDRESS - arm9_ram
    loop_offset = arm9_offset + LOOP_BRANCH_ADDRESS - arm9_ram
    rom[block_offset : block_offset + BLOCK_SIZE] = ORIGINAL_BLOCK
    rom[loop_offset : loop_offset + 4] = ORIGINAL_LOOP_BRANCH
    return bytes(rom)


def original_continues(fields: tuple[int, int, int, int, int, int]) -> bool:
    lower_x, current_x, upper_x, lower_y, current_y, upper_y = fields
    return lower_x <= current_x < upper_x and lower_y <= current_y < upper_y


def rewritten_continues(fields: tuple[int, int, int, int, int, int]) -> bool:
    lower_x, current_x, upper_x, lower_y, current_y, upper_y = fields
    if lower_x > current_x or current_x >= upper_x:
        return False
    return not (lower_y > current_y or current_y >= upper_y)


def compensate(previous_two: bytes, cursor: int) -> int:
    if previous_two == b"\x0a\x20" and cursor == 6:
        return 1
    return cursor


def test_replacement_size_and_all_branch_targets() -> None:
    verify_replacement()
    assert len(REPLACEMENT_BLOCK) == len(ORIGINAL_BLOCK) == BLOCK_SIZE
    targets = []
    for branch in BRANCHES:
        offset = branch.address - BLOCK_ADDRESS
        decoded = decode_arm_branch(branch.address, REPLACEMENT_BLOCK[offset : offset + 4])
        assert decoded == (branch.condition, branch.target, False)
        targets.append(branch.target)
    assert targets.count(EXIT_TARGET) == 4
    assert CONTINUE_TARGET in targets
    assert BYTE_LOOP in targets
    assert decode_arm_branch(LOOP_BRANCH_ADDRESS, REPLACEMENT_LOOP_BRANCH) == (
        0x1,
        HELPER_ADDRESS,
        False,
    )


def test_bounds_logic_matches_original() -> None:
    values = (-2, -1, 0, 1, 2)
    for fields in itertools.product(values, repeat=6):
        assert rewritten_continues(fields) == original_continues(fields)
    rng = random.Random(0xD5804)
    for _ in range(10_000):
        fields = tuple(rng.randint(-(1 << 31), (1 << 31) - 1) for _ in range(6))
        assert rewritten_continues(fields) == original_continues(fields)


def test_cursor_compensation_is_exact_and_fail_closed() -> None:
    assert compensate(b"\x0a\x20", 6) == 1
    assert compensate(b"\x0a\x20", 0) == 0
    assert compensate(b"\x0a\x20", 12) == 12
    assert compensate(b"A\x20", 6) == 6
    assert compensate(b"\x0aA", 6) == 6
    helper_store = 0x020D555C - BLOCK_ADDRESS
    assert REPLACEMENT_BLOCK[helper_store : helper_store + 4] == bytes.fromhex("24408A05")


def test_retired_probe_hard_fails_before_writing() -> None:
    source = synthetic_rom()
    try:
        apply_patch(source, require_source_lock=False)
    except ValueError as error:
        assert str(error) == RETIRED_REASON
    else:
        raise AssertionError("retired cursor probe unexpectedly built")


def test_patch_rejects_wrong_block_or_loop_instruction() -> None:
    for address in (BLOCK_ADDRESS, LOOP_BRANCH_ADDRESS):
        source = bytearray(synthetic_rom())
        offset = 0x200 + address - 0x02000000
        source[offset] ^= 0xFF
        try:
            apply_patch(bytes(source), require_source_lock=False)
        except ValueError as error:
            assert str(error) == RETIRED_REASON
        else:
            raise AssertionError("unexpected ARM9 bytes were accepted")


def test_patch_rejects_wrong_source_hash() -> None:
    try:
        apply_patch(synthetic_rom())
    except ValueError as error:
        assert str(error) == RETIRED_REASON
    else:
        raise AssertionError("wrong source hash was accepted")
