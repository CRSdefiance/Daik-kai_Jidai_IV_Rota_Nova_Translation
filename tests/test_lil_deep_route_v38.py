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

BATCH = Path("translations/lil_deep_route_v38.json")


def test_lil_v38_source_states_first_letters_and_full_scene() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 22, "translated_records": 22, "blocks": {"123": 7, "124": 15}}
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert {2, 6, 0x1A} <= profile.leading_speaker_bytes
    leads = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        leads.add(raw[0])
        assert english.startswith(f"{{SPEAKER:{raw[0]:02X}}}")
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        assert encoded[0] == raw[0]
        assert encoded[1] not in {10, 32}
    assert leads == {2, 6, 0x1A}
    expected = {(int(row["id"].split("_B", 1)[1].split("_R", 1)[0]), int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 22
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_v38_and_unified_v4_extend_prior_profiles() -> None:
    profiles = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))["profiles"]
    lil = profiles["lil-deep-route-v38"]["batches"]
    unified = profiles["all-routes-unified-v4"]["batches"]
    assert lil[:-1] == profiles["lil-deep-route-v37"]["batches"]
    assert unified[:-1] == profiles["all-routes-unified-v3"]["batches"]
    assert lil[-1] == unified[-1] == BATCH.as_posix()
    assert len(lil) == 48 and len(unified) == 305
