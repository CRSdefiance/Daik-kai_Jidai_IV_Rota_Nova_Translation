from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments
from scripts.materialize_hodram_deep_route_v3 import BLOCKS, LINES

V1_BATCH = Path("translations/hodram_deep_route_v1.json")
V2_BATCH = Path("translations/hodram_deep_route_v2.json")
V3_BATCH = Path("translations/hodram_deep_route_v3.json")
STACK = Path("translations/release_stack.json")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_deep_route_v3_inventory_is_complete_and_source_locked() -> None:
    batch = _load(V3_BATCH)
    records = batch["records"]
    assert isinstance(records, list)
    assert len(records) == len(LINES) == 150
    assert {record["id"] for record in records} == set(LINES)
    assert batch["dialogue_profile"] == "hodram-story-live"
    assert set(batch["inventory"]["blocks"]) == {str(block) for block in BLOCKS}


def test_deep_route_v3_encodes_exactly_and_has_no_blocking_layout_issue() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    batches = [_load(V1_BATCH), _load(V2_BATCH), _load(V3_BATCH)]
    rows_by_batch = [materialize_translation_batch(batch, source) for batch in batches]
    profile = get_dialogue_profile("hodram-story-live")
    for row in rows_by_batch[-1]:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        assert not [
            issue for issue in audit["issues"] if issue["severity"] == "error"
        ], (row["id"], audit)

    rows = [row for batch_rows in rows_by_batch for row in batch_rows]
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (
            int(str(row["id"]).split("_B", 1)[1].split("_", 1)[0]),
            int(str(row["id"]).rsplit("R", 1)[1]),
        )
        for row in rows
    }
    assert len(expected) == 489
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_deep_route_v3_profile_keeps_v2_and_current_polish_layers() -> None:
    profiles = _load(STACK)["profiles"]
    v2 = profiles["hodram-deep-route-v2"]
    v3 = profiles["hodram-deep-route-v3"]
    assert v3["status"] == "experimental"
    assert v3["batches"][:-1] == v2["batches"]
    assert v3["batches"][-1] == V3_BATCH.as_posix()
    profile = get_dialogue_profile("hodram-story-live")
    assert profile.macro_ascii_lengths == {"FI": 6, "FA": 9, "FO": 15}
    assert {0x22, 0x73, 0x9C} <= profile.leading_speaker_bytes
    assert profile.guard_linebreaks is True
    assert profile.pair_phase_safe_breaks is True
