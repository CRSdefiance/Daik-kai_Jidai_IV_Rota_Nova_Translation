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

BATCH = Path("translations/lil_deep_route_v40.json")


def test_lil_v40_trading_choices_macro_and_presentation() -> None:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 15, "translated_records": 15, "blocks": {"126": 15}}
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert profile.macro_ascii_lengths["FI"] == 3
    assert {2, 9} <= profile.leading_speaker_bytes
    assert 0x8C not in profile.leading_speaker_bytes
    choices = {}
    macros = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        english = row["english"]
        number = int(row["id"].rsplit("R", 1)[1])
        issues = audit_fixed_dialogue_record(raw, english, profile)["issues"]
        assert not [issue for issue in issues if issue["severity"] in {"error", "warning"}], row["id"]
        encoded = encode_fixed_dialogue(raw, english, profile).encoded
        if raw[0] in {2, 9}:
            assert english.startswith(f"{{SPEAKER:{raw[0]:02X}}}")
            assert encoded[0] == raw[0]
            assert encoded[1] not in {10, 32}
        else:
            assert raw[0] == 0x8C
            assert not english.startswith("{SPEAKER:")
            assert encoded[0] == ord(english[0])
            choices[number] = chr(encoded[0])
        assert raw.count(b"FI") == encoded.count(b"FI")
        if "{MACRO:FI}" in english:
            macros.add(number)
    assert choices == {16: "H", 18: "A"}
    assert macros == {50}
    expected = {(126, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 15
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected


def test_lil_v40_and_unified_v6_extend_prior_profiles() -> None:
    profiles = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))["profiles"]
    lil = profiles["lil-deep-route-v40"]["batches"]
    unified = profiles["all-routes-unified-v6"]["batches"]
    assert lil[:-1] == profiles["lil-deep-route-v39"]["batches"]
    assert unified[:-1] == profiles["all-routes-unified-v5"]["batches"]
    assert lil[-1] == unified[-1] == BATCH.as_posix()
    assert len(lil) == 50 and len(unified) == 307
