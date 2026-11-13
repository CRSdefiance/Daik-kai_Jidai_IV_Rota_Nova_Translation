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
BATCH = Path("translations/lil_deep_route_v27.json")
SPEAKER_BYTES = {0x02, 0x09, 0x10, 0x14, 0xA0, 0xB1, 0xB2, 0xD0}
TEXT_LEADS = {0x82, 0x89, 0x92}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v27_records_fit_preserve_controls_and_first_text_characters() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 55,
        "translated_records": 55,
        "blocks": {"106": 45, "108": 10},
    }
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert {0xA0, 0xB1, 0xB2} <= profile.leading_speaker_bytes
    assert TEXT_LEADS.isdisjoint(profile.leading_speaker_bytes)

    seen = set()
    for row in rows:
        source_raw = bytes.fromhex(row["source_hex"])
        target = row["english"]
        audit = audit_fixed_dialogue_record(source_raw, target, profile)
        blocking = [issue for issue in audit["issues"] if issue["severity"] in {"error", "warning"}]
        assert not blocking, (row["id"], blocking)
        encoded = encode_fixed_dialogue(source_raw, target, profile).encoded
        lead = source_raw[0]
        seen.add(lead)
        if lead in SPEAKER_BYTES:
            assert target.startswith(f"{{SPEAKER:{lead:02X}}}"), row["id"]
            assert encoded[0] == lead, row["id"]
        else:
            assert lead in TEXT_LEADS, row["id"]
            assert not target.startswith("{SPEAKER:"), row["id"]
            assert encoded[0] == ord(target[0]), row["id"]
    assert {0x89, 0xA0, 0xB1, 0xB2} <= seen

    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_R", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 55
    assert changed_segments(source, rebuilt) == expected


def test_lil_v27_is_registered_as_an_experimental_extension() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v27"]["status"] == "experimental"
    assert profiles["lil-deep-route-v27"]["batches"][:-1] == profiles["lil-deep-route-v26"]["batches"]
    assert profiles["lil-deep-route-v27"]["batches"][-1] == BATCH.as_posix()
