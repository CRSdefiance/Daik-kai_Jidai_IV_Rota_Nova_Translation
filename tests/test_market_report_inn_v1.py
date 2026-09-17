from __future__ import annotations

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import (
    apply_arm9_fixed_batches,
    validate_ascii_guard_policy,
)


BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
MARKET = Path("translations/market_report_goods_info_arm9_v1.json")
INN_TEXT = Path("translations/common_inn_dialogue_polish_v1.json")
INN_NAMES = Path("translations/innkeeper_nameplates_arm9_v1.json")
PLACEHOLDERS = Path("translations/common_placeholder_english_v1.json")
STACK = Path("translations/release_stack.json")


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_market_categories_fit_live_six_character_limit_and_goods_info_is_guarded() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batches([MARKET, INN_NAMES], source)
    assert len(ids) == 13
    assert rebuilt[0x159FE4 : 0x159FF0].startswith(b"Goods Info\0")
    assert rebuilt[0x15A058 : 0x15A064] == b"%s\n  %s %d%\0"
    assert rebuilt[0x15A074 : 0x15A080] == b"%s\n  %s %d%\0"
    assert rebuilt[0x15A0D4 : 0x15A0DC] == b"Fiber\0\0\0"
    assert rebuilt[0x15A0EC : 0x15A0F4] == b"Cond.\0\0\0"
    assert rebuilt[0x15A0FC : 0x15A104] == b"Jewels\0\0"
    assert all(len(label) <= 6 for label in (b"Fiber", b"Cond.", b"Jewels", b"Delic."))
    for offset in (0x15E284, 0x15E294, 0x15E2B4, 0x15E2C4, 0x15E2D4, 0x15E2E4, 0x15E2F4):
        assert rebuilt[offset : offset + 16].startswith(b"Innkeeper\0")


def test_inn_dialogue_is_natural_packed_and_two_byte_guarded() -> None:
    common = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    header = load(INN_TEXT)
    validate_ascii_guard_policy(INN_TEXT, header)
    rows = materialize_translation_batch(header, common)
    rebuilt = rebuild_mesfile(common, rows)
    blocks = IlnkContainer.parse(rebuilt).blocks
    assert blocks[0].split(b"\0")[46] == b" Welcome! Come in. "
    assert blocks[14].split(b"\0")[59] == b" It's 1 coin a night.\n How many nights?   "
    assert blocks[14].split(b"\0")[60] == b"  Stay %s nights? Rest up.  "
    assert blocks[14].split(b"\0")[60][18:].startswith(b"Rest up.")

    placeholder = load(PLACEHOLDERS)
    validate_ascii_guard_policy(PLACEHOLDERS, placeholder)
    checkout = next(row for row in placeholder["records"] if row["id"] == "DK4_MES_B14_R0058")
    replacement = bytes.fromhex(checkout["replacement_hex"])
    assert replacement[:14] == b"  Just 1 coin."
    assert replacement[14:].startswith(b"Sleep well!")


def test_market_and_inn_profile_keeps_the_complete_review_set_together() -> None:
    profile = load(STACK)["profiles"]["hodram-market-inn-v1"]
    assert profile["status"] == "experimental"
    for path in (MARKET, INN_TEXT, INN_NAMES):
        assert path.as_posix() in profile["batches"]
    assert profile["batches"][:10] == load(STACK)["profiles"]["hodram-port-cargo-sailing-v1"]["batches"]
