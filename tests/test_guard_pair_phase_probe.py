from __future__ import annotations

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from scripts.build_guard_pair_phase_probe import (
    ARM9_LOAD_ADDRESS,
    BLOCK_ADDRESS,
    BLOCK_INDEX,
    FORBIDDEN_END,
    FORBIDDEN_START,
    LOOP_BRANCH_ADDRESS,
    ORIGINAL_BLOCK,
    ORIGINAL_LOOP_BRANCH,
    ORIGINAL_RECORD,
    PHASE_SAFE_RECORD,
    RECORD_INDEX,
    SC0_RECORD_OFFSET,
    SC0_SHA256,
    ZERO_CURSOR_BLOCK,
    ZERO_CURSOR_LOOP_BRANCH,
    apply_arm9,
    apply_sc0,
    sha256,
)


def make_sc0() -> bytes:
    blocks = [b"\0" for _ in range(BLOCK_INDEX + 1)]
    records = [b"" for _ in range(RECORD_INDEX + 1)]
    records[RECORD_INDEX] = ORIGINAL_RECORD
    blocks[BLOCK_INDEX] = b"\0".join(records)
    return IlnkContainer(blocks).to_bytes()


def test_pair_phase_record_is_exact_size_and_changes_only_needed_bytes() -> None:
    assert len(PHASE_SAFE_RECORD) == len(ORIGINAL_RECORD)
    assert b"her. \n Janus" in PHASE_SAFE_RECORD
    assert b"helped repair her." in PHASE_SAFE_RECORD


def test_arm9_patch_is_inline_and_avoids_forbidden_tail() -> None:
    size = LOOP_BRANCH_ADDRESS - ARM9_LOAD_ADDRESS + 4
    arm9 = bytearray(size)
    block_offset = BLOCK_ADDRESS - ARM9_LOAD_ADDRESS
    loop_offset = LOOP_BRANCH_ADDRESS - ARM9_LOAD_ADDRESS
    arm9[block_offset : block_offset + len(ORIGINAL_BLOCK)] = ORIGINAL_BLOCK
    arm9[loop_offset : loop_offset + 4] = ORIGINAL_LOOP_BRANCH
    rebuilt = apply_arm9(bytes(arm9))
    assert rebuilt[block_offset : block_offset + len(ZERO_CURSOR_BLOCK)] == ZERO_CURSOR_BLOCK
    assert rebuilt[loop_offset : loop_offset + 4] == ZERO_CURSOR_LOOP_BRANCH
    for start, length in ((BLOCK_ADDRESS, len(ORIGINAL_BLOCK)), (LOOP_BRANCH_ADDRESS, 4)):
        assert start + length <= FORBIDDEN_START or start >= FORBIDDEN_END


def test_arm9_patch_rejects_wrong_hook_bytes() -> None:
    size = LOOP_BRANCH_ADDRESS - ARM9_LOAD_ADDRESS + 4
    arm9 = bytearray(size)
    with pytest.raises(ValueError, match="LF block mismatch"):
        apply_arm9(bytes(arm9))


def test_sc0_patch_rejects_wrong_component_hash(monkeypatch: pytest.MonkeyPatch) -> None:
    sc0 = make_sc0()
    monkeypatch.setattr("scripts.build_guard_pair_phase_probe.SC0_SHA256", "00" * 32)
    with pytest.raises(ValueError, match="does not match"):
        apply_sc0(sc0)


def test_sc0_patch_changes_only_target_record(monkeypatch: pytest.MonkeyPatch) -> None:
    sc0 = make_sc0()
    monkeypatch.setattr("scripts.build_guard_pair_phase_probe.SC0_SHA256", sha256(sc0))
    monkeypatch.setattr("scripts.build_guard_pair_phase_probe.SC0_RECORD_OFFSET", 0x133)
    rebuilt = apply_sc0(sc0)
    before = IlnkContainer.parse(sc0)
    after = IlnkContainer.parse(rebuilt)
    assert before.blocks[:BLOCK_INDEX] == after.blocks[:BLOCK_INDEX]
    before_records = before.blocks[BLOCK_INDEX].split(b"\0")
    after_records = after.blocks[BLOCK_INDEX].split(b"\0")
    assert after_records[RECORD_INDEX] == PHASE_SAFE_RECORD
    assert [
        index for index, pair in enumerate(zip(before_records, after_records)) if pair[0] != pair[1]
    ] == [RECORD_INDEX]


def test_sc0_patch_rejects_wrong_record_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    sc0 = make_sc0().replace(ORIGINAL_RECORD, b"X" * len(ORIGINAL_RECORD))
    monkeypatch.setattr("scripts.build_guard_pair_phase_probe.SC0_SHA256", sha256(sc0))
    monkeypatch.setattr("scripts.build_guard_pair_phase_probe.SC0_RECORD_OFFSET", 0x133)
    with pytest.raises(ValueError, match="source bytes do not match"):
        apply_sc0(sc0)


def test_expected_safe_sc0_hash_is_locked() -> None:
    assert SC0_SHA256 == "d968fb685460487441fd47b8d86b87f4281c4c0021524201380494e399674a98"
    assert SC0_RECORD_OFFSET == 0x7B4D
