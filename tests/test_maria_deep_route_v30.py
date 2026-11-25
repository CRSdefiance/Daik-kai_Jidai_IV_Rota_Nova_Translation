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
BATCH = Path("translations/maria_deep_route_v30.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v30_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 87, "translated_records": 87, "excluded_records": 0,
        "blocks": {"294": 7, "295": 17, "296": 24, "297": 6, "298": 24, "299": 9},
    }
    source = NdsImage.open(BASE).read_file("/data/SC3.DK4")
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
    old = IlnkContainer.parse(source)
    new = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(new.blocks[block].split(b"\0")[index]) == len(old.blocks[block].split(b"\0")[index])


def test_maria_v30_states_leading_breaks_macros_and_release() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record for record in batch["records"]}
    for row_id, state in {
        "DK4_MES_B294_R0004": "CE", "DK4_MES_B295_R0004": "93",
        "DK4_MES_B296_R0051": "B3", "DK4_MES_B297_R0007": "87",
        "DK4_MES_B298_R0004": "B3", "DK4_MES_B299_R0004": "A1",
    }.items():
        assert by_id[row_id]["english"].startswith(f"{{SPEAKER:{state}}}")
    for row_id in (
        "DK4_MES_B298_R0041", "DK4_MES_B298_R0049", "DK4_MES_B298_R0056",
        "DK4_MES_B298_R0065", "DK4_MES_B298_R0094",
    ):
        assert by_id[row_id]["english"].startswith("{LB}")
        assert "source-leading-linebreak" in by_id[row_id]["qa_waivers"]
    assert "{MACRO:FA}" in by_id["DK4_MES_B295_R0004"]["english"]
    assert "{MACRO:FI}" in by_id["DK4_MES_B298_R0041"]["english"]
    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v30"]["batches"][-1] == BATCH.as_posix()
