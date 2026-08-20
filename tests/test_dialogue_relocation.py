from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

import pytest

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.relocation import (
    BlockEntryPointMap,
    DialogueRelocationError,
    InteriorEntryPoint,
    load_relocation_map,
    plan_block_relocation,
    rebuild_mapped_cs_dialogue,
)
from dk4tool.formats.ilnk import IlnkContainer


def test_relocation_refuses_incomplete_reference_map() -> None:
    mapping = BlockEntryPointMap(44, False, ())
    with pytest.raises(DialogueRelocationError, match="references are complete"):
        plan_block_relocation(b"one\0two\0", {0: 8}, mapping)


def test_relocation_moves_declared_record_entry_points() -> None:
    mapping = BlockEntryPointMap(
        44, True, (InteriorEntryPoint("first", 0), InteriorEntryPoint("second", 1))
    )
    plan = plan_block_relocation(b"one\0two\0", {0: 8}, mapping)
    assert plan.old_size == 8
    assert plan.new_size == 13
    assert [(item.name, item.old_offset, item.new_offset) for item in plan.entry_points] == [
        ("first", 0, 0),
        ("second", 4, 9),
    ]


def test_relocation_requires_explicit_remap_inside_resized_record() -> None:
    mapping = BlockEntryPointMap(
        44, True, (InteriorEntryPoint("inside", 0, old_intra_record_offset=2),)
    )
    with pytest.raises(DialogueRelocationError, match="explicit new intra-record"):
        plan_block_relocation(b"one\0", {0: 8}, mapping)

    mapped = BlockEntryPointMap(
        44,
        True,
        (InteriorEntryPoint("inside", 0, 2, new_intra_record_offset=5),),
    )
    plan = plan_block_relocation(b"one\0", {0: 8}, mapped)
    assert plan.entry_points[0].old_offset == 2
    assert plan.entry_points[0].new_offset == 5


def _cs_block(body: bytes) -> bytes:
    logical = bytearray(b"CS\0\x01\0\0\0\0" + body)
    struct.pack_into("<H", logical, 4, len(logical) - 8)
    return bytes(logical) + b"\0" * (-len(logical) % 4)


def _mapped_fixture() -> tuple[bytes, int, dict[str, object]]:
    block = _cs_block(b"\x40\xFF\xFF\0\x05olds\0tail\0")
    logical_end = 8 + struct.unpack_from("<H", block, 4)[0]
    segments = block[:logical_end].split(b"\0")
    segment_index = segments.index(b"\x05olds")
    source = IlnkContainer([block, b"untouched"]).to_bytes()
    mapping: dict[str, object] = {
        "format": "dk4-cs-relocation-map-v1",
        "source_file_sha256": hashlib.sha256(source).hexdigest(),
        "block_index": 0,
        "source_block_sha256": hashlib.sha256(block).hexdigest(),
        "source_cs_body_size": struct.unpack_from("<H", block, 4)[0],
        "movable_segments": [segment_index],
        "required_segments": [segment_index],
        "external_references_complete": True,
        "preserve_record_parity": True,
    }
    return source, segment_index, mapping


def test_load_relocation_map_fails_closed(tmp_path) -> None:
    path = tmp_path / "map.json"
    path.write_text(
        json.dumps(
            {
                "format": "dk4-cs-relocation-map-v1",
                "external_references_complete": False,
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(DialogueRelocationError, match="references are incomplete"):
        load_relocation_map(path)


def test_load_relocation_map_requires_record_parity_guard(tmp_path) -> None:
    path = tmp_path / "map.json"
    path.write_text(
        json.dumps(
            {
                "format": "dk4-cs-relocation-map-v1",
                "external_references_complete": True,
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(DialogueRelocationError, match="parity preservation"):
        load_relocation_map(path)


def test_revoked_real_block44_map_fails_closed() -> None:
    with pytest.raises(DialogueRelocationError, match="references are incomplete"):
        load_relocation_map(Path("translations/sc0_b44_relocation_map.json"))


def test_mapped_cs_relocation_expands_only_authorized_segment() -> None:
    source, segment_index, mapping = _mapped_fixture()
    old_container = IlnkContainer.parse(source)
    row = {
        "id": "proof",
        "pointer_group": f"ILNK:0:{segment_index}",
        "source_hex": b"\x05olds".hex(),
        "english": "{SPEAKER:05}This dialogue is naturally longer!",
    }

    result = rebuild_mapped_cs_dialogue(
        source, [row], get_dialogue_profile("raphael-story-live"), mapping
    )

    rebuilt = IlnkContainer.parse(result.rebuilt_file)
    assert rebuilt.blocks[1] == old_container.blocks[1]
    assert len(result.new_block) > len(result.old_block)
    assert result.changed_segments == (segment_index,)
    assert result.parity_padded_segments == ()
    new_body_size = struct.unpack_from("<H", result.new_block, 4)[0]
    assert 8 + new_body_size <= len(result.new_block)
    assert not any(result.new_block[8 + new_body_size :])


def test_mapped_cs_relocation_rejects_unauthorized_or_missing_segments() -> None:
    source, segment_index, mapping = _mapped_fixture()
    profile = get_dialogue_profile("raphael-story-live")
    missing = dict(mapping)
    missing["required_segments"] = [segment_index, segment_index + 1]
    row = {
        "id": "proof",
        "pointer_group": f"ILNK:0:{segment_index}",
        "source_hex": b"\x05olds".hex(),
        "english": "{SPEAKER:05}Longer dialogue!",
    }
    with pytest.raises(DialogueRelocationError, match="exactly mapped proof segments"):
        rebuild_mapped_cs_dialogue(source, [row], profile, missing)

    unauthorized = dict(row)
    unauthorized["pointer_group"] = f"ILNK:0:{segment_index + 1}"
    with pytest.raises(DialogueRelocationError, match="not authorized"):
        rebuild_mapped_cs_dialogue(source, [unauthorized], profile, mapping)


def test_mapped_cs_relocation_rejects_changed_record_parity() -> None:
    source, segment_index, mapping = _mapped_fixture()
    row = {
        "id": "proof",
        "pointer_group": f"ILNK:0:{segment_index}",
        "source_hex": b"\x05olds".hex(),
        "english": "{SPEAKER:05}X",
    }
    with pytest.raises(DialogueRelocationError, match="changed byte parity"):
        rebuild_mapped_cs_dialogue(
            source,
            [row],
            get_dialogue_profile("raphael-story-live"),
            mapping,
        )


def test_mapped_cs_relocation_can_add_declared_structural_parity_space() -> None:
    source, segment_index, mapping = _mapped_fixture()
    mapping["parity_mismatch_policy"] = "append-single-space"
    row = {
        "id": "proof",
        "pointer_group": f"ILNK:0:{segment_index}",
        "source_hex": b"\x05olds".hex(),
        "english": "{SPEAKER:05}X",
    }
    result = rebuild_mapped_cs_dialogue(
        source,
        [row],
        get_dialogue_profile("raphael-story-live"),
        mapping,
    )
    assert result.parity_padded_segments == (segment_index,)
    logical_end = 8 + struct.unpack_from("<H", result.new_block, 4)[0]
    assert b"\x05X \0" in result.new_block[:logical_end]
