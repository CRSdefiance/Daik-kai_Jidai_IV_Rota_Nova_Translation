from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.mesfile import iter_mesfile_records, rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import apply_arm9_fixed_batch


BASE = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
ARM9_BATCH = Path("translations/deck_view_arm9_v2.json")
DIALOGUE_BATCH = Path("translations/deck_view_dialogue_v2.json")


def test_deck_view_fixed_text_is_source_locked_and_complete() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/__arm9__.bin")
    batch = json.loads(ARM9_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(ids) == 42
    expected = {
        0x11B5A4: "Crew",
        0x12FF58: "Helm",
        0x12FF68: "Survey",
        0x12FFA8: "Mast",
        0x131E74: "Confirm crew assignment?",
        0x131E98: "No unassigned crew.",
        0x131EB4: "Command",
        0x131EBC: "Only %s can be Captain.",
        0x132058: "Skill: %s",
        0x132068: "Need: --",
        0x132078: "Anyone may serve.",
        0x13208C: "Cannot assign here.",
        0x1320A8: "Need: %4d",
        0x1320B8: "No eligible crew.",
        0x14831C: "Observe",
        0x148344: "Sailing",
        0x14834C: "Survey",
    }
    for offset, text in expected.items():
        assert rebuilt[offset : offset + len(text) + 1] == text.encode("ascii") + b"\0"


def test_all_deck_activity_responses_fit_the_runtime_window() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/COMMON/MESFILE.DK4")
    batch = json.loads(DIALOGUE_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]
    assert len(batch["records"]) == 72
    assert all(len(row["english"].removesuffix("{PAD}").encode("ascii")) <= 24 for row in batch["records"])

    rows = materialize_translation_batch(batch, source)
    rebuilt = rebuild_mesfile(source, rows)
    b17 = [record for record in iter_mesfile_records(rebuilt, include_non_japanese=True) if record.block_index == 17]
    visible_ascii = [record.text.rstrip() for record in b17 if all(byte in b"\t\n\r" or 0x20 <= byte < 0x7F for byte in record.raw_bytes)]
    assert visible_ascii
    assert max(map(len, visible_ascii)) <= 24
    assert "This fleet is mine." in visible_ascii
    assert "Leave the wheel to me." in visible_ascii
    assert "Test-firing now." in visible_ascii
    assert "Leave diplomacy to me." in visible_ascii
    assert "see below" not in visible_ascii
    japanese = [record.row_id for record in b17 if contains_japanese(record.text)]
    assert japanese == []


def test_deck_view_v2_is_in_the_current_review_profile() -> None:
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    batches = stack["profiles"]["raphael-story-push-v1"]["batches"]
    assert ARM9_BATCH.as_posix() in batches
    assert DIALOGUE_BATCH.as_posix() in batches
