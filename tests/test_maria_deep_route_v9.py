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
BATCH = Path("translations/maria_deep_route_v9.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v9_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 57,
        "translated_records": 57,
        "excluded_records": 0,
        "blocks": {"259": 57},
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
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)

    rebuilt = rebuild_mesfile(source, rows)
    expected = {(259, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_maria_v9_states_and_release_registration() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    assert by_id["DK4_MES_B259_R0016"].startswith("{SPEAKER:D3}")
    assert not by_id["DK4_MES_B259_R0039"].startswith("{SPEAKER:")
    assert by_id["DK4_MES_B259_R0099"].startswith("{SPEAKER:97}")
    assert by_id["DK4_MES_B259_R0112"].startswith("{SPEAKER:D8}")
    assert by_id["DK4_MES_B259_R0197"].startswith("{MACRO:FI}")
    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v9"]["batches"][-1] == BATCH.as_posix()
