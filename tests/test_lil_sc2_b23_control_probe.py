from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BATCH = Path("translations/lil_sc2_b23_control_probe_v1.json")
SOURCE = Path("work/extracted_clean/data/SC2.DK4")


def changed_segments(before: bytes, after: bytes) -> set[tuple[int, int]]:
    old = IlnkContainer.parse(before)
    new = IlnkContainer.parse(after)
    changed = set()
    for block_index, (old_block, new_block) in enumerate(zip(old.blocks, new.blocks, strict=True)):
        for record_index, (old_record, new_record) in enumerate(
            zip(old_block.split(b"\0"), new_block.split(b"\0"), strict=True)
        ):
            if old_record != new_record:
                changed.add((block_index, record_index))
    return changed


def test_lil_b23_profile_maps_the_route_specific_states_and_default_macros():
    profile = get_dialogue_profile("lil-story-b23-probe")
    assert profile.leading_speaker_bytes == {0x02, 0x09, 0x14, 0xFE}
    assert profile.macro_ascii_lengths == {"FI": 3, "FA": 5, "FO": 9}
    assert profile.macro_widths == {"FI": 18, "FA": 30, "FO": 54, "I": 12}


def test_lil_b23_probe_is_fixed_allocation_and_exactly_source_locked():
    source = SOURCE.read_bytes()
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile("lil-story-b23-probe")
    expected = set()
    for row, record in zip(rows, batch["records"], strict=True):
        original = bytes.fromhex(str(row["source_hex"]))
        assert original.hex().upper() == record["source_hex_guard"]
        encoded = encode_fixed_dialogue(original, str(row["english"]), profile)
        assert len(encoded.encoded) == len(original)
        block = int(str(row["id"]).split("_B", 1)[1].split("_R", 1)[0])
        index = int(str(row["id"]).rsplit("R", 1)[1])
        expected.add((block, index))
    rebuilt = rebuild_mesfile(source, rows)
    assert changed_segments(source, rebuilt) == expected


def test_lil_b23_two_unprefixed_records_are_choice_labels_not_dialogue_states():
    segments = IlnkContainer.parse(SOURCE.read_bytes()).blocks[23].split(b"\0")
    assert segments[15] == b"\x21"
    assert segments[17] == b"\x10"
    assert segments[18].decode("cp932") == "それって初耳…"
    assert segments[20].decode("cp932") == "聞かなくたって、分かってる"
    assert segments[23] == b"\x02\x04"
    assert segments[25] == b"\x03\x04"
    assert segments[27] == b"\x01\x34"
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    choices = [record for record in batch["records"] if record["id"].endswith(("R0018", "R0020"))]
    assert len(choices) == 2
    assert all("{SPEAKER:" not in record["english"] for record in choices)


def test_lil_b23_probe_is_experimental_and_profile_scoped():
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    profile = stack["profiles"]["lil-b23-control-probe"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [BATCH.as_posix()]
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert batch["research_only"] is True
