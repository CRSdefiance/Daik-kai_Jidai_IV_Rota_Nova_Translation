from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import GLOBAL_NAME_ENTRIES
from scripts.build_integrated_release import (
    apply_arm9_fixed_batch,
    apply_pxl_native_label_batch,
    resolve_release_batches,
)

BASE = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
ARM9_BATCH = Path("translations/route_forces_arm9_v1.json")
FORCE_GRAPHICS_BATCH = Path("translations/force_info_graphics_v2.json")
SHIPS_GRAPHICS_BATCH = Path("translations/ships_submenu_graphics_v2.json")
SHIPS_ARM9_BATCH = Path("translations/ships_submenu_arm9_v1.json")

CITY_OBJECT_START = 0x1225D0
CITY_OBJECT_END = 0x125890
CITY_OBJECT_SIZE = 0x74
ARM9_LOAD_ADDRESS = 0x02000000
CITY_SIGNATURE = bytes.fromhex("7D000C00")

EXPECTED_LIVE_CITY_NAMES = [
    "Bristol",
    "Amsterdam",
    "Bruges",
    "Nantes",
    "Hamburg",
    "Lubeck",
    "Stockholm",
    "Oslo",
    "Copenhagen",
    "Riga",
    "Lisbon",
    "Ceuta",
    "Seville",
    "Valencia",
    "Genoa",
    "Marseille",
    "Syracuse",
    "Venice",
    "Athens",
    "Crete",
    "Cyprus",
    "Istanbul",
    "Ragusa",
    "Beirut",
    "Alexandria",
    "Tripoli",
    "Algiers",
    "Tunis",
    "Sao Jorge",
    "Madeira",
    "Las Palmas",
    "Verde",
    "Luanda",
    "Sofala",
    "Cape Town",
    "Mozambique",
    "Mogadishu",
    "Basra",
    "Aden",
    "Muscat",
    "Hormuz",
    "Calicut",
    "Goa",
    "Ceylon",
    "Calcutta",
    "Ava",
    "Malacca",
    "Brunei",
    "Manila",
    "Batavia",
    "Palembang",
    "Ternate",
    "Amboyna",
    "Hangzhou",
    "Quanzhou",
    "Macao",
    "Seoul",
    "Nagasaki",
    "Osaka",
    "Naha",
    "Havana",
    "Santo Domingo",
    "San Juan",
    "Jamaica",
    "Veracruz",
    "Merida",
    "Portobelo",
    "Maracaibo",
    "Pernambuco",
    "Trujillo",
    "Cayenne",
    "Sierra Leone",
    "Sao Tome",
    "Madagascar",
    "Mombasa",
    "Socotra",
    "Diu",
    "Madras",
    "Masulipatam",
    "Achin",
    "Giadin",
    "Banjarmasin",
    "Makassar",
    "Surabaya",
    "Yizhou",
    "Pensacola",
    "Abhaz",
    "Lelystad",
    "Tamsui",
    "Inuvik",
    "Hawaii",
    "Rio de Janeiro",
    "Churchill",
    "Valparaiso",
    "Nome",
    "Cod",
    "Montevideo",
    "Hekla",
    "Karibib",
    "Forel",
    "Tahiti",
    "Dixon",
    "Azores",
    "Santa Barbara",
    "Narvik",
    "Lebeque",
    "Callao",
    "Ezo",
    "Perth",
    "Guam",
    "Tsukushi",
    "Corfu",
    "Wanganui",
]

EXPECTED_FORCE_NAMES = [
    "Castor Co.",
    "Argot Co.",
    "Bergstrom Fleet",
    "Li Clan",
    "Clifford",
    "Speyer Co.",
    "Albuquerque",
    "Valdes",
    "Centurione Co.",
    "Pasha",
    "Hayreddin Clan",
    "Silveira Co.",
    "Espinosa Co.",
    "Uddin Co.",
    "Nagarpur Co.",
    "Pereira",
    "Kuhn",
    "Kurushima",
    "Maldonado",
    "Escante",
]


def _live_city_names(arm9: bytes) -> list[str]:
    names: list[str] = []
    for object_offset in range(
        CITY_OBJECT_START, CITY_OBJECT_END + 1, CITY_OBJECT_SIZE
    ):
        assert arm9[object_offset : object_offset + 4] == CITY_SIGNATURE
        runtime_pointer = struct.unpack_from("<I", arm9, object_offset + 4)[0]
        name_offset = runtime_pointer - ARM9_LOAD_ADDRESS
        assert 0 <= name_offset < len(arm9)
        terminator = arm9.find(b"\0", name_offset, name_offset + 21)
        assert terminator >= 0, f"unterminated city name at {object_offset:#x}"
        names.append(arm9[name_offset:terminator].decode("ascii"))
    return names


def test_combined_profile_contains_ships_route_cities_and_forces() -> None:
    with pytest.raises(ValueError, match="accepted-baked"):
        resolve_release_batches("ships-route-forces-v1", [])


