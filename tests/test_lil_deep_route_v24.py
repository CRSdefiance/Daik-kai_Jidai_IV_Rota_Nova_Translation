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
BATCH = Path("translations/lil_deep_route_v24.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v24_source_locked_records_fit_and_change_only_their_segments() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 51,
        "translated_records": 51,
        "blocks": {"99": 5, "119": 22, "165": 24},
    }
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    for row in rows:
        audit = audit_fixed_dialogue_record(bytes.fromhex(row["source_hex"]), row["english"], profile)
        blocking = [issue for issue in audit["issues"] if issue["severity"] in {"error", "warning"}]
        assert not blocking, (row["id"], blocking)
    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_R", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 51
    assert changed_segments(source, rebuilt) == expected


def test_lil_v24_is_registered_as_an_experimental_extension() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v24"]["status"] == "experimental"
    assert profiles["lil-deep-route-v24"]["batches"][:-1] == profiles["lil-deep-route-v23"]["batches"]
    assert profiles["lil-deep-route-v24"]["batches"][-1] == BATCH.as_posix()
