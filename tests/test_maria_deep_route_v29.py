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
BATCH = Path("translations/maria_deep_route_v29.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v29_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 70, "translated_records": 70, "excluded_records": 0,
        "blocks": {
            "118": 1, "165": 8, "190": 4, "216": 4, "217": 3, "218": 4,
            "219": 4, "222": 3, "224": 2, "229": 3, "240": 6, "246": 5,
            "247": 9, "249": 5, "250": 8, "253": 1,
        },
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


def test_maria_v29_states_macros_and_release_registration() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    for row_id, state in {
        "DK4_MES_B118_R0005": "79", "DK4_MES_B165_R0005": "99",
        "DK4_MES_B190_R0004": "03", "DK4_MES_B190_R0007": "5C",
        "DK4_MES_B216_R0005": "BC", "DK4_MES_B217_R0006": "C1",
        "DK4_MES_B218_R0006": "C3", "DK4_MES_B219_R0005": "C4",
        "DK4_MES_B222_R0006": "C8", "DK4_MES_B224_R0005": "BD",
        "DK4_MES_B229_R0005": "93", "DK4_MES_B240_R0004": "94",
        "DK4_MES_B247_R0004": "47", "DK4_MES_B250_R0004": "48",
        "DK4_MES_B250_R0061": "CF", "DK4_MES_B253_R0005": "71",
    }.items():
        assert by_id[row_id].startswith(f"{{SPEAKER:{state}}}")
    assert "{MACRO:FO}" in by_id["DK4_MES_B118_R0005"]
    assert "{MACRO:FI}" in by_id["DK4_MES_B217_R0006"]
    assert "{MACRO:FA}" in by_id["DK4_MES_B240_R0004"]
    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v29"]["batches"][-1] == BATCH.as_posix()
