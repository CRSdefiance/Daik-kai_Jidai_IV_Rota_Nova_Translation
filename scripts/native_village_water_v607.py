"""Source-terrain-checked Inuvik fixture; only eight ship coordinate bytes owned."""

import struct

from ndspy.code import loadOverlayTable
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_location_v606 import relocate as center_fixture
from scripts.probe_button_prompt_native import call, machine

ROM = "out/all_routes_combined_v604_candidate.nds"


def terrain_queries(arm, points):
    rom = NdsImage.open(ROM)
    clean = NdsImage.open("work/clean.nds")
    assert rom.read_file("/__arm9__.bin") == arm
    source = rom.read_file("/data/WORLDMAP.DK4")
    assert source == clean.read_file("/data/WORLDMAP.DK4")
    for lo, hi in ((0x69B5C, 0x69E00),):
        assert arm[lo:hi] == clean.read_file("/__arm9__.bin")[lo:hi]
    blocks = IlnkContainer.parse(source).blocks
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])[0]
    u = machine(arm)
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    pages = {}

    def page(px, py):
        if (px, py) not in pages:
            block = px // 5
            raw = blocks[block]
            u.mem_write(0x02460000, struct.pack("<2I", block, 0x02480000))
            u.mem_write(0x02480000, raw)
            u.mem_write(0x02460100, struct.pack("<2i", px, py))
            u.mem_write(0x024601F0, b"\xA5" * 2532)
            call(u, 0x01FFA10C - 0x02000000,
                 (0x02460000, 0x02460100, 0x02460200), instruction_limit=300000)
            assert bytes(u.mem_read(0x024601F0, 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(0x02460BC4, 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(0x02480000, len(raw))) == raw
            pages[px, py] = bytes(u.mem_read(0x02460200, 2500))
        return pages[px, py]

    results = []
    for point in points:
        tx, ty = (v // 16 for v in point)
        px, py = tx // 50, ty // 25
        for xx in (px, px - 1 if tx % 50 == 0 else px + 1):
            for yy in (py, py - 1 if ty % 25 == 0 else py + 1):
                slot = 0x02468010 + (xx & 1) * 2508 + (yy & 1) * 5016
                u.mem_write(slot, struct.pack("<2i", xx, yy) + page(xx, yy))
        u.mem_write(0x02460100, struct.pack("<2i", *point))
        call(u, 0x69B5C, (0x02468000, 0x02460100))
        result = u.reg_read(UC_ARM_REG_R0)
        results.append({"map_point": list(point), "native_collision_result": result,
                        "collision_free": result == 0})
    return {"WORLDMAP_sha256": sha(source), "native_decoder": 0x01FFA10C,
            "native_predicate": 0x02069B5C, "queries": results,
            "loaded_cache_is_explicit_replay_contract": True,
            "page_hashes": {f"{x},{y}": sha(v) for (x, y), v in pages.items()}}


def relocate(arm, raw, village):
    if village != 0:
        raise ValueError("V607 only binds the source-checked Inuvik water point")
    _, proof = center_fixture(arm, raw, village)
    center = [v + 16 for v in proof["village_point"]]
    assert center == [4896, 2320]
    water = [4874, 2320]
    terrain = terrain_queries(arm, (center, water))
    assert not terrain["queries"][0]["collision_free"]
    assert terrain["queries"][1]["collision_free"]
    assert sum((a - b) ** 2 for a, b in zip(center, water, strict=True)) < 32 ** 2
    after = bytearray(raw)
    offset = proof["active_ship"] - 0x02000000 + 16
    target = [v * 128 for v in water]
    struct.pack_into("<2i", after, offset, *target)
    assert raw[:offset] == after[:offset] and raw[offset + 8:] == after[offset + 8:]
    proof.update({"terrain_proof": terrain, "expected_selector_point_after_original_update": water,
                  "after_ship_fixed_point": target, "village_center_is_collision_free": False,
                  "changes": [{"address": 0x02000000 + i, "before": raw[i], "after": after[i]}
                              for i in range(offset, offset + 8) if raw[i] != after[i]],
                  "after_RAM_sha256": sha(after)})
    return bytes(after), proof
