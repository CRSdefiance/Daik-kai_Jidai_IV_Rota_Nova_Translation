from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BATCH = Path("translations/lil_sc2_b22_intro_natural_v2.json")
SOURCE = Path("work/extracted_clean/data/SC2.DK4")


def _changed_segments(before: bytes, after: bytes) -> set[tuple[int, int]]:
    old = IlnkContainer.parse(before)
    new = IlnkContainer.parse(after)
    return {
        (block_index, record_index)
        for block_index, (old_block, new_block) in enumerate(
            zip(old.blocks, new.blocks, strict=True)
        )
        for record_index, (old_record, new_record) in enumerate(
            zip(old_block.split(b"\0"), new_block.split(b"\0"), strict=True)
        )
        if old_record != new_record
    }


def test_complete_lil_intro_is_fixed_size_and_source_locked() -> None:
    source = SOURCE.read_bytes()
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile("lil-story-b22-intro-probe")
    assert len(rows) == 49

    expected = set()
    guards = {record["id"]: record["source_hex_guard"] for record in batch["records"]}
    for row in rows:
        original = bytes.fromhex(str(row["source_hex"]))
        assert original.hex().upper() == guards[row["id"]]
        encoded = encode_fixed_dialogue(original, str(row["english"]), profile)
        assert len(encoded.encoded) == len(original)
        expected.add((22, int(str(row["id"]).rsplit("R", 1)[1])))

    rebuilt = rebuild_mesfile(source, rows)
    assert _changed_segments(source, rebuilt) == expected


def test_complete_lil_intro_maps_all_four_speakers_and_name_macro() -> None:
    profile = get_dialogue_profile("lil-story-b22-intro-probe")
    assert profile.leading_speaker_bytes == {0x02, 0x09, 0x0E, 0x14}
    assert profile.macro_ascii_lengths == {"FI": 3, "FA": 5, "FO": 9}
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    prefixes = {record["english"].split("}", 1)[0] + "}" for record in batch["records"]}
    assert prefixes == {
        "{SPEAKER:02}",
        "{SPEAKER:09}",
        "{SPEAKER:0E}",
        "{SPEAKER:14}",
    }
    assert any("{MACRO:FI}" in record["english"] for record in batch["records"])


def test_complete_lil_intro_profile_is_experimental() -> None:
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    entry = stack["profiles"]["lil-b22-intro-probe"]
    assert entry["status"] == "experimental"
    assert entry["batches"] == [BATCH.as_posix()]
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert batch["research_only"] is True
