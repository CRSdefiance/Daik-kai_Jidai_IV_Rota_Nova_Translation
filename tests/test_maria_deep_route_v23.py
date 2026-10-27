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
BATCH = Path("translations/maria_deep_route_v23.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v23_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 57,
        "translated_records": 57,
        "excluded_records": 0,
        "blocks": {
            "150": 10,
            "152": 8,
            "155": 8,
            "158": 8,
            "197": 14,
            "241": 9,
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


def test_maria_v23_states_and_release_registration() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    for row_id, state in {
        "DK4_MES_B150_R0005": "AE",
        "DK4_MES_B152_R0008": "60",
        "DK4_MES_B152_R0034": "5C",
        "DK4_MES_B155_R0004": "A6",
        "DK4_MES_B158_R0005": "A5",
        "DK4_MES_B197_R0004": "1A",
        "DK4_MES_B197_R0007": "C5",
        "DK4_MES_B241_R0004": "94",
        "DK4_MES_B241_R0008": "44",
        "DK4_MES_B241_R0018": "FE",
    }.items():
        assert by_id[row_id].startswith(f"{{SPEAKER:{state}}}")

    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v23"]["batches"][-1] == BATCH.as_posix()
