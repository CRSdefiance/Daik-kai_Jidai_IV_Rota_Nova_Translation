from __future__ import annotations

from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import TABLE_OFFSET, common_message_entries
from scripts.inventory_common_native_messages import inventory


@pytest.fixture
def clean_sources() -> tuple[bytes, bytes]:
    path = Path("work/clean.nds")
    if not path.exists():
        pytest.skip("Local clean ROM required for native loader evidence")
    image = NdsImage.open(path)
    return image.read_file("/COMMON/MESFILE.DK4"), image.read_file("/__arm9__.bin")


def test_complete_native_table_maps_41_blocks_and_3668_entries(clean_sources):
    common, arm9 = clean_sources
    entries = common_message_entries(common, arm9)
    assert [entry.message_id for entry in entries] == list(range(3668))
    assert {entry.block for entry in entries} == set(range(41))
    assert entries[2922].text.decode("cp932").startswith("聖書の難解な部分に")
    assert entries[2922].start == 89
    assert entries[-1].block == 40


@pytest.mark.parametrize("offset", [0x534F4, 0x53628, 0x14186C, TABLE_OFFSET])
def test_clean_mapper_rejects_corrupted_evidence(clean_sources, offset):
    common, arm9 = clean_sources
    damaged = bytearray(arm9)
    damaged[offset] ^= 1
    with pytest.raises(ValueError):
        common_message_entries(common, damaged)


def test_current_mapper_rejects_pointer_into_nul(clean_sources):
    common, arm9 = clean_sources
    damaged = bytearray(arm9)
    # Entry zero ends at byte 35, its first NUL. A native pointer there is invalid.
    damaged[TABLE_OFFSET:TABLE_OFFSET + 2] = (35).to_bytes(2, "little")
    with pytest.raises(ValueError, match="invalid native copy span"):
        common_message_entries(common, damaged, clean=False)


def test_current_mapper_uses_repacked_bgm_offsets():
    path = Path("out/all_routes_combined_v99_candidate.nds")
    if not path.exists():
        pytest.skip("V99 candidate required for accepted BGM pointer evidence")
    image = NdsImage.open(path)
    entries = common_message_entries(image.read_file("/COMMON/MESFILE.DK4"),
                                     image.read_file("/__arm9__.bin"), clean=False)
    assert entries[3264].block_offset == 3281
    assert entries[3264].text.rstrip(b" ") == b"India Town"


def test_native_inventory_finds_blank_messages_hidden_by_record_translation():
    path = Path("out/all_routes_combined_v101_candidate.nds")
    clean = Path("work/clean.nds")
    if not path.exists() or not clean.exists():
        pytest.skip("V101 and clean ROM required for hidden packed message evidence")
    report = inventory(path, clean)
    missing = {entry["message_id"] for entry in report["blank_native_messages"]}
    assert {907, 908} <= missing
    assert report["blank_native_message_count"] == len(missing)
