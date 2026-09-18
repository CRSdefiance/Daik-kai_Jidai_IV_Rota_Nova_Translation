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
BATCHES = [Path(f"translations/raphael_deep_route_v{i}.json") for i in range(1, 7)]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_raphael_v6_inventory_layout_and_cumulative_segments() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC0.DK4")
    rows = []
    for path, count in zip(BATCHES, (59, 92, 57, 26, 114, 84), strict=True):
        batch = _load(path)
        assert len(batch["records"]) == count
        profile = get_dialogue_profile(str(batch["dialogue_profile"]))
        materialized = materialize_translation_batch(batch, source)
        for row in materialized:
            audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
            errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
            assert not errors, (row["id"], errors)
        rows.extend(materialized)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 432
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_raphael_v6_release_stack_and_rescue_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["raphael-deep-route-v6"]["batches"][:-1] == profiles["raphael-deep-route-v5"]["batches"]
    assert profiles["raphael-deep-route-v6"]["batches"][-1] == BATCHES[-1].as_posix()
    v6 = _load(BATCHES[-1])
    assert v6["inventory"] == {"identified_records": 85, "translated_records": 84, "blocks": {"83": 84}}
    assert set(v6["excluded_records"]) == {"DK4_MES_B83_R0081"}
    by_id = {record["id"]: record["english"] for record in v6["records"]}
    assert "Mivor is coming" in by_id["DK4_MES_B83_R0156"]
    assert "Mivor saved you" in by_id["DK4_MES_B83_R0192"]
    assert "You looked... brave" in by_id["DK4_MES_B83_R0299"]
