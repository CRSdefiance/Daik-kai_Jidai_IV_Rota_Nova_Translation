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
BATCH = Path("translations/lil_deep_route_v28.json")
NON_PROSE = "DK4_MES_B107_R0003"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_lil_v28_temple_clue_fits_and_preserves_opening_fragment() -> None:
    batch = _load(BATCH)
    assert batch["inventory"] == {
        "identified_records": 17,
        "translated_records": 16,
        "blocks": {"107": 16},
    }
    assert list(batch["excluded_records"]) == [NON_PROSE]
    assert batch["translation_policy"] == "natural-dialogue-v2"
    source = NdsImage.open(BASE).read_file("/data/SC2.DK4")
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile(str(batch["dialogue_profile"]))
    assert profile.guard_linebreaks and profile.pair_phase_safe_breaks
    assert {0x02, 0x09, 0x97, 0xFE} <= profile.leading_speaker_bytes

    for row in rows:
        source_raw = bytes.fromhex(row["source_hex"])
        target = row["english"]
        lead = source_raw[0]
        assert target.startswith(f"{{SPEAKER:{lead:02X}}}"), row["id"]
        audit = audit_fixed_dialogue_record(source_raw, target, profile)
        blocking = [issue for issue in audit["issues"] if issue["severity"] in {"error", "warning"}]
        assert not blocking, (row["id"], blocking)
        encoded = encode_fixed_dialogue(source_raw, target, profile).encoded
        assert encoded[0] == lead, row["id"]

    rebuilt = rebuild_mesfile(source, rows)
    expected = {
        (int(row["id"].split("_B", 1)[1].split("_R", 1)[0]), int(row["id"].rsplit("R", 1)[1]))
        for row in rows
    }
    assert len(expected) == 16
    assert (107, 3) not in expected
    assert changed_segments(source, rebuilt) == expected


def test_lil_v28_is_registered_as_an_experimental_extension() -> None:
    profiles = _load(Path("translations/release_stack.json"))["profiles"]
    assert profiles["lil-deep-route-v28"]["status"] == "experimental"
    assert profiles["lil-deep-route-v28"]["batches"][:-1] == profiles["lil-deep-route-v27"]["batches"]
    assert profiles["lil-deep-route-v28"]["batches"][-1] == BATCH.as_posix()
