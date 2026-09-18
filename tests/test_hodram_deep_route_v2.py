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
from scripts.materialize_hodram_deep_route_v2 import BLOCKS, LINES

V1_BATCH = Path("translations/hodram_deep_route_v1.json")
V2_BATCH = Path("translations/hodram_deep_route_v2.json")
STACK = Path("translations/release_stack.json")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_deep_route_v2_inventory_is_complete_and_source_locked() -> None:
    batch = _load(V2_BATCH)
    records = batch["records"]
    assert isinstance(records, list)
    assert len(records) == len(LINES) == 191
    assert {record["id"] for record in records} == set(LINES)
    assert batch["dialogue_profile"] == "hodram-story-live"
    assert set(batch["inventory"]["blocks"]) == {str(block) for block in BLOCKS}


def test_deep_route_v2_encodes_exactly_and_has_no_blocking_layout_issue() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    v1_rows = materialize_translation_batch(_load(V1_BATCH), source)
    v2_rows = materialize_translation_batch(_load(V2_BATCH), source)
    profile = get_dialogue_profile("hodram-story-live")
    for row in v2_rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        assert not [
            issue for issue in audit["issues"] if issue["severity"] == "error"
        ], (row["id"], audit)

    rows = [*v1_rows, *v2_rows]
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (
            int(str(row["id"]).split("_B", 1)[1].split("_", 1)[0]),
            int(str(row["id"]).rsplit("R", 1)[1]),
        )
        for row in rows
    }
    assert len(expected) == 339
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_deep_route_v2_profile_keeps_v1_and_current_polish_layers() -> None:
    profiles = _load(STACK)["profiles"]
    v1 = profiles["hodram-deep-route-v1"]
    v2 = profiles["hodram-deep-route-v2"]
    assert v2["status"] == "experimental"
    assert v2["batches"][:-1] == v1["batches"]
    assert v2["batches"][-1] == V2_BATCH.as_posix()
    profile = get_dialogue_profile("hodram-story-live")
    assert profile.macro_ascii_lengths == {"FI": 6, "FA": 9, "FO": 15}
    assert 0x11 in profile.leading_speaker_bytes
    assert 0x74 in profile.leading_speaker_bytes
    assert profile.guard_linebreaks is True
    assert profile.pair_phase_safe_breaks is True
