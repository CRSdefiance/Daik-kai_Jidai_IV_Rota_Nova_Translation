"""Explicit one-byte ship-layout research fixture; not acquisition or a full refit."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

BASE, SHIP, MASTER = 0x02000000, 0x022D9E94, 0x022D94CC
VERIFIED_ARMS = {
    "85d1b032ebdb16a4337f43de46b4bca4207b7ded8d763ef71eb1960791db0fe7",
    "0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731",
}


def set_ship_type(arm, raw, ship_type):
    if sha(arm) not in VERIFIED_ARMS or len(raw) != 0x400000:
        raise ValueError("Ship layout fixture requires exact V599/clean ARM9 and 4 MiB RAM")
    if type(ship_type) is not int or ship_type not in (11, 33):
        raise ValueError("Only the original Brigantine/Ironclad layout cases are owned")
    if arm[0x11DB0:0x11DB8] != bytes.fromhex("4900d0e51eff2fe1"):
        raise ValueError("Original ship type getter differs")
    at = SHIP - BASE
    if struct.unpack_from("<2I", raw, at) != (0x0215EE94, 0x0215EEF8):
        raise ValueError("Actual source-save ship vtables differ")
    if raw[at + 8:at + 24].split(b"\0")[0] != b"Vestaros":
        raise ValueError("Fixture does not point to the named test ship")
    if raw[at + 0x49] not in (11, 33):
        raise ValueError("Prior ship type is outside the owned pair")
    entry = MASTER + 4 + ship_type * 64
    vt, secondary, name_pointer = struct.unpack_from("<3I", raw, entry - BASE)
    if (vt, secondary) != (0x0215EE20, 0x0215EE6C) or not BASE <= name_pointer < BASE + len(raw) - 64:
        raise ValueError("Original ship-type record/name contract differs")
    name = raw[name_pointer - BASE:name_pointer - BASE + 64].split(b"\0")[0].decode("cp932")
    expected = ("Brigantine", "ブリガンティン") if ship_type == 11 else ("Ironclad", "鉄甲船")
    if name not in expected:
        raise ValueError("Requested ship-type identity differs: " + name)
    uc = machine(arm)
    uc.mem_write(BASE, raw)
    call(uc, 0x11DB0, (SHIP,))
    assert uc.reg_read(UC_ARM_REG_R0) == raw[at + 0x49]
    after = bytearray(raw)
    after[at + 0x49] = ship_type
    changes = [{"address": SHIP + 0x49, "before": raw[at + 0x49], "after": ship_type}]
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == int(raw[at + 0x49] != ship_type)
    return bytes(after), {"synthetic_ship_type_fixture": True, "normal_acquisition_or_refit_verified": False,
        "existing_room_layout_and_stats_not_rebuilt": True,
        "scope": "Only original ship-type selection and resource/display research; not a complete Ironclad model",
        "ship": SHIP, "ship_name": "Vestaros", "source_type": raw[at + 0x49], "target_type": ship_type,
        "original_master_record": entry, "original_master_name": name, "changes": changes,
        "one_type_byte_only": True, "before_RAM_sha256": sha(raw), "after_RAM_sha256": sha(after),
        "helper_sha256": sha(Path(__file__).read_bytes())}