def test_every_live_route_city_is_terminated_english() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, ids = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert len(ids) == 67
    assert len(EXPECTED_LIVE_CITY_NAMES) == 113
    assert _live_city_names(rebuilt) == EXPECTED_LIVE_CITY_NAMES


def test_coordinate_and_forces_runtime_text_are_pair_safe() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, _ = apply_arm9_fixed_batch(ARM9_BATCH, source)
    assert rebuilt[0x140490 : 0x1404A8] == b"\n %s %3d %s %3d".ljust(24, b"\0")
    assert rebuilt[0x14C114 : 0x14C120] == b"Switch\0".ljust(12, b"\0")
    assert rebuilt[0x14C120 : 0x14C138] == (b"Done\0".ljust(8, b"\0") * 3)
    assert rebuilt[0x14C138 : 0x14C144] == b"Switch\0".ljust(12, b"\0")
    assert rebuilt[0x14C144 : 0x14C14C] == b"Done\0".ljust(8, b"\0")
    assert rebuilt[0x14C14C : 0x14C154] == b"Area\0\0\0\0"
    assert rebuilt[0x14C154 : 0x14C15C] == b"Area\0\0\0\0"
    assert rebuilt[0x14C164 : 0x14C17C] == (b"Done\0".ljust(8, b"\0") * 3)
    assert rebuilt[0x14C17C : 0x14C184] == b"Map \0\0\0\0"
    assert rebuilt[0x14C184 : 0x14C190] == b"World Map\0".ljust(12, b"\0")
    assert rebuilt[0x14C190 : 0x14C19C] == b"Fleet/Town\0".ljust(12, b"\0")
    assert rebuilt[0x14C19C : 0x14C1A4] == b"Area\0\0\0\0"
    assert rebuilt[0x14C1A4 : 0x14C1B8] == b": select one.\0".ljust(20, b"\0")
    assert rebuilt[0x14C1B8 : 0x14C1D0] == b"Press X to change\0".ljust(24, b"\0")
    assert rebuilt[0x14C1D0 : 0x14C1E4] == b"selection type.\0".ljust(20, b"\0")
    assert rebuilt[0x14C1E8 : 0x14C1F4] == b"Leader (%s)\0"
    assert rebuilt[0x14C1FC : 0x14C20C] == b"(Unknown Force)\0"
    assert rebuilt[0x14C79C : 0x14C7E8].decode("ascii")
    assert rebuilt[0x15E78C : 0x15E7A0] == b"Hayreddin Clan\0".ljust(20, b"\0")
    assert rebuilt[0x15E7A0 : 0x15E7B4] == b"Silveira Co.\0".ljust(20, b"\0")
    assert rebuilt[0x15E7B4 : 0x15E7C8] == b"Uddin Co.\0".ljust(20, b"\0")
    assert rebuilt[0x15E9BC : 0x15E9D0] == b"Centurione Co.\0".ljust(20, b"\0")


def test_all_profiled_sailor_names_are_ascii_in_accepted_base() -> None:
    arm9 = NdsImage.open(BASE).read_file("/__arm9__.bin")
    assert len(GLOBAL_NAME_ENTRIES) == 190
    for entry in GLOBAL_NAME_ENTRIES:
        if entry.offset == 0x15E96C:
            assert arm9[entry.offset : entry.offset + entry.source_length] == entry.expected_bytes
            continue
        visible = arm9[entry.offset : entry.offset + entry.source_length].split(b"\0", 1)[0]
        assert visible.decode("ascii"), entry.row_id


def test_every_named_force_record_resolves_to_english() -> None:
    source = NdsImage.open(BASE).read_file("/__arm9__.bin")
    rebuilt, _ = apply_arm9_fixed_batch(ARM9_BATCH, source)
    names = []
    for pointer_offset in range(0x11BC70, 0x11C180, 0x44):
        pointer = struct.unpack_from("<I", rebuilt, pointer_offset)[0]
        name_offset = pointer - ARM9_LOAD_ADDRESS
        terminator = rebuilt.index(0, name_offset)
        names.append(rebuilt[name_offset:terminator].decode("ascii"))
    assert names == EXPECTED_FORCE_NAMES


def test_forces_plaques_use_native_font_and_preserve_other_pixels() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/_pxl/forceinfo.pxl")
    arm9 = image.read_file("/__arm9__.bin")
    batch = json.loads(FORCE_GRAPHICS_BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]
    assert all("background_indices_zlib_hex" in record for record in batch["records"])

    rebuilt, ids = apply_pxl_native_label_batch(FORCE_GRAPHICS_BATCH, source, arm9)
    assert len(ids) == 5
    assert len(rebuilt) == len(source)
    before = PxlImage.from_bytes(source)
    after = PxlImage.from_bytes(rebuilt)
    boxes = [tuple(record["box"]) for record in batch["records"]]
    for y in range(before.height):
        for x in range(before.width):
            if not any(
                left <= x < right and top <= y < bottom
                for left, top, right, bottom in boxes
            ):
                position = y * before.width + x
                assert after.indices[position] == before.indices[position]
