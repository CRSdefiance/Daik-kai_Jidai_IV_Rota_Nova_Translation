from __future__ import annotations

import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_arm9_fixed_batch
from scripts.materialize_all_item_names_v1 import COUNT, ENGLISH, FREE_SIZE, FREE_START, TABLE

BASE = Path("out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds")
BATCH = Path("translations/all_item_names_arm9_v1.json")
STACK = Path("translations/release_stack.json")


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _c_string(data: bytes, offset: int) -> bytes:
    return data[offset:data.index(0, offset)]


def test_all_218_runtime_item_names_are_complete_ascii() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(BATCH, source)
    assert COUNT == len(ENGLISH) == 218
    assert len(ids) == 384

    for index, expected in enumerate(ENGLISH):
        pointer = struct.unpack_from("<I", rebuilt, TABLE + index * 0x18)[0]
        offset = pointer - 0x02000000
        visible = _c_string(rebuilt, offset)
        assert visible.decode("ascii") == expected


def test_relocation_pool_stays_inside_verified_zero_run() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    batch = _load(BATCH)
    pool = next(record for record in batch["records"] if record["id"] == "DK4_ITEM_NAME_RELOCATION_POOL")
    assert pool["offset"] == FREE_START
    assert len(bytes.fromhex(pool["source_hex"])) == FREE_SIZE
    assert set(bytes.fromhex(pool["source_hex"])) == {0}
    assert bytes.fromhex(pool["replacement_hex"])[-1] == 0
    assert source[FREE_START:FREE_START + FREE_SIZE] == bytes(FREE_SIZE)


def test_item_table_boundary_does_not_touch_country_table() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, _ = apply_arm9_fixed_batch(BATCH, source)
    country_record = TABLE + COUNT * 0x18
    assert rebuilt[country_record:country_record + 0x18] == source[country_record:country_record + 0x18]
    country_pointer = struct.unpack_from("<I", rebuilt, country_record)[0]
    assert _c_string(rebuilt, country_pointer - 0x02000000).decode("cp932") == "イギリス"


def test_v5_profile_contains_global_catalogue_without_name_overlap() -> None:
    profile = _load(STACK)["profiles"]["lil-b22-intro-all-items-v5"]
    assert profile["status"] == "accepted-baked"
    assert profile["batches"] == [
        "translations/lil_sc2_b22_intro_natural_v2.json",
        "translations/lil_shared_names_port_fleet_arm9_v1.json",
        "translations/guild_inn_ui_arm9_v2.json",
        BATCH.as_posix(),
        "translations/common_crew_join_leading_guard_v2.json",
        "translations/guild_amsterdam_item_descriptions_v2.json",
    ]
    guild_ids = {record["id"] for record in _load(Path("translations/guild_inn_ui_arm9_v2.json"))["records"]}
    assert "DK4_ITEM_RAINBOW_MARBLES" not in guild_ids
