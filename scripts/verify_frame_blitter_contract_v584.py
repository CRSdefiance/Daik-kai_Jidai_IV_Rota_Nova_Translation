"""Original tiled 4-bpp blitter: source XYWH and destination LTRB contracts."""

import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.direct_equipment_paper import FRAMEBUFFER, ORIGIN_X, ORIGIN_Y
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine

ROOT = Path("work/analysis/frame_callers_v584")
HEADER, TILE, DESTINATION = 0x02420000, 0x02450000, 0x02450100


def main():
    rom = NdsImage.open("out/all_routes_combined_v581_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    overlays = [loadOverlayTable(r.rom.arm9OverlayTable, lambda _id, file_id, r=r: r.rom.files[file_id])[0]
                for r in (rom, clean)]
    assert overlays[0].ramAddress == overlays[1].ramAddress == 0x01FFA000
    assert bytes(overlays[0].data) == bytes(overlays[1].data)
    arm = rom.read_file("/__arm9__.bin")
    source = rom.read_file("/_pxl/__frame.pxl")
    atlas = PxlImage.from_bytes(source)
    assert atlas.width == atlas.height == 256
    u = machine(arm)
    u.mem_write(overlays[0].ramAddress, bytes(overlays[0].data))
    u.mem_write(HEADER - 16, b"\xA5" * (len(source) + 32))
    u.mem_write(HEADER, source)
    cases = []
    captions = [("Pick Cargo", (208, 32, 48, 8)), ("Pick Ship", (208, 40, 32, 8)),
                ("Done", (240, 40, 16, 8)), ("Rank", (184, 48, 24, 8)), ("Cancel", (208, 48, 48, 8))]
    selections = []
    for label, tile in captions:
        for bank in (0, 9):
            selections.append((label, tile, (20, 30, 20 + tile[2], 30 + tile[3]), bank, 0, (0, 0)))
    selections += [("decorative tile", (16, 104, 8, 16), (20, 30, 76, 62), 39, screen, (0, 0))
                   for screen in (0, 1)]
    selections += [("left clipped tile", (16, 104, 8, 16), (-5, 30, 51, 46), 39, 0, (0, 0)),
                   ("top clipped tile", (16, 104, 8, 16), (20, -3, 76, 29), 39, 1, (0, 0)),
                   ("right and bottom clipped tile", (16, 104, 8, 16), (244, 184, 276, 216), 39, 0, (0, 0)),
                   ("viewport origin", (16, 104, 8, 16), (27, 41, 83, 73), 39, 1, (7, 11))]
    selections += [("zero-dimension solid fill", (0, 0, 0, 0), (20, 30, 76, 62), bank, 0, (0, 0))
                   for bank in (0, 9)]
    seed = bytes([0xA5]) * 0x30000
    for label, tile, destination, bank, screen, origin in selections:
        u.mem_write(FRAMEBUFFER - 16, b"\xA5" * (len(seed) + 32))
        u.mem_write(ORIGIN_X, struct.pack("<i", origin[0]))
        u.mem_write(ORIGIN_Y, struct.pack("<i", origin[1]))
        source_descriptor = struct.pack("<4i", *tile)
        destination_descriptor = struct.pack("<4i", *destination)
        u.mem_write(TILE, source_descriptor)
        u.mem_write(DESTINATION, destination_descriptor)
        u.mem_write(STACK, struct.pack("<I", DESTINATION))
        executed = call(u, 0x01FFAE70 - BASE, (screen, HEADER, bank, TILE), instruction_limit=1000000)
        assert {0x01FFAE70, 0x01FFADA0} <= executed
        expected = bytearray(seed)
        palette = struct.unpack_from("<16H", source, 20 + bank * 32)
        left, top, right, bottom = destination
        left, right = left - origin[0], right - origin[0]
        top, bottom = top - origin[1], bottom - origin[1]
        clipped_left, clipped_top = max(0, left), max(0, top)
        writes = 0
        for y in range(clipped_top, min(192, bottom)):
            for x in range(clipped_left, min(256, right)):
                # This original tiled-frame routine restarts its tile phase at
                # the clipped destination edge; it is not a general sprite crop.
                sx = tile[0] + (x - clipped_left) % max(1, tile[2])
                sy = tile[1] + (y - clipped_top) % max(1, tile[3])
                value = palette[atlas.indices[sy * 256 + sx]]
                if value & 0x8000:
                    struct.pack_into("<H", expected, screen * 0x18000 + (y * 256 + x) * 2, value)
                    writes += 1
        assert bytes(u.mem_read(FRAMEBUFFER, len(seed))) == expected, label
        assert bytes(u.mem_read(FRAMEBUFFER - 16, 16)) == b"\xA5" * 16
        assert bytes(u.mem_read(FRAMEBUFFER + len(seed), 16)) == b"\xA5" * 16
        assert bytes(u.mem_read(HEADER, len(source))) == source
        assert bytes(u.mem_read(HEADER - 16, 16)) == b"\xA5" * 16
        assert bytes(u.mem_read(HEADER + len(source), 16)) == b"\xA5" * 16
        assert bytes(u.mem_read(TILE, 16)) == source_descriptor
        assert bytes(u.mem_read(DESTINATION, 16)) == destination_descriptor
        cases.append({"label": label, "source_tile_XYWH": tile, "destination_LTRB": destination,
                      "palette": bank, "screen": screen, "viewport_origin": origin,
                      "opaque_source_pixel_writes": writes, "whole_framebuffer_bytes_exact": len(seed),
                      "source_descriptors_resource_guards_and_saved_register_ABI_exact": True})
    corner_cases = []
    for bank in (0, 9):
        for screen in (0, 1):
            u.mem_write(FRAMEBUFFER - 16, b"\xA5" * (len(seed) + 32))
            u.mem_write(ORIGIN_X, bytes(4))
            u.mem_write(ORIGIN_Y, bytes(4))
            u.mem_write(TILE, struct.pack("<4I", 208, 32, 48, 8))
            u.mem_write(DESTINATION, struct.pack("<2I", 30, 40))
            u.mem_write(STACK, struct.pack("<2I", TILE + 8, DESTINATION))
            call(u, 0x01FF92D8 - BASE, (screen, HEADER, bank, TILE), instruction_limit=1000000)
            expected = bytearray(seed)
            palette = struct.unpack_from("<16H", source, 20 + bank * 32)
            for y in range(8):
                for x in range(48):
                    value = palette[atlas.indices[(32 + y) * 256 + 208 + x]]
                    if value & 0x8000:
                        struct.pack_into("<H", expected, screen * 0x18000 + ((40 + y) * 256 + 30 + x) * 2, value)
            assert bytes(u.mem_read(FRAMEBUFFER, len(seed))) == expected
            assert bytes(u.mem_read(FRAMEBUFFER - 16, 16)) == bytes(u.mem_read(FRAMEBUFFER + len(seed), 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(HEADER, len(source))) == source
            corner_cases.append({"blitter": 0x01FF92D8, "source_XY": [208, 32], "source_size": [48, 8],
                                 "destination_XY": [30, 40], "palette": bank, "screen": screen,
                                 "full_framebuffer_guards_and_saved_register_ABI_exact": True})
    result = {"candidate": str(rom.source), "candidate_sha256": sha(rom.source.read_bytes()),
              "source_atlas_sha256": sha(source), "overlay_sha256": sha(bytes(overlays[0].data)),
              "original_overlay_entirely_exact_clean": True,
              "blitter": 0x01FFAE70, "r0": "screen index", "r1": "PXL header",
              "r2": "palette bank", "r3": "source tile XYWH pointer",
              "stack_argument0": "destination LTRB pointer",
              "tile_repeats_to_fill_destination_and_restarts_at_clipped_edge": True,
              "zero_dimension_tiled_descriptor_repeats_one_source_pixel": True,
              "cases": cases, "controlled_source_binding_not_ordinary_caption_parent": True,
              "non_tiled_corner_cases": corner_cases,
              "non_tiled_blitter_r3_source_XY_stack0_size_stack4_destination_XY": True,
              "source_owner_filename_cache_and_GPU_not_proven_by_this_probe": True,
              "no_ROM_changes": True, "full_goal_complete": False}
    (ROOT / "native_blitter_contract_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{len(cases)} tiled and {len(corner_cases)} original corner-copy cases: source/destination contracts, palettes, guards and ABI pass.")


if __name__ == "__main__":
    main()
