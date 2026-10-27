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
BATCH = Path("translations/lil_deep_route_v22.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v22_inventory_layout_and_segments() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 144,
        "translated_records": 144,
        "blocks": {"81": 7, "82": 16, "83": 15, "84": 19, "86": 10, "88": 28, "164": 49},
    }
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    for row in rows:
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        errors = [issue for issue in audit["issues"] if issue["severity"] == "error"]
        assert not errors, (row["id"], errors)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 144
    assert changed_segments(source, rebuilt) == expected


def test_lil_v22_release_stack_and_tutorial_coverage() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v22"]["batches"][:-1] == profiles["lil-deep-route-v21"]["batches"]
    assert profiles["lil-deep-route-v22"]["batches"][-1] == BATCH.as_posix()
    by_id = {row["id"]: row["english"] for row in _load(BATCH)["records"]}
    assert "Alexandria" in by_id["DK4_MES_B164_R0005"]
    assert "five holds" in by_id["DK4_MES_B164_R0166"]
    assert "marine quarters" in by_id["DK4_MES_B164_R0177"]
    assert "local fleets" in by_id["DK4_MES_B164_R0183"]
