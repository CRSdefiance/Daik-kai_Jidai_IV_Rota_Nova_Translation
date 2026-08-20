from __future__ import annotations

import itertools
import random
import struct

from scripts.build_inline_dialogue_guard_skip_probe import (
    BLOCK_ADDRESS,
    BLOCK_SIZE,
    BRANCHES,
    CONTINUE_TARGET,
    EXIT_TARGET,
    ORIGINAL_ADVANCE,
    ORIGINAL_ADVANCE_ADDRESS,
    ORIGINAL_BLOCK,
    REPLACEMENT_BLOCK,
    RETIRED_REASON,
    apply_patch,
    decode_arm_branch,
    verify_replacement,
)


def synthetic_rom() -> bytes:
    arm9_offset = 0x200
    arm9_ram = 0x02000000
    arm9_size = BLOCK_ADDRESS - arm9_ram + BLOCK_SIZE + 0x20
    rom = bytearray(arm9_offset + arm9_size)
    struct.pack_into("<IIII", rom, 0x20, arm9_offset, arm9_ram, arm9_ram, arm9_size)
    offset = arm9_offset + BLOCK_ADDRESS - arm9_ram
    rom[offset : offset + BLOCK_SIZE] = ORIGINAL_BLOCK
    return bytes(rom)


def original_continues(
    lower_x: int, current_x: int, upper_x: int, lower_y: int, current_y: int, upper_y: int
) -> bool:
    r8 = lower_x <= current_x < upper_x
    r0 = r8 and lower_y <= current_y
    r1 = r0 and current_y < upper_y
    return r1


def rewritten_continues(
    lower_x: int, current_x: int, upper_x: int, lower_y: int, current_y: int, upper_y: int
) -> bool:
    if lower_x > current_x:
        return False
    if current_x >= upper_x:
        return False
    if lower_y > current_y:
        return False
    return current_y < upper_y


def test_inline_rewrite_has_exact_size_and_branch_targets() -> None:
    verify_replacement()
    assert len(ORIGINAL_BLOCK) == len(REPLACEMENT_BLOCK) == BLOCK_SIZE
    targets = []
    for branch in BRANCHES:
        offset = branch.address - BLOCK_ADDRESS
        condition, target, link = decode_arm_branch(
            branch.address, REPLACEMENT_BLOCK[offset : offset + 4]
        )
        assert (condition, target, link) == (branch.condition, branch.target, False)
        targets.append(target)
    assert targets.count(EXIT_TARGET) == 4
    assert targets.count(CONTINUE_TARGET) == 1


def test_original_advance_is_source_locked_and_replaced_inline() -> None:
    offset = ORIGINAL_ADVANCE_ADDRESS - BLOCK_ADDRESS
    assert ORIGINAL_BLOCK[offset : offset + 4] == ORIGINAL_ADVANCE
    assert REPLACEMENT_BLOCK[offset : offset + 4] == bytes.fromhex("02908902")
    assert REPLACEMENT_BLOCK[offset + 4 : offset + 8] == bytes.fromhex("01908912")


def test_guard_advance_semantics() -> None:
    def advance(next_byte: int) -> int:
        return 2 if next_byte == 0x20 else 1

    assert advance(0x20) == 2
    assert advance(ord("A")) == 1
    assert advance(ord("R")) == 1
    assert advance(0) == 1


def test_bounds_logic_matches_original_at_boundaries() -> None:
    values = (-2, -1, 0, 1, 2)
    for fields in itertools.product(values, repeat=6):
        assert rewritten_continues(*fields) == original_continues(*fields)


def test_bounds_logic_matches_original_for_random_signed_values() -> None:
    rng = random.Random(0xD54F0)
    for _ in range(10_000):
        fields = tuple(rng.randint(-(1 << 31), (1 << 31) - 1) for _ in range(6))
        assert rewritten_continues(*fields) == original_continues(*fields)


def test_retired_probe_hard_fails_before_writing() -> None:
    source = synthetic_rom()
    try:
        apply_patch(source, require_source_lock=False)
    except ValueError as error:
        assert str(error) == RETIRED_REASON
    else:
        raise AssertionError("retired failed probe unexpectedly built")


def test_patch_rejects_wrong_original_block() -> None:
    source = bytearray(synthetic_rom())
    block_offset = 0x200 + BLOCK_ADDRESS - 0x02000000
    source[block_offset] ^= 0xFF
    try:
        apply_patch(bytes(source), require_source_lock=False)
    except ValueError as error:
        assert str(error) == RETIRED_REASON
    else:
        raise AssertionError("unexpected original block was accepted")


def test_patch_rejects_wrong_source_hash() -> None:
    try:
        apply_patch(synthetic_rom())
    except ValueError as error:
        assert str(error) == RETIRED_REASON
    else:
        raise AssertionError("wrong source hash was accepted")
