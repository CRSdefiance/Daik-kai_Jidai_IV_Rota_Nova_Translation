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
from scripts.materialize_hodram_deep_route_v4a import (
    BLOCKS as BLOCKS_A,
    EXCLUDED as EXCLUDED_A,
    LINES as LINES_A,
)
from scripts.materialize_hodram_deep_route_v4b import (
    BLOCKS as BLOCKS_B,
    EXCLUDED as EXCLUDED_B,
    LINES as LINES_B,
)

BATCHES = [Path(f"translations/hodram_deep_route_v{i}.json") for i in range(1, 4)]
V4_BATCHES = [
    Path("translations/hodram_deep_route_v4a.json"),
    Path("translations/hodram_deep_route_v4b.json"),
]
STACK = Path("translations/release_stack.json")
BASE = Path("out/raphael_natural_v2_accepted_base.nds")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_deep_route_v4_inventory_is_complete_and_source_locked() -> None:
    a, b = (_load(path) for path in V4_BATCHES)
    a_records, b_records = a["records"], b["records"]
    assert isinstance(a_records, list) and isinstance(b_records, list)
    assert len(a_records) == len(LINES_A) == 182
    assert len(b_records) == len(LINES_B) == 131
    assert a["excluded_records"] == EXCLUDED_A
    assert b["excluded_records"] == EXCLUDED_B
    assert set(a["inventory"]["blocks"]) == {str(block) for block in BLOCKS_A}
    assert set(b["inventory"]["blocks"]) == {str(block) for block in BLOCKS_B}


def test_deep_route_v4_encodes_exactly_and_preserves_every_other_record() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    all_batches = [*BATCHES, *V4_BATCHES]
    rows_by_batch = [materialize_translation_batch(_load(path), source) for path in all_batches]
    profile = get_dialogue_profile("hodram-story-live")
    for row in [row for rows in rows_by_batch[-2:] for row in rows]:
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
    assert len(expected) == 802
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_deep_route_v4_profile_keeps_v3_and_both_new_layers() -> None:
    profiles = _load(STACK)["profiles"]
    v3 = profiles["hodram-deep-route-v3"]
    v4 = profiles["hodram-deep-route-v4"]
    assert v4["status"] == "experimental"
    assert v4["batches"][:-2] == v3["batches"]
    assert v4["batches"][-2:] == [path.as_posix() for path in V4_BATCHES]
    profile = get_dialogue_profile("hodram-story-live")
    assert {0x1A, 0x29, 0x4F, 0x52, 0x5F, 0x68, 0x6C, 0x93, 0x9E, 0xA2, 0xA7} <= profile.leading_speaker_bytes
