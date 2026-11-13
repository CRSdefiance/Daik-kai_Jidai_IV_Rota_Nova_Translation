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
BATCH = Path("translations/maria_deep_route_v43.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v43_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 43,
        "translated_records": 27,
        "excluded_records": 16,
        "blocks": {
            "242": 2, "243": 4, "244": 9, "245": 2, "248": 2, "251": 2,
            "252": 0, "281": 0, "282": 2, "283": 0, "284": 4, "291": 0,
            "292": 0, "293": 0,
        },
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
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert changed_segments(source, rebuilt) == expected
    old, new = IlnkContainer.parse(source), IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(new.blocks[block].split(b"\0")[index]) == len(old.blocks[block].split(b"\0")[index])


def test_maria_v43_macros_states_exclusions_and_release() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record for record in batch["records"]}
    assert by_id["DK4_MES_B244_R0008"]["english"].startswith("{SPEAKER:43}")
    assert by_id["DK4_MES_B243_R0004"]["english"].startswith("{SPEAKER:93}")
    assert by_id["DK4_MES_B282_R0006"]["english"].startswith("{SPEAKER:C9}")
    assert by_id["DK4_MES_B284_R0005"]["english"].startswith("{SPEAKER:CD}")
    assert "{MACRO:FI}" in by_id["DK4_MES_B282_R0006"]["english"]
    assert len(batch["excluded"]) == 16
    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v43"]["batches"][-1] == BATCH.as_posix()
