from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments


BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCH = Path("translations/maria_deep_route_v46.json")


def _load(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_maria_v46_inventory_and_allocations() -> None:
    batch = _load(BATCH)
    inventory = batch["inventory"]
    assert inventory["identified_records"] == 64
    assert inventory["translated_records"] == 64
    assert inventory["excluded_records"] == 0

    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    rows = materialize_translation_batch(batch, source)
    failures = []
    for row in rows:
        errors = [
            issue
            for issue in audit_fixed_dialogue_record(
                bytes.fromhex(row["source_hex"]), row["english"], profile
            )["issues"]
            if issue["severity"] == "error"
        ]
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


def test_maria_v46_states_macros_and_release_registration() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record for record in batch["records"]}
    assert by_id["DK4_MES_B19_R0005"]["english"].startswith("{SPEAKER:1B}")
    assert by_id["DK4_MES_B19_R0008"]["english"].startswith("{SPEAKER:B7}")
    assert by_id["DK4_MES_B19_R0033"]["english"].startswith("{LB}")
    assert by_id["DK4_MES_B19_R0096"]["english"].startswith("{SPEAKER:0C}")
    assert "{MACRO:FO}" in by_id["DK4_MES_B19_R0059"]["english"]
    assert "{MACRO:FI}" in by_id["DK4_MES_B19_R0130"]["english"]
    assert "{MACRO:FA}" in by_id["DK4_MES_B19_R0130"]["english"]
    release = _load("translations/release_stack.json")
    assert release["profiles"]["maria-deep-route-v46"]["batches"][-1] == BATCH.as_posix()
