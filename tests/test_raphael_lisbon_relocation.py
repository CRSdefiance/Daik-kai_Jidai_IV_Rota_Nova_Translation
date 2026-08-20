from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import (
    audit_fixed_dialogue_record,
    audit_relocatable_dialogue_record,
)
from dk4tool.dialogue.relocation import load_relocation_map, rebuild_mapped_cs_dialogue
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments

BASE_ROM = Path("out/raphael_natural_v2_pre_lisbon_accepted_rollback.nds")
MANUSCRIPT = Path("translations/drafts/raphael_intro_lisbon_sol_v1.json")
BATCH = Path("translations/raphael_intro_lisbon_natural_relocatable_v1.json")
CHOICE_BATCH = Path("translations/raphael_intro_lisbon_choice_fixed_v1.json")
CREW_BATCH = Path("translations/common_crew_join_pair_phase_repair.json")
MAP = Path("translations/sc0_b44_lisbon_parity_relocation_map.json")
STACK = Path("translations/release_stack.json")
BASE_SHA256 = "fe7cdcaf7cfa24f18c1c48608ddddf58dc9a7555cb93c8131163037e814c8586"
SC0_SHA256 = "8568db05c98a4ac10e8b1846a9d35838b8a1a6d7be223c4a92dfc2af755c26e2"
BLOCK44_SHA256 = "9b5ee50c4ebb6c49b1540e6cc0b5e76dc53d38785b2444e3d04aa414043eb00f"
EXCLUDED_IDS = {
    "DK4_MES_B44_R0013",
    "DK4_MES_B44_R0017",
    "DK4_MES_B44_R0021",
    "DK4_MES_B44_R0025",
    "DK4_MES_B44_R0029",
    "DK4_MES_B44_R0092",
    "DK4_MES_B44_R0264",
    "DK4_MES_B44_R0454",
    "DK4_MES_B44_R0456",
}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_lisbon_batch_is_exact_post_opening_inventory() -> None:
    manuscript = _load(MANUSCRIPT)
    batch = _load(BATCH)
    manuscript_ids = {str(record["id"]) for record in manuscript["records"]}
    batch_ids = {str(record["id"]) for record in batch["records"]}

    assert len(manuscript_ids) == 115
    choice = _load(CHOICE_BATCH)
    choice_ids = {str(record["id"]) for record in choice["records"]}

    assert len(batch_ids) == 106
    assert manuscript_ids - batch_ids == EXCLUDED_IDS
    assert not (batch_ids & EXCLUDED_IDS)
    assert choice_ids == {
        "DK4_MES_B44_R0454",
        "DK4_MES_B44_R0456",
    }


def test_lisbon_batch_is_locked_to_the_accepted_base() -> None:
    rom_data = BASE_ROM.read_bytes()
    assert _sha256(rom_data) == BASE_SHA256

    image = NdsImage.open(BASE_ROM)
    sc0 = image.read_file("/data/SC0.DK4")
    block44 = IlnkContainer.parse(sc0).blocks[44]
    batch = _load(BATCH)
    relocation_map = _load(MAP)

    assert _sha256(sc0) == SC0_SHA256
    assert _sha256(block44) == BLOCK44_SHA256
    assert batch["source_file_sha256"] == SC0_SHA256
    assert _load(CHOICE_BATCH)["source_file_sha256"] == SC0_SHA256
    assert relocation_map["source_file_sha256"] == SC0_SHA256
    assert relocation_map["source_block_sha256"] == BLOCK44_SHA256


def test_lisbon_records_are_macro_safe_and_qa_clean() -> None:
    image = NdsImage.open(BASE_ROM)
    sc0 = image.read_file("/data/SC0.DK4")
    batch = _load(BATCH)
    profile = get_dialogue_profile("raphael-story-live")
    materialized = materialize_translation_batch(batch, sc0)

    assert len(materialized) == 106
    for row in materialized:
        english = str(row["english"])
        visible = re.sub(r"\{[^}]+\}", "", english)
        assert "{PAD}" not in english
        assert "{LB" not in english
        assert "{ALIGN" not in english
        assert "F" not in visible
        assert "I" not in visible
        audit = audit_relocatable_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), english, profile
        )
        blockers = [
            issue
            for issue in audit["issues"]
            if issue["severity"] in {"warning", "error"}
        ]
        assert blockers == [], row["id"]


