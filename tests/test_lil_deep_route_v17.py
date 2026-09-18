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
BATCHES = [Path(f"translations/lil_deep_route_v{i}.json") for i in range(1, 18)]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v17_inventory_layout_and_cumulative_segments() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = []
    counts = (61, 70, 53, 84, 125, 56, 110, 85, 84, 94, 87, 75, 74, 83, 162, 94, 86)
    for path, count in zip(BATCHES, counts, strict=True):
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
    assert len(expected) == 1483
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_lil_v17_release_stack_exclusion_and_rescue_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v17"]["batches"][:-1] == profiles["lil-deep-route-v16"]["batches"]
    assert profiles["lil-deep-route-v17"]["batches"][-1] == BATCHES[-1].as_posix()
    v17 = _load(BATCHES[-1])
    assert v17["inventory"] == {
        "identified_records": 87,
        "translated_records": 86,
        "blocks": {"73": 86},
    }
    assert set(v17["excluded_records"]) == {"DK4_MES_B73_R0080"}
    by_id = {record["id"]: record["english"] for record in v17["records"]}
    assert "fell into the sea" in by_id["DK4_MES_B73_R0083"]
    assert "Mivor is coming" in by_id["DK4_MES_B73_R0155"]
    assert "Mivor saved you" in by_id["DK4_MES_B73_R0191"]
    assert "He must love you" in by_id["DK4_MES_B73_R0247"]
    assert "You looked... brave" in by_id["DK4_MES_B73_R0296"]
    assert "good pair" in by_id["DK4_MES_B73_R0323"]
    visible = [text.split("}", 1)[1] if text.startswith("{SPEAKER:") else text for text in by_id.values()]
    assert all("I" not in text.replace("{MACRO:FI}", "") for text in visible)
    assert all(
        "F" not in text.replace("{MACRO:FI}", "").replace("{MACRO:FA}", "").replace("{MACRO:FO}", "")
        for text in visible
    )
