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


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCHES = [Path(f"translations/lil_deep_route_v{i}.json") for i in range(1, 10)]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v9_inventory_layout_and_cumulative_segments() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = []
    for path, count in zip(BATCHES, (61, 70, 53, 84, 125, 56, 110, 85, 84), strict=True):
        batch = _load(path)
        assert len(batch["records"]) == count
        profile = get_dialogue_profile(str(batch["dialogue_profile"]))
        materialized = materialize_translation_batch(batch, source)
        for row in materialized:
            audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
            assert not [issue for issue in audit["issues"] if issue["severity"] == "error"]
        rows.extend(materialized)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 728
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_lil_v9_release_stack_states_and_story_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v9"]["batches"][:-1] == profiles["lil-deep-route-v8"]["batches"]
    assert profiles["lil-deep-route-v9"]["batches"][-1] == BATCHES[-1].as_posix()
    profile = get_dialogue_profile("lil-story-deep-route-live")
    assert {0x06, 0x0B, 0x0D, 0x38, 0x4C} <= profile.leading_speaker_bytes
    v9 = _load(BATCHES[-1])
    assert v9["inventory"]["blocks"] == {"43": 21, "44": 16, "45": 25, "46": 13, "47": 9}
    by_id = {record["id"]: record["english"] for record in v9["records"]}
    assert "raw material" in by_id["DK4_MES_B43_R0006"]
    assert "Mediterranean" in by_id["DK4_MES_B44_R0029"]
    assert "Hayreddin" in by_id["DK4_MES_B45_R0123"]
    assert "Pasha's treasure" in by_id["DK4_MES_B46_R0109"]
    assert "Batavia's tavern" in by_id["DK4_MES_B47_R0035"]
    assert by_id["DK4_MES_B47_R0009"].startswith("{SPEAKER:38}")
    visible = [text.split("}", 1)[1] if text.startswith("{SPEAKER:") else text for text in by_id.values()]
    assert all("I" not in text.replace("{MACRO:FI}", "") for text in visible)
    assert all(
        "F" not in text.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        for text in visible
    )
