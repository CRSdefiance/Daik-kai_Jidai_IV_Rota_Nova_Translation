from __future__ import annotations

import json
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import audit_fixed_dialogue_record
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import apply_arm9_fixed_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
ARM9_BATCH = Path("translations/cargo_port_sea_ui_arm9_v1.json")
STORY_BATCH = Path("translations/hodram_sc1_b127_sailing_tutorial_v1.json")
STACK = Path("translations/release_stack.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_cargo_and_sea_ui_are_complete_terminated_ascii() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    records = _load(ARM9_BATCH)["records"]
    assert isinstance(records, list)
    assert len(ids) == len(records) == 12
    for record in records:
        offset = int(record["offset"])
        size = len(bytes.fromhex(str(record["source_hex"])))
        value = rebuilt[offset : offset + size]
        assert value.rstrip(b"\0").isascii()
        assert b"\0" in value

    assert rebuilt[0x11B57C : 0x11B584].startswith(b"Menu\0")
    assert rebuilt[0x11B5B4 : 0x11B5BC].startswith(b"Unload\0")
    assert rebuilt[0x14A03C : 0x14A05C].startswith(b"Is this cargo setup okay?\0")
    assert rebuilt[0x14A05C : 0x14A078] == b"Move cargo to another ship.\0"
    assert rebuilt[0x14A078 : 0x14A088].startswith(b"%s Cargo Setup\0")
    assert rebuilt[0x147F18 : 0x147F24].startswith(b"Sky: Sunny\0")


def test_hodram_sailing_tutorial_is_complete_fixed_and_qa_clean() -> None:
    source = NdsImage.open(BASE).read_file("/data/SC1.DK4")
    batch = _load(STORY_BATCH)
    rows = materialize_translation_batch(batch, source)
    profile = get_dialogue_profile("hodram-story-probe")
    assert len(rows) == 10
    for row in rows:
        audit = audit_fixed_dialogue_record(
            bytes.fromhex(str(row["source_hex"])), str(row["english"]), profile
        )
        assert not [
            issue for issue in audit["issues"] if issue["severity"] in {"warning", "error"}
        ]


def test_unified_profile_keeps_every_reported_layer_together() -> None:
    profile = _load(STACK)["profiles"]["hodram-port-cargo-sailing-v1"]
    assert profile["status"] == "experimental"
    assert profile["batches"][-2:] == [ARM9_BATCH.as_posix(), STORY_BATCH.as_posix()]
    assert "translations/common_port_departure_guard_v1.json" in profile["batches"]
