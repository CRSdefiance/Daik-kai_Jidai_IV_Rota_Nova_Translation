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
BATCH = Path("translations/lil_deep_route_v35.json")
SPEAKER_BYTES = {0x02, 0x09, 0xFE}
TEXT_LEADS = {0x82, 0x95}
MACRO_IDS = {"DK4_MES_B120_R0009", "DK4_MES_B120_R0027"}
INHERITED = "DK4_MES_B120_R0012"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v35_preserves_tutorial_states_macros_and_bare_text() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 29,
        "translated_records": 28,
        "inherited_records": [INHERITED],
        "blocks": {"120": 28},
    }
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert profile.macro_ascii_lengths["FI"] == 3
    assert SPEAKER_BYTES <= profile.leading_speaker_bytes
    assert TEXT_LEADS.isdisjoint(profile.leading_speaker_bytes)
    seen = set()
    macros = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        lead = raw[0]
        seen.add(lead)
        target = row["english"]
        issues = audit_fixed_dialogue_record(raw, target, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, target, profile).encoded
        if lead in SPEAKER_BYTES:
            assert target.startswith(f"{{SPEAKER:{lead:02X}}}"), row["id"]
            assert encoded[0] == lead, row["id"]
        else:
            assert lead in TEXT_LEADS, row["id"]
            assert not target.startswith("{SPEAKER:"), row["id"]
            assert encoded[0] == ord(target[0]), row["id"]
        if "{MACRO:FI}" in target:
            macros.add(row["id"])
            assert raw.count(b"FI") == encoded.count(b"FI") == 1
    assert seen == SPEAKER_BYTES | TEXT_LEADS
    assert macros == MACRO_IDS
    expected = {
        (120, int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 28 and (120, 12) not in expected
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_v35_extends_v34_and_inherits_v21_refusal() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    batches = profiles["lil-deep-route-v35"]["batches"]
    assert profiles["lil-deep-route-v35"]["status"] == "experimental"
    assert batches[:-1] == profiles["lil-deep-route-v34"]["batches"]
    assert batches[-1] == BATCH.as_posix()
    assert "translations/lil_deep_route_v21.json" in batches
    inherited = _load(Path("translations/lil_deep_route_v21.json"))["records"]
    assert any(row["id"] == INHERITED for row in inherited)
