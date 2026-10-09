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
BATCH = Path("translations/maria_deep_route_v31.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v31_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 38, "translated_records": 38, "excluded_records": 0,
        "blocks": {"286": 8, "287": 11, "288": 4, "289": 7, "290": 8},
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


def test_maria_v31_states_text_leads_macro_and_release() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record for record in batch["records"]}
    for row_id, state in {
        "DK4_MES_B286_R0005": "CC",
        "DK4_MES_B287_R0004": "93",
        "DK4_MES_B287_R0008": "03",
        "DK4_MES_B288_R0006": "93",
        "DK4_MES_B289_R0005": "93",
        "DK4_MES_B290_R0014": "FE",
    }.items():
        assert by_id[row_id]["english"].startswith(f"{{SPEAKER:{state}}}")
    for row_id in ("DK4_MES_B286_R0030", "DK4_MES_B286_R0043"):
        assert not by_id[row_id]["english"].startswith("{SPEAKER:")
    assert "{MACRO:FI}" in by_id["DK4_MES_B286_R0009"]["english"]
    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v31"]["batches"][-1] == BATCH.as_posix()
