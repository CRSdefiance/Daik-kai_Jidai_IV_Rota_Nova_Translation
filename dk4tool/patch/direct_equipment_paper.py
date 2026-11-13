"""Bounded native framebuffer paper tiling for long equipment tooltips."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.sailing_no_target import mov_immediate as arm_mov
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "779b9230135163e483a7ed9c7f9fb056a76dad0fc739596463161c42bb80c821"
ROOT = Path("work/analysis/direct_equipment_v270")
FRAMEBUFFER, ORIGIN_X, ORIGIN_Y = 0x022E1794, 0x022E1770, 0x022E176C


def paint(address, state, old, tile, period):
    if not 4 <= period <= 120:
        raise ValueError("Paper period exceeds the source-locked row size")
    a = Assembly()
    a.load(12, "state", state); a.emit(0xE59CC000); a.emit(0xE150000C); a.branch("original", 1)
    a.emit(0xE590C028); a.emit(0xE5901020); a.emit(0xE04CC001)
    for width in (34, 40, 88):
        a.emit(0xE35C0000 | width); a.branch("original", 0)
    a.emit(0xE35C000A); a.branch("original", 3)
    a.emit(0xE35C00F4); a.branch("original", 8)
    a.emit(0xE92D4FFF); a.emit(0xE24DD004)  # all input registers; aligned56-byte frame
    a.emit(0xE1A0400C)
    a.emit(0xE590C02C); a.emit(0xE5901024); a.emit(0xE04CC001)
    a.emit(0xE35C0010); a.branch("restore_original", 1)
    a.emit(0xE590C018); a.emit(0xE35C0001); a.branch("restore_original", 8)
    a.load(7, "framebuffer", FRAMEBUFFER)
    a.emit(0x02877000 | (arm_mov(0, 0x18000) & 0xFFF))
    a.load(12, "origin_x", ORIGIN_X); a.emit(0xE59CC000)
    a.emit(0xE5902020); a.emit(0xE042200C)
    a.emit(0xE3520000); a.branch("restore_original", 11)
    a.emit(0xE082C004); a.emit(0xE35C0C01); a.branch("restore_original", 8)  #256
    a.load(12, "origin_y", ORIGIN_Y); a.emit(0xE59CC000)
    a.emit(0xE5903024); a.emit(0xE043300C)
    a.emit(0xE3530000); a.branch("restore_original", 11)
    a.emit(0xE283C010); a.emit(0xE35C00C0); a.branch("restore_original", 8)
    a.emit(0xE0877083); a.emit(0xE0877082)  # temporary; patched below with proper shifts
    a.words[-2] = 0xE0877483  # add r7,r7,r3,lsl9
    a.words[-1] = 0xE0877082  # add r7,r7,r2,lsl1
    a.load(6, "tile", tile); a.emit(0xE3A08010)
    a.mark("row")
    a.emit(0xE1A05007)
    a.emit(0xE1D600B0); a.emit(0xE1C500B0)
    a.emit(0xE1D600B2); a.emit(0xE1C500B2); a.emit(0xE2855004)
    a.emit(0xE2869004); a.emit(0xE286A000 | (period + 2) * 2)
    a.emit(0xE244B004)
    a.mark("interior")
    a.emit(0xE1D900B0); a.emit(0xE1C500B0)
    a.emit(0xE2899002); a.emit(0xE2855002)
    a.emit(0xE159000A); a.emit(0x02869004)
    a.emit(0xE25BB001); a.branch("interior", 1)
    a.emit(0xE1DA00B0); a.emit(0xE1C500B0)
    a.emit(0xE1DA00B2); a.emit(0xE1C500B2)
    a.emit(0xE2866000 | (period + 4) * 2)
    a.emit(0xE2877000 | (arm_mov(0, 512) & 0xFFF))
    a.emit(0xE2588001); a.branch("row", 1)
    a.emit(0xE28DD004); a.emit(0xE8BD8FFF)
    a.mark("restore_original"); a.emit(0xE28DD004); a.emit(0xE8BD4FFF)
    a.mark("original"); a.emit(tail(address + len(a.words) * 4, old))
    return a.finish()


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V267 ARM9 required")
    data = json.loads((ROOT / "paper_data_plan.json").read_text(encoding="utf-8"))
    tile = (ROOT / "paper_tile.bin").read_bytes()
    if sha(tile) != data["tile_sha256"] or len(tile) != (data["period"] + 4) * 16 * 2:
        raise ValueError("Source paper tile differs")
    prior = json.loads(Path("work/analysis/plaque_coverage_v252/runtime_plan.json").read_text(encoding="utf-8"))
    old, state = prior["dispatcher_entry"], prior["state_pointer"]
    code = MainCodeFile(source, BASE); before = [bytes(s.data) for s in code.sections]
    cache_plan(source); packed = bytearray(before[3][:-48]); preserved = len(packed)
    tile_pointer = POOL + len(packed); packed.extend(tile)
    entry = POOL + len(packed); packed.extend(paint(entry, state, old, tile_pointer, data["period"]))
    changes = []

    def replace(offset, expected, value):
        if struct.unpack_from("<I", source, offset)[0] != expected:
            raise ValueError("Direct paper caller differs")
        struct.pack_into("<I", code.sections[0].data, offset, value)
        changes.append({"offset": offset, "before": expected, "after": value})

    replace(0x6BDC, branch_link(BASE + 0x6BDC, old), branch_link(BASE + 0x6BDC, entry))
    packed.extend(bytes((-len(packed)) % 32)); size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Direct paper exceeds owned arena")
    cache_entry, copy = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    replace(0x8E4, struct.unpack_from("<I", source, 0x8E4)[0], branch_link(BASE + 0x8E4, cache_entry))
    replace(0xE45DC, struct.unpack_from("<I", source, 0xE45DC)[0], POOL + size)
    saved = bytes(code.save()); parsed = MainCodeFile(saved, BASE); restored = bytearray(parsed.sections[0].data)
    for row in changes:
        o = row["offset"]; restored[o:o + 4] = before[0][o:o + 4]
    o = code.codeSettingsOffs; restored[o:o + 12] = before[0][o:o + 12]
    assert bytes(restored) == before[0] and all(bytes(parsed.sections[n].data) == before[n] for n in (1, 2))
    assert bytes(parsed.sections[3].data[:preserved]) == before[3][:-48]
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved), "entry": entry,
                   "old_dispatcher": old, "state_pointer": state, "tile_pointer": tile_pointer,
                   "period": data["period"], "changes": changes, "payload_bytes": size, "cache": cache_plan(saved),
                   "native_framebuffer_addresses_are_existing_source_fields": True,
                   "out_of_bounds_screen_or_rectangle_delegates_to_original": True}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-direct-equipment-paper-release-v1":
        raise ValueError("Unknown direct paper release")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Direct paper dependency differs")
    saved, plan = transform(source)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Direct paper target differs")
    plan["changed_records"] = ["DK4_DIRECT_VARIABLE_EQUIPMENT_PAPER_V1"]
    return saved, plan
