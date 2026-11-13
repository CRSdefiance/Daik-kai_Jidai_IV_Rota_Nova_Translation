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
BATCH = Path("translations/maria_deep_route_v19.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_maria_v19_inventory_layout_and_allocations() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 20,
        "translated_records": 20,
        "excluded_records": 0,
        "blocks": {"182": 20},
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
    assert not failures, "\n".join(f"{row_id}: {errors}" for row_id, errors in failures)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {(182, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert changed_segments(source, rebuilt) == expected
    old = IlnkContainer.parse(source)
    new = IlnkContainer.parse(rebuilt)
    for block, index in expected:
        assert len(new.blocks[block].split(b"\0")[index]) == len(old.blocks[block].split(b"\0")[index])


def test_maria_v19_states_shift_jis_leads_and_release_registration() -> None:
    batch = _load(BATCH)
    by_id = {record["id"]: record["english"] for record in batch["records"]}
    assert by_id["DK4_MES_B182_R0013"].startswith("{SPEAKER:D0}")
    assert by_id["DK4_MES_B182_R0026"].startswith("{SPEAKER:0C}")
    assert by_id["DK4_MES_B182_R0064"].startswith("{SPEAKER:0B}")
    assert by_id["DK4_MES_B182_R0070"].startswith("{SPEAKER:03}")
    for row_id in (
        "DK4_MES_B182_R0014",
        "DK4_MES_B182_R0019",
        "DK4_MES_B182_R0053",
        "DK4_MES_B182_R0059",
    ):
        assert not by_id[row_id].startswith("{SPEAKER:")
        assert not by_id[row_id].startswith("{LB}")
    release = _load(Path("translations/release_stack.json"))
    assert release["profiles"]["maria-deep-route-v19"]["batches"][-1] == BATCH.as_posix()
