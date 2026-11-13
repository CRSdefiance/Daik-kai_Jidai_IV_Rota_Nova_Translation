"""Authorized village-proximity fixture: exactly eight ship-coordinate bytes."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ARM_SHA = "236c41a67fe8ddc82181b9809c82980a08154b3dc886c44d2cb0f585f202606e"
POINT = 0x02460000


def relocate(arm, raw, village):
    if sha(arm) != ARM_SHA or len(raw) != 0x400000 or type(village) is not int or not 0 <= village < 24:
        raise ValueError("Village research requires exact V604,4MiB RAM and village0..23")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    for lo, hi in ((0xCB118, 0xCB124), (0xCACAC, 0xCACBC), (0xCB1A8, 0xCB1B4),
                   (0x2E58C, 0x2E5A8), (0x36C70, 0x36C94), (0x578E0, 0x57908),
                   (0x78654, 0x78840), (0x2C1C4, 0x2C204)):
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(offset, args=()):
        call(u, offset, args)
        return u.reg_read(UC_ARM_REG_R0)

    fleets = get(0xCB1A8)
    index = get(0x2E58C)
    fleet = fleets + 4 + index * 0x84
    ship = get(0x36C70, (fleet + 12,))
    if not BASE <= ship < BASE + len(raw) - 0x100:
        raise ValueError("No active ship; enter the sea scene before applying the fixture")
    villages = get(0xCB118)
    model = get(0xCACAC, (villages, village))
    vt = struct.unpack("<I", u.mem_read(model, 4))[0]
    assert vt == 0x0215AF74
    village_point_getter = struct.unpack("<I", u.mem_read(vt + 0x1C, 4))[0]
    call(u, village_point_getter - BASE, (POINT, model))
    village_point = list(struct.unpack("<2i", u.mem_read(POINT, 8)))
    target = [(value + 16) * 128 for value in village_point]
    before = list(struct.unpack_from("<2i", raw, ship - BASE + 16))
    after = bytearray(raw)
    struct.pack_into("<2i", after, ship - BASE + 16, *target)
    # The selector reads a cached fleet point, not the ship's fixed coordinates.
    # Preserve that cache; the original next-frame update must synchronize it.
    u.mem_write(ship + 16, struct.pack("<2i", *target))
    fvt = struct.unpack("<I", u.mem_read(fleet, 4))[0]
    getter = struct.unpack("<I", u.mem_read(fvt + 0x20, 4))[0]
    call(u, getter - BASE, (POINT, fleet))
    fleet_point = list(struct.unpack("<2i", u.mem_read(POINT, 8)))
    assert fleet_point == list(struct.unpack_from("<2i", raw, fleet - BASE + 0x34))
    changes = [{"address": BASE + i, "before": raw[i], "after": after[i]}
               for i in range(ship - BASE + 16, ship - BASE + 24) if raw[i] != after[i]]
    assert raw[:ship - BASE + 16] == after[:ship - BASE + 16]
    assert raw[ship - BASE + 24:] == after[ship - BASE + 24:]
    return bytes(after), {"synthetic_location_fixture": True, "location_kind": "village-proximity",
        "village_id": village, "village_model": model, "village_point": village_point,
        "selector_cached_point_before_original_update": fleet_point,
        "expected_selector_point_after_original_update": [value + 16 for value in village_point],
        "fleet_point_cache_preserved_pending_original_update": True,
        "active_fleet": fleet, "active_ship": ship,
        "before_ship_fixed_point": before, "after_ship_fixed_point": target,
        "only_eight_ship_coordinate_bytes_owned": True, "changes": changes,
        "no_discovery_development_dialogue_resource_or_scene_flags_changed": True,
        "normal_travel_verified": False, "original_village_logic_must_still_run": True,
        "before_RAM_sha256": sha(raw), "after_RAM_sha256": sha(after)}
