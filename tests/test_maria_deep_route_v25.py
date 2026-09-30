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
BATCH = Path("translations/maria_deep_route_v25.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v25_inventory_layout_allocations_and_payloads() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 101,
        "translated_records": 99,
        "excluded_records": 2,
        "blocks": {"176": 21, "177": 20, "178": 17, "184": 12, "185": 13, "186": 16},
        "excluded_blocks": {"178": 1, "186": 1},
    }
    excluded = {
        "DK4_MES_B178_R0006": "414893A8",
        "DK4_MES_B186_R0021": "214896A8",
    }
    assert {row["id"] for row in batch["excluded"]} == set(excluded)

    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
    original = IlnkContainer.parse(source)
    for row_id, source_hex in excluded.items():
        block = int(row_id.split("_B")[1].split("_")[0])
        index = int(row_id.rsplit("R", 1)[1])
        assert original.blocks[block].split(b"\0")[index].hex().upper() == source_hex

    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    rows = materialize_translation_batch(batch, source)
    failures = []
    for row in rows:
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        if errors:
            failures.append((row["id"], errors))
    assert not failures, failures

    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B")[1].split("_")[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert changed_segments(source, rebuilt) == expected
    updated = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(updated.blocks[block].split(b"\0")[index]) == len(original.blocks[block].split(b"\0")[index])
    for row_id, source_hex in excluded.items():
        block = int(row_id.split("_B")[1].split("_")[0])
        index = int(row_id.rsplit("R", 1)[1])
        assert updated.blocks[block].split(b"\0")[index].hex().upper() == source_hex


def test_maria_v25_states_text_leads_and_release_registration() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    for row_id, state in {
        "DK4_MES_B176_R0008": "03",
        "DK4_MES_B176_R0045": "AA",
        "DK4_MES_B177_R0045": "82",
        "DK4_MES_B177_R0059": "FE",
        "DK4_MES_B178_R0008": "0F",
        "DK4_MES_B184_R0004": "07",
        "DK4_MES_B185_R0004": "95",
        "DK4_MES_B186_R0008": "03",
    }.items():
        assert by_id[row_id].startswith(f"{{SPEAKER:{state}}}")

    for row_id in (
        "DK4_MES_B185_R0009",
        "DK4_MES_B185_R0038",
        "DK4_MES_B185_R0040",
        "DK4_MES_B185_R0042",
    ):
        assert not by_id[row_id].startswith("{SPEAKER:")
        assert not by_id[row_id].startswith("{LB}")

    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v25"]["batches"][-1] == BATCH.as_posix()