def test_lisbon_relocation_map_covers_exact_batch_segments() -> None:
    image = NdsImage.open(BASE_ROM)
    sc0 = image.read_file("/data/SC0.DK4")
    batch = _load(BATCH)
    rows = materialize_translation_batch(batch, sc0)
    expected_segments = {
        int(str(row["pointer_group"]).rsplit(":", 1)[1]) for row in rows
    }
    relocation_map = _load(MAP)

    assert relocation_map["block_index"] == 44
    assert relocation_map["external_references_complete"] is True
    assert relocation_map["preserve_record_parity"] is True
    assert relocation_map["parity_mismatch_policy"] == "append-single-space"
    assert set(relocation_map["movable_segments"]) == expected_segments
    assert set(relocation_map["required_segments"]) == expected_segments
    assert len(expected_segments) == 106
    assert not ({454, 456} & expected_segments)


def test_lisbon_choice_slots_keep_their_proven_fixed_lengths() -> None:
    image = NdsImage.open(BASE_ROM)
    sc0 = image.read_file("/data/SC0.DK4")
    batch = _load(CHOICE_BATCH)
    rows = materialize_translation_batch(batch, sc0)
    profile = get_dialogue_profile("raphael-story-live")

    assert len(rows) == 2
    for row in rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        blockers = [
            issue
            for issue in audit["issues"]
            if issue["severity"] in {"warning", "error"}
        ]
        assert blockers == [], row["id"]

    rebuilt = rebuild_mesfile(sc0, rows)
    segments = IlnkContainer.parse(rebuilt).blocks[44].split(b"\0")
    assert segments[454] == b"Ask him."
    assert segments[456] == b"Prepare alone."
    assert len(segments[454]) == 8
    assert len(segments[456]) == 14


def test_lisbon_hybrid_relocation_and_fixed_choices_keep_segment_contract() -> None:
    image = NdsImage.open(BASE_ROM)
    sc0 = image.read_file("/data/SC0.DK4")
    relocation_batch = _load(BATCH)
    relocation_rows = materialize_translation_batch(relocation_batch, sc0)
    result = rebuild_mapped_cs_dialogue(
        sc0,
        relocation_rows,
        get_dialogue_profile("raphael-story-live"),
        load_relocation_map(MAP),
    )
    fixed_rows = materialize_translation_batch(_load(CHOICE_BATCH), sc0)
    rebuilt = rebuild_mesfile(result.rebuilt_file, fixed_rows)
    changed = changed_segments(sc0, rebuilt)
    block = IlnkContainer.parse(rebuilt).blocks[44]
    logical_end = 8 + int.from_bytes(block[4:6], "little")
    segments = block[:logical_end].split(b"\0")
    offsets: list[int] = []
    cursor = 0
    for segment in segments:
        offsets.append(cursor)
        cursor += len(segment) + 1

    assert (44, 454) in changed
    assert (44, 456) in changed
    assert not ({(44, 92), (44, 264)} & changed)
    assert offsets[454] - offsets[451] == 5
    assert offsets[456] - offsets[451] == 15
    assert offsets[464] - offsets[451] == 44


def test_shared_crew_join_repair_removes_break_without_moving_placeholders() -> None:
    image = NdsImage.open(BASE_ROM)
    common = image.read_file("/COMMON/MESFILE.DK4")
    batch = _load(CREW_BATCH)
    rows = materialize_translation_batch(batch, common)
    rebuilt = rebuild_mesfile(common, rows)
    source_record = IlnkContainer.parse(common).blocks[4].split(b"\0")[59]
    record = IlnkContainer.parse(rebuilt).blocks[4].split(b"\0")[59]
    assert len(record) == len(source_record) == 43
    assert record[:22] == source_record[:22]
    assert record.find(b"%s", 1) == 20
    assert b"\n" not in record
    assert record == b"%s acquired!        %s joined your crew!   "


def test_lisbon_choicefix_profile_is_accepted_and_baked() -> None:
    stack = _load(STACK)
    revoked = stack["profiles"]["raphael-intro-lisbon-natural-relocation"]
    profile = stack["profiles"]["raphael-intro-lisbon-choicefix"]
    assert revoked["status"] == "revoked"
    assert profile["status"] == "accepted-baked"
    assert profile["batches"] == [
        BATCH.as_posix(),
        CHOICE_BATCH.as_posix(),
        CREW_BATCH.as_posix(),
    ]
