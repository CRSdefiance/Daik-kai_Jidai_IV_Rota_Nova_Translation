from __future__ import annotations

import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch
from scripts.build_integrated_release import apply_arm9_fixed_batch

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
ARM9_BATCH = Path("translations/guild_inn_arm9_v1.json")
DESCRIPTION_BATCH = Path("translations/guild_rainbow_marbles_description_v1.json")
ITEM_NAMES_V2 = Path("translations/guild_amsterdam_item_names_v2.json")
ITEM_DESCRIPTIONS_V2 = Path("translations/guild_amsterdam_item_descriptions_v2.json")
STACK = Path("translations/release_stack.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _visible(data: bytes, offset: int, size: int) -> bytes:
    return data[offset : offset + size].split(b"\0", 1)[0]


def test_guild_and_inn_arm9_pass_covers_every_shared_role_slot() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(ids) == 17

    assert _visible(rebuilt, 0x143CDC, 16) == b"Buy Items"
    assert _visible(rebuilt, 0x143CEC, 16) == b"Sell Items"
    assert _visible(rebuilt, 0x13C2A0, 8) == b"Gift"
    assert _visible(rebuilt, 0x13E330, 8) == b"Price"
    assert _visible(rebuilt, 0x15D5C4, 16) == b"Rainbow Marbles"

    pitch = _visible(rebuilt, 0x143D20, 88)
    assert pitch == b"You're in luck!\n An old map here points to a legendary treasure."
    assert b"\n " in pitch

    for offset in (0x15E284, 0x15E294, 0x15E2B4, 0x15E2C4, 0x15E2D4, 0x15E2E4, 0x15E2F4):
        assert _visible(rebuilt, offset, 16) == b"Innkeeper"
    for offset in (0x15E304, 0x15E324, 0x15E334, 0x15E344):
        assert _visible(rebuilt, offset, 16) == b"Guildmaster"


def test_rainbow_marbles_packed_description_preserves_neighbors_and_offsets() -> None:
    source_file = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows = materialize_translation_batch(_load(DESCRIPTION_BATCH), source_file)
    rebuilt_file = rebuild_mesfile(source_file, rows)
    source = IlnkContainer.parse(source_file).blocks[32].split(b"\0")[12]
    rebuilt = IlnkContainer.parse(rebuilt_file).blocks[32].split(b"\0")[12]

    first_end = 1 + 88
    rainbow_end = first_end + 92
    assert len(source) == len(rebuilt) == 267
    assert rebuilt[:first_end] == source[:first_end]
    assert rebuilt[rainbow_end:] == source[rainbow_end:]
    rainbow = rebuilt[first_end:rainbow_end]
    assert rainbow.startswith(b" Rainbow-colored glass marbles")
    assert rainbow.rstrip().endswith(b"known only to their makers.")
    assert rainbow[0] == 0x20
    rainbow.decode("ascii")


def test_guild_inn_v3_profile_keeps_all_layers_together() -> None:
    profile = _load(STACK)["profiles"]["lil-b22-intro-guild-inn-v3"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        "translations/lil_sc2_b22_intro_natural_v2.json",
        "translations/lil_shared_names_port_fleet_arm9_v1.json",
        ARM9_BATCH.as_posix(),
        "translations/common_crew_join_leading_guard_v2.json",
        DESCRIPTION_BATCH.as_posix(),
    ]


def test_all_three_amsterdam_guild_item_names_are_english() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(ITEM_NAMES_V2, source)
    assert ids == ["DK4_ITEM_HUIZONG_ART", "DK4_ITEM_SNOW_SILK_ROBE"]
    assert _visible(source, 0x15D5C4, 16).decode("cp932") == "虹色のビー玉"
    assert _visible(rebuilt, 0x15D5D4, 16) == b"Huizong Art"
    assert _visible(rebuilt, 0x15D5F4, 16) == b"Snow-Silk Robe"


def test_all_three_amsterdam_guild_item_descriptions_preserve_packed_neighbors() -> None:
    source_file = NdsImage.open(BASE).read_file("/COMMON/MESFILE.DK4")
    rows = materialize_translation_batch(_load(ITEM_DESCRIPTIONS_V2), source_file)
    rebuilt_file = rebuild_mesfile(source_file, rows)
    source = IlnkContainer.parse(source_file).blocks[32].split(b"\0")
    rebuilt = IlnkContainer.parse(rebuilt_file).blocks[32].split(b"\0")

    assert len(rows) == 3
    assert len(rebuilt[12]) == len(source[12]) == 267
    assert rebuilt[12][:89] == source[12][:89]
    assert rebuilt[12][181:] == source[12][181:]
    assert rebuilt[12][89:181].startswith(b" Rainbow-colored glass marbles")

    assert len(rebuilt[13]) == len(source[13]) == 267
    assert rebuilt[13][:77] == source[13][:77]
    assert rebuilt[13][177:] == source[13][177:]
    assert rebuilt[13][77:177].startswith(b" A graceful watercolor painted by Huizong")

    assert len(rebuilt[19]) == len(source[19]) == 79
    assert rebuilt[19].startswith(b" A light, soft silk robe")
    rebuilt[12][89:181].decode("ascii")
    rebuilt[13][77:177].decode("ascii")
    rebuilt[19].decode("ascii")


def test_guild_inn_v4_profile_includes_every_amsterdam_item() -> None:
    profile = _load(STACK)["profiles"]["lil-b22-intro-guild-inn-v4"]
    assert profile["status"] == "experimental"
    assert profile["batches"] == [
        "translations/lil_sc2_b22_intro_natural_v2.json",
        "translations/lil_shared_names_port_fleet_arm9_v1.json",
        ARM9_BATCH.as_posix(),
        ITEM_NAMES_V2.as_posix(),
        "translations/common_crew_join_leading_guard_v2.json",
        ITEM_DESCRIPTIONS_V2.as_posix(),
    ]
