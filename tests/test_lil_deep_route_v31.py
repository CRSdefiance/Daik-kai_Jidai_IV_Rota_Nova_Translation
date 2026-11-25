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
BATCH = Path("translations/lil_deep_route_v31.json")
NON_PROSE = "DK4_MES_B112_R0010"
SPEAKER_BYTES = {0x02, 0xA3, 0xAA, 0xD0, 0xD6, 0xD7}
TEXT_LEADS = {0x81, 0x82, 0x8E, 0x94}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v31_preserves_rescue_states_and_first_text_characters() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 31,
        "translated_records": 30,
        "blocks": {"112": 30},
    }
    assert set(batch["excluded_records"]) == {NON_PROSE}
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert SPEAKER_BYTES <= profile.leading_speaker_bytes
    assert TEXT_LEADS.isdisjoint(profile.leading_speaker_bytes)

    seen = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        lead = raw[0]
        seen.add(lead)
        target = row["english"]
        issues = audit_fixed_dialogue_record(raw, target, profile)["issues"]
        blocking = [issue for issue in issues if issue["severity"] in {"error", "warning"}]
        assert not blocking, (row["id"], blocking)
        encoded = encode_fixed_dialogue(raw, target, profile).encoded
        if lead in SPEAKER_BYTES:
            assert target.startswith(f"{{SPEAKER:{lead:02X}}}"), row["id"]
            assert encoded[0] == lead, row["id"]
        else:
            assert lead in TEXT_LEADS, row["id"]
            assert not target.startswith("{SPEAKER:"), row["id"]
            assert encoded[0] == ord(target[0]), row["id"]
    assert seen == SPEAKER_BYTES | TEXT_LEADS

    rebuilt = rebuild_mesfile(source, rows)
    expected = {(112, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 30
    assert (112, 10) not in expected
    assert changed_segments(source, rebuilt) == expected


def test_lil_v31_is_registered_as_an_experimental_extension() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v31"]["status"] == "experimental"
    assert profiles["lil-deep-route-v31"]["batches"][:-1] == profiles["lil-deep-route-v30"]["batches"]
    assert profiles["lil-deep-route-v31"]["batches"][-1] == BATCH.as_posix()
