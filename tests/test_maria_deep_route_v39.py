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
BATCH = Path("translations/maria_deep_route_v39.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v39_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 32,
        "translated_records": 32,
        "excluded_records": 0,
        "blocks": {"254": 14, "255": 6, "256": 2, "257": 1, "258": 9},
    }
    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    rows = materialize_translation_batch(batch, source)
    failures = []
    for row in rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(row["source_hex"]), row["english"], profile
        )
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, failures

    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (
            int(row["id"].split("_B", 1)[1].split("_", 1)[0]),
            int(row["id"].rsplit("R", 1)[1]),
        )
        for row in rows
    }
    assert changed_segments(source, rebuilt) == expected
    old, new = IlnkContainer.parse(source), IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(new.blocks[block].split(b"\0")[index]) == len(
            old.blocks[block].split(b"\0")[index]
        )


def test_maria_v39_macros_timing_rewards_and_release() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record for record in batch["records"]}
    assert "{MACRO:FA}" in by_id["DK4_MES_B254_R0047"]["english"]
    assert "one month" in by_id["DK4_MES_B254_R0069"]["english"]
    assert by_id["DK4_MES_B254_R0065"]["english"] == "{SPEAKER:FE}Lent the Lime Drops.{PAD}"
    assert by_id["DK4_MES_B258_R0012"]["english"] == "{SPEAKER:FE}Received 20,000 coins.{PAD}"
    assert by_id["DK4_MES_B258_R0037"]["english"] == "{SPEAKER:FE}London share rose slightly!{PAD}"
    assert by_id["DK4_MES_B258_R0061"]["english"].startswith("{LB}")
    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v39"]["batches"][-1] == BATCH.as_posix()
