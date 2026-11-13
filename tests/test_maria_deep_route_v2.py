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
BATCH = Path("translations/maria_deep_route_v2.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v2_inventory_and_layout() -> None:
    batch = _load(BATCH)
    assert batch["file_path"] == "/data/SC3.DK4"
    assert batch["translation_policy"] == "natural-dialogue-v2"
    assert batch["inventory"] == {
        "identified_records": 42,
        "translated_records": 41,
        "excluded_records": 1,
        "blocks": {"170": 24, "193": 17},
    }
    assert batch["excluded_records"] == {
        "DK4_MES_B170_R0021": "Event-control payload !H plus a binary argument; not dialogue."
    }
    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    failures = []
    for row in materialize_translation_batch(batch, source):
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(row["source_hex"]), row["english"], profile
        )
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)


def test_maria_v2_preserves_states_and_exact_allocations() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    assert by_id["DK4_MES_B170_R0004"].startswith("{SPEAKER:A9}")
    assert by_id["DK4_MES_B170_R0008"].startswith("{SPEAKER:15}")
    assert by_id["DK4_MES_B170_R0108"].startswith("{SPEAKER:FE}")
    assert by_id["DK4_MES_B193_R0004"].startswith("{SPEAKER:1A}")
    assert by_id["DK4_MES_B193_R0007"].startswith("{SPEAKER:C7}")

    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    rows = materialize_translation_batch(batch, source)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 41
    assert changed_segments(source, rebuilt) == expected
    parsed_source = IlnkContainer.parse(source)
    parsed_rebuilt = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(parsed_rebuilt.blocks[block].split(b"\0")[index]) == len(
            parsed_source.blocks[block].split(b"\0")[index]
        )


def test_maria_v2_release_registration() -> None:
    release = _load(Path("translations/release_stack.json"))
    registered = release["profiles"]["maria-deep-route-v2"]
    assert registered["status"] == "experimental"
    assert registered["batches"][-2:] == [
        "translations/maria_deep_route_v1.json",
        BATCH.as_posix(),
    ]
