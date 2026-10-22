"""Execute all fixed style-wrapper paths and record every original source tile."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine

ROOT = Path("work/analysis/frame_callers_v584")
HEADER, CONTEXT, DESTINATION = 0x02420000, 0x02460000, 0x02460100
CELLS = [("Pick Cargo", (208, 32, 256, 40)), ("Pick Ship", (208, 40, 240, 48)),
         ("Done", (240, 40, 256, 48)), ("Rank", (184, 48, 208, 56)), ("Cancel", (208, 48, 256, 56))]


def main():
    rom = NdsImage.open("out/all_routes_combined_v581_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    u, original = (machine(r.read_file("/__arm9__.bin")) for r in (rom, clean))
    assert bytes(u.mem_read(0x020D0A40, 0xD13A4 - 0xD0A40)) == bytes(original.mem_read(0x020D0A40, 0xD13A4 - 0xD0A40))
    source = rom.read_file("/_pxl/__frame.pxl")
    u.mem_write(HEADER, source)
    u.mem_write(CONTEXT, bytes(64))
    u.mem_write(CONTEXT + 0x20, struct.pack("<4I", 20, 30, 180, 110))
    u.mem_write(DESTINATION, struct.pack("<4I", 20, 30, 180, 110))
    draws = []

    def contracts(uc, address, _size, _data):
        if address == 0x020D6558:
            assert uc.reg_read(UC_ARM_REG_R0) == 0x02313F60
            uc.reg_write(UC_ARM_REG_R0, HEADER)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address in (0x01FFAE70, 0x01FF92D8):
            assert uc.reg_read(UC_ARM_REG_R0) == 0 and uc.reg_read(UC_ARM_REG_R1) == HEADER
            pointer = uc.reg_read(UC_ARM_REG_R3)
            if address == 0x01FFAE70:
                tile = struct.unpack("<4I", uc.mem_read(pointer, 16))
            else:
                point = struct.unpack("<2I", uc.mem_read(pointer, 8))
                size_pointer = int.from_bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 4), "little")
                tile = point + struct.unpack("<2I", uc.mem_read(size_pointer, 8))
            x, y, width, height = tile
            assert width <= 256 and height <= 256 and x < 256 and y < 256 and x + width <= 256 and y + height <= 256, tile
            effective_width, effective_height = (max(1, width), max(1, height)) if address == 0x01FFAE70 else (width, height)
            intersections = [name for name, (l, t, r, b) in CELLS
                             if x < r and y < b and x + effective_width > l and y + effective_height > t]
            draws.append({"callee": address, "return_address": uc.reg_read(UC_ARM_REG_LR),
                          "palette": uc.reg_read(UC_ARM_REG_R2), "source_tile_XYWH": list(tile),
                          "effective_sample_dimensions": [effective_width, effective_height],
                          "intersecting_caption_cells": intersections})
            uc.reg_write(UC_ARM_REG_R0, 0)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, contracts)
    census = json.loads((ROOT / "literal_style_callers.json").read_text(encoding="utf-8"))
    rows = []
    try:
        for row in census["direct_style_call_sites"]:
            assert row["valid_original_atlas_tile"]
            pointer, target = row["style_pointer"], row["target"]
            count = 9 if row["kind"] in ("frame_style", "default_frame", "direct_tiled_border") else 3 if row["kind"] == "strip_style" else 1
            start = pointer if target == 0x020D0AC4 else pointer + 4
            data = bytes(u.mem_read(start, count * 16))
            assert data == bytes(original.mem_read(start, count * 16))
            tiles = [struct.unpack_from("<4I", data, offset) for offset in range(0, len(data), 16)]
            declared = {tile for tile in tiles if tile[2] and tile[3]}
            empty = [tile for tile in tiles if not tile[2] or not tile[3]]
            selections = []
            for center in (0, 1):
                draws.clear()
                u.mem_write(STACK, struct.pack("<I", center))
                if target == 0x020D0AC4:
                    palette = int.from_bytes(u.mem_read(pointer - 4, 4), "little")
                    args = palette, pointer, DESTINATION, 0
                else:
                    args = CONTEXT, 0, pointer, DESTINATION
                call(u, target - BASE, args)
                assert draws and not any(d["intersecting_caption_cells"] for d in draws)
                assert {tuple(d["source_tile_XYWH"]) for d in draws} <= set(tiles)
                selections.append({"center_flag": center, "native_source_tile_calls": list(draws)})
            observed = {tuple(d["source_tile_XYWH"]) for selection in selections for d in selection["native_source_tile_calls"]}
            assert declared <= observed, (hex(row["call"]), observed, declared)
            rows.append({"original_caller": row["call"], "wrapper": target, "style_pointer": pointer,
                         "complete_style_bytes_exact_clean": True, "declared_tile_count": count,
                         "all_declared_nonempty_source_tiles_exercised": True,
                         "zero_dimension_records": [{"descriptor": tile, "observed": tile in observed} for tile in empty],
                         "native_cases": selections})
    finally:
        u.hook_del(hook)
    result = {"candidate_sha256": sha(rom.source.read_bytes()), "source_atlas_sha256": sha(source),
              "native_style_cases": rows, "all84_literal_style_caller_paths_checked": len(rows) == 84,
              "all_selected_tiles_outside_five_caption_cells": True,
              "complete_original_helper_code_and_style_arrays_exact_clean": True,
              "resource_getter_bridged_to_exact_production_header_and_pixel_calls_argument_traced": True,
              "actual_pixel_contracts_separately_verified": "native_blitter_contract_proof.json",
              "original_parent_UI_and_all_indirect_aliases_not_proven": True,
              "no_ROM_changes": True, "full_goal_complete": False}
    (ROOT / "native_all_style_tiles_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print({"original_style_callers": len(rows), "native_wrapper_cases": len(rows) * 2,
           "native_source_tile_calls": sum(len(c["native_source_tile_calls"]) for r in rows for c in r["native_cases"]),
           "miniature_caption_intersections": 0})


if __name__ == "__main__":
    main()
