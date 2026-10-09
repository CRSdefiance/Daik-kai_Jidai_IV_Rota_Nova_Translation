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
BATCH = Path("translations/lil_deep_route_v29.json")
NON_PROSE = "DK4_MES_B109_R0281"
SPEAKER_BYTES = {0x02, 0x09, 0x97, 0xCF, 0xD0, 0xFE}
TEXT_LEADS = {0x81, 0x82, 0x83, 0x89, 0x8D, 0x92}
NAME_MACRO_IDS = {"DK4_MES_B109_R0076", "DK4_MES_B109_R0165"}


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v29_records_fit_and_preserve_first_glyphs_and_name_macros() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 74,
        "translated_records": 73,
        "blocks": {"109": 55, "110": 18},
    }
    assert list(batch["excluded_records"]) == [NON_PROSE]
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert SPEAKER_BYTES <= profile.leading_speaker_bytes
    assert TEXT_LEADS.isdisjoint(profile.leading_speaker_bytes)

    seen: set[int] = set()
    for row in rows:
        raw = bytes.fromhex(row["source_hex"])
        target = row["english"]
        lead = raw[0]
        seen.add(lead)
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
        if row["id"] in NAME_MACRO_IDS:
            assert "{MACRO:FI}" in target
            assert b"FI" in raw and b"FI" in encoded

    assert SPEAKER_BYTES <= seen
    assert TEXT_LEADS <= seen
    assert {row["id"] for row in rows if "{MACRO:FI}" in row["english"]} == NAME_MACRO_IDS

    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_R", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 73
    assert (109, 281) not in expected
    assert changed_segments(source, rebuilt) == expected


def test_lil_v29_is_registered_as_an_experimental_extension() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v29"]["status"] == "experimental"
    assert profiles["lil-deep-route-v29"]["batches"][:-1] == profiles["lil-deep-route-v28"]["batches"]
    assert profiles["lil-deep-route-v29"]["batches"][-1] == BATCH.as_posix()
