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
BATCH = Path("translations/maria_deep_route_v22.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v22_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 90,
        "translated_records": 90,
        "excluded_records": 0,
        "blocks": {
            "151": 13,
            "153": 11,
            "154": 10,
            "157": 9,
            "159": 12,
            "161": 11,
            "164": 13,
            "167": 11,
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
        (
            int(row["id"].split("_B")[1].split("_")[0]),
            int(row["id"].rsplit("R", 1)[1]),
        )
        for row in rows
    }
    assert changed_segments(source, rebuilt) == expected
    old = IlnkContainer.parse(source)
    new = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(new.blocks[block].split(b"\0")[index]) == len(
            old.blocks[block].split(b"\0")[index]
        )


def test_maria_v22_verified_states_and_release_registration() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    for row_id, state in {
        "DK4_MES_B151_R0006": "A6",
        "DK4_MES_B157_R0005": "A5",
        "DK4_MES_B159_R0004": "AE",
        "DK4_MES_B161_R0005": "82",
        "DK4_MES_B161_R0009": "96",
        "DK4_MES_B164_R0052": "56",
        "DK4_MES_B164_R0055": "9A",
        "DK4_MES_B167_R0005": "9C",
        "DK4_MES_B167_R0009": "75",
        "DK4_MES_B167_R0045": "06",
        "DK4_MES_B167_R0055": "FE",
    }.items():
        assert by_id[row_id].startswith(f"{{SPEAKER:{state}}}")

    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    rows = {
        row["id"]: row
        for row in materialize_translation_batch(batch, source)
    }
    # The high first bytes are presentation states only in these correlated
    # blocks. The following byte pairs remain intact Shift-JIS text leads.
    assert bytes.fromhex(rows["DK4_MES_B161_R0005"]["source_hex"])[:3] == bytes.fromhex("829166")
    assert bytes.fromhex(rows["DK4_MES_B164_R0055"]["source_hex"])[:3] == bytes.fromhex("9A82BB")

    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v22"]["batches"][-1] == BATCH.as_posix()
