from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BATCH = Path("translations/lil_sc2_b22_first_screen_probe_v1.json")
SOURCE = Path("work/extracted_clean/data/SC2.DK4")
ROW_ID = "DK4_MES_B22_R0019"


def test_first_screen_probe_is_one_fixed_source_locked_record() -> None:
    source = SOURCE.read_bytes()
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    rows = materialize_translation_batch(batch, source)
    assert [row["id"] for row in rows] == [ROW_ID]
    row = rows[0]
    original = bytes.fromhex(str(row["source_hex"]))
    assert len(original) == 85
    assert original.hex().upper() == batch["records"][0]["source_hex_guard"]

    profile = get_dialogue_profile("lil-story-b22-first-screen-probe")
    encoded = encode_fixed_dialogue(original, str(row["english"]), profile)
    assert len(encoded.encoded) == 85
    assert encoded.encoded.startswith(b"\x02Hee hee!")
    assert encoded.padding_bytes == 8

    before = IlnkContainer.parse(source)
    after = IlnkContainer.parse(rebuild_mesfile(source, rows))
    changed = {
        (block_index, record_index)
        for block_index, (old_block, new_block) in enumerate(
            zip(before.blocks, after.blocks, strict=True)
        )
        for record_index, (old_record, new_record) in enumerate(
            zip(old_block.split(b"\0"), new_block.split(b"\0"), strict=True)
        )
        if old_record != new_record
    }
    assert changed == {(22, 19)}


def test_first_screen_probe_is_explicitly_experimental() -> None:
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    entry = stack["profiles"]["lil-b22-first-screen-probe"]
    assert entry["status"] == "experimental"
    assert entry["batches"] == [BATCH.as_posix()]
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert batch["research_only"] is True
