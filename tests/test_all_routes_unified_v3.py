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


def test_unified_v3_preserves_all_four_route_stacks() -> None:
    profiles = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))["profiles"]
    profile = profiles["all-routes-unified-v3"]
    batches = profile["batches"]
    assert profile["status"] == "experimental" and profile["require_screen_entry_layout"]
    assert len(batches) == len(set(batches)) == 304
    assert batches[:290] == profiles["all-routes-unified-v2"]["batches"]
    assert set(profiles["lil-deep-route-v37"]["batches"]) <= set(batches)
    assert set(profiles["maria-deep-route-v111"]["batches"]) <= set(batches)
    assert sum("raphael_deep_route" in name for name in batches) == 95
    assert sum("hodram_deep_route" in name for name in batches) == 46
    assert sum("lil_deep_route" in name for name in batches) == 37
    assert sum("maria_deep_route" in name for name in batches) == 111


def test_lil_v37_preserves_clifford_voice_letter_and_macros() -> None:
    batch = json.loads(Path("translations/lil_deep_route_v37.json").read_text(encoding="utf-8"))
    assert batch["inventory"] == {"identified_records": 30, "translated_records": 30, "blocks": {"122": 30}}
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(batch["dialogue_profile"])
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert profile.macro_ascii_lengths["FI"] == 3
    leads = set()
    macros = set()
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
        assert raw.count(b"FI") == encoded.count(b"FI"), row["id"]
        if "{MACRO:FI}" in english:
            macros.add(int(row["id"].rsplit("R", 1)[1]))
    assert leads == {2, 9, 0x97, 0xFE}
    assert macros == {58, 121, 162}
    expected = {(122, int(row["id"].rsplit("R", 1)[1])) for row in rows}
    assert len(expected) == 30
    assert changed_segments(source, rebuild_mesfile(source, rows)) == expected
