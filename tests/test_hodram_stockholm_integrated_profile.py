from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import GLOBAL_NAME_ENTRIES, PROFILES
from scripts.build_integrated_release import apply_arm9_fixed_batch

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
LEGACY_BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
NAME_BATCH = Path("translations/hodram_gerhard_nameplate_arm9_v1.json")
STACK = Path("translations/release_stack.json")
ARM9_SHA256 = "ba0d426b975280a51d503f38b62baeda0a7cf21fc18f962dd0ddeb2f36450dd1"
PROFILE_BATCHES = [
    "translations/hodram_intro_natural_v2_sc1_b42_b44.json",
    "translations/hodram_stockholm_tavern_natural_v2_sc1_b134.json",
    "translations/hodram_stockholm_dock_natural_v2_sc1_b135.json",
    "translations/hodram_stockholm_market_natural_v2_sc1_b136.json",
    "translations/hodram_gerhard_nameplate_arm9_v1.json",
    "translations/tutorial_tavern_recruit_natural_v2.json",
    "translations/stockholm_tavern_interior_fixed_v1.json",
    "translations/stockholm_tavern_rumor_natural_v2.json",
]


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_gerhard_surname_is_a_source_locked_fixed_slot() -> None:
    arm9 = NdsImage.open(LEGACY_BASE).read_file("/__arm9__.bin")
    assert hashlib.sha256(arm9).hexdigest() == ARM9_SHA256
    batch = _load(NAME_BATCH)
    assert batch["source_file_sha256"] == ARM9_SHA256
    record = batch["records"][0]
    assert record["offset"] == 0x15E674
    assert record["english"] == "Ardelknatts"

    rebuilt, changed = apply_arm9_fixed_batch(NAME_BATCH, arm9)
    offset = int(record["offset"])
    size = len(bytes.fromhex(str(record["source_hex"])))
    assert changed == ["DK4_NAME_ARDELKNATTS_15E674"]
    assert rebuilt[offset : offset + size].rstrip(b"\0") == b"Ardelknatts"
    assert rebuilt[:offset] == arm9[:offset]
    assert rebuilt[offset + size :] == arm9[offset + size :]


def test_global_name_profile_includes_the_omitted_surname() -> None:
    matches = [entry for entry in GLOBAL_NAME_ENTRIES if entry.offset == 0x15E674]
    assert len(matches) == 1
    assert matches[0].japanese == "アーデルンカッツ"
    assert matches[0].suggested_english == "Ardelknatts"
    assert matches[0].source_length == 20


def test_stockholm_profile_registers_the_complete_feature() -> None:
    profile = _load(STACK)["profiles"]["hodram-stockholm-tavern-complete"]
    assert profile["status"] == "accepted-baked"
    assert profile["batches"] == PROFILE_BATCHES


def test_existing_stockholm_menu_labels_are_already_in_the_baseline() -> None:
    arm9 = NdsImage.open(BASE).read_file("/__arm9__.bin")
    expected = {
        "DK4_PLACE_TAVERN": b"Tavern",
        "DK4_PLACE_MARKET": b"Market",
        "DK4_PLACE_SHIPYARD": b"Yard",
        "DK4_TAVERN_RECRUIT": b"Recruit Crew",
        "DK4_TAVERN_TREAT": b"Treat Everyone",
        "DK4_TAVERN_DRINK": b"Order Drink",
    }
    entries = {
        entry.row_id: entry
        for profile_name in ("shared", "town")
        for entry in PROFILES[profile_name]
        if entry.row_id in expected
    }
    assert set(entries) == set(expected)
    for row_id, text in expected.items():
        entry = entries[row_id]
        actual = arm9[entry.offset : entry.offset + entry.source_length].rstrip(b"\0")
        assert actual == text
