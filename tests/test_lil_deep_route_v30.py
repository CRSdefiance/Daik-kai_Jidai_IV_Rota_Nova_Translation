from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import changed_segments

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
BATCH = Path("translations/lil_deep_route_v30.json")
ELLIPSES = {"DK4_MES_B111_R0062", "DK4_MES_B111_R0138"}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v30_monk_state_and_name_macro_are_source_locked() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 35,
        "translated_records": 33,
        "blocks": {"111": 33},
    }
    assert set(batch["excluded_records"]) == ELLIPSES
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert {0x02, 0x09, 0x89} <= profile.leading_speaker_bytes

    seen = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        lead = raw[0]
        seen.add(lead)
        assert lead in {0x02, 0x09, 0x89}, row["id"]
        target = row["english"]
        assert target.startswith(f"{{SPEAKER:{lead:02X}}}"), row["id"]
        issues = audit_fixed_dialogue_record(raw, target, profile)["issues"]
        blocking = [issue for issue in issues if issue["severity"] in {"error", "warning"}]
        assert not blocking, (row["id"], blocking)
        encoded = encode_fixed_dialogue(raw, target, profile).encoded
        assert encoded[0] == lead, row["id"]
        if row["id"] == "DK4_MES_B111_R0112":
            assert "{MACRO:FI}" in target
            assert b"FI" in raw and b"FI" in encoded
    assert seen == {0x02, 0x09, 0x89}

    rebuilt = rebuild_mesfile(source, rows)
    expected = {(111, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 33
    assert (111, 62) not in expected and (111, 138) not in expected
    assert changed_segments(source, rebuilt) == expected


def test_lil_v30_is_registered_as_an_experimental_extension() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v30"]["status"] == "experimental"
    assert profiles["lil-deep-route-v30"]["batches"][:-1] == profiles["lil-deep-route-v29"]["batches"]
    assert profiles["lil-deep-route-v30"]["batches"][-1] == BATCH.as_posix()
