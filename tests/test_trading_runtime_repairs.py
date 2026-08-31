from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import PROFILES
from scripts.build_integrated_release import (
    apply_arm9_fixed_batch,
    apply_pxl_label_batches,
)
from scripts.materialize_tavern_runtime_entry_repairs import RUNTIME_RECORDS
from scripts.materialize_trader_tutorial_repair import PACKED_RECORDS

BASE = Path("out/raphael_natural_v2_pre_common_accepted_rollback.nds")
ARM9_BATCH = Path("translations/trading_runtime_arm9_v1.json")
PXL_BATCH = Path("translations/trading_towninfo_graphics_v1.json")
STACK = Path("translations/release_stack.json")
ARM9_SHA256 = "ba0d426b975280a51d503f38b62baeda0a7cf21fc18f962dd0ddeb2f36450dd1"
TOWNINFO_SHA256 = "a84e60e030303da06df123aba5155ec6bd61056b598f189008c9aa45766409da"

PROFILE_BATCHES = [
    "translations/hodram_intro_natural_v2_sc1_b42_b44.json",
    "translations/hodram_stockholm_tavern_natural_v2_sc1_b134.json",
    "translations/hodram_stockholm_dock_natural_v2_sc1_b135.json",
    "translations/hodram_stockholm_market_natural_v2_sc1_b136.json",
    "translations/hodram_gerhard_nameplate_arm9_v1.json",
    "translations/tutorial_tavern_recruit_natural_v2.json",
    "translations/stockholm_tavern_interior_fixed_v1.json",
    "translations/stockholm_tavern_rumor_natural_v2.json",
    "translations/trader_tutorial_natural_v2.json",
    "translations/trader_tutorial_interior_fixed_v1.json",
    "translations/trader_market_map_arm9_v1.json",
    "translations/trading_runtime_arm9_v1.json",
    "translations/trading_towninfo_graphics_v1.json",
]


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_runtime_arm9_repairs_are_source_locked_terminated_and_nonoverlapping() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    assert hashlib.sha256(source).hexdigest() == ARM9_SHA256
    batch = load(ARM9_BATCH)
    rebuilt, changed = apply_arm9_fixed_batch(ARM9_BATCH, source)
    records = batch["records"]
    assert changed == [record["id"] for record in records]

    claimed: set[int] = set()
    for record in records:
        offset = int(record["offset"])
        size = len(bytes.fromhex(str(record["source_hex"])))
        replacement = rebuilt[offset : offset + size]
        assert replacement.startswith(str(record["english"]).encode("ascii") + b"\0")
        positions = set(range(offset, offset + size))
        assert not claimed & positions
        claimed |= positions

    assert b"Iron OreLiFam" not in rebuilt
    assert rebuilt[0x15BD58 : 0x15BD60] == b"Iron\0\0\0\0"
    assert rebuilt[0x15BD60 : 0x15BD68] == b"Li Clan\0"
    assert rebuilt[0x15BFB0 : 0x15BFB8] == b"P. Oil\0\0"
    assert rebuilt[0x15E778 : 0x15E78C].startswith(b"Speyer Co.\0")


def test_all_global_goods_leave_a_terminator_in_their_fixed_slots() -> None:
    goods = [entry for entry in PROFILES["all"] if entry.context == "Global commodity name"]
    assert goods
    assert all(len(entry.suggested_english.encode("ascii")) < entry.source_length for entry in goods)


def test_runtime_dialogue_inventories_cover_reported_prefixes() -> None:
    assert set(PACKED_RECORDS) >= {
        "DK4_MES_B00_R0009",
        "DK4_MES_B00_R0011",
        "DK4_MES_B00_R0012",
        "DK4_MES_B09_R0030",
        "DK4_MES_B09_R0041",
        "DK4_MES_B09_R0042",
        "DK4_MES_B09_R0043",
        "DK4_MES_B09_R0044",
    }
    assert RUNTIME_RECORDS["DK4_MES_B00_R0037"]["entries"][1] == (21, "5 coins.")
    assert RUNTIME_RECORDS["DK4_MES_B00_R0039"]["entries"][0] == (2, "Hey, %s!")
    assert RUNTIME_RECORDS["DK4_MES_B00_R0042"]["entries"][0][0] == 2
    assert RUNTIME_RECORDS["DK4_MES_B10_R0039"]["entries"][1] == (
        22,
        "%s serves %s as %s.",
    )


def test_towninfo_redraw_changes_only_declared_boxes() -> None:
    source = NdsImage.open(BASE).read_file("/_pxl/towninfo.pxl")
    assert hashlib.sha256(source).hexdigest() == TOWNINFO_SHA256
    rebuilt, changed = apply_pxl_label_batches([PXL_BATCH], source)
    batch = load(PXL_BATCH)
    assert changed == [record["id"] for record in batch["records"]]
    before = PxlImage.from_bytes(source)
    after = PxlImage.from_bytes(rebuilt)
    assert (after.width, after.height, len(rebuilt)) == (
        before.width,
        before.height,
        len(source),
    )
    boxes = [tuple(int(value) for value in record["box"]) for record in batch["records"]]
    for position, (old, new) in enumerate(zip(before.indices, after.indices, strict=True)):
        if old == new:
            continue
        x = position % before.width
        y = position // before.width
        assert any(left <= x < right and top <= y < bottom for left, top, right, bottom in boxes)


def test_trading_profile_registers_the_complete_integrated_pass() -> None:
    profile = load(STACK)["profiles"]["hodram-trading-complete"]
    assert profile["status"] == "accepted-baked"
    assert profile["batches"] == PROFILE_BATCHES
