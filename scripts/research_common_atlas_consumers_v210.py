"""Execute common portrait/item readers and trade origins on real native atlases."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_SP,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.research_online_loader_v190 import resource_call

ROOT = Path("work/analysis/common_atlas_consumers_v210")
ROM = Path("out/all_routes_combined_v205_candidate.nds")
BUFFER, VIEW = 0x02233040, 0x02470020
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == "88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0"
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    arm, original = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    ranges = [(0x47774, 0x477B8), (0x47864, 0x479B0), (0x47A28, 0x47AE0), (0xD3D30, 0xD42AC)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    files = {p: rom.read_file(p) for p in ("/GRP/CMMNIMG.000", "/_pxl/item.pxl", "/_pxl/itemtrade.pxl",
                                        "/_pxl/item16.pxl", "/_pxl/itemtrade16.pxl")}
    assert all(data == clean.read_file(p) for p, data in files.items())
    portrait = files["/GRP/CMMNIMG.000"]
    item, trade = PxlImage.from_bytes(files["/_pxl/item.pxl"]), PxlImage.from_bytes(files["/_pxl/itemtrade.pxl"])
    assert len(portrait) == 512 + 178 * 56 * 64
    assert (item.width, item.height, item.bits_per_pixel, item.pixels_offset) == (32, 6976, 8, 532)
    assert (trade.width, trade.height, trade.bits_per_pixel) == (24, 2976, 8)
    u = machine(arm)
    resource_call(u, 0x10E190, ())
    manager = struct.unpack_from("<I", arm, 0x5D24)[0]
    call(u, 0xD6C0C, (manager,))
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address == 0x020E5650:
            raise ValueError("Native assertion reached")
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 128)).split(b"\0")[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            assert path in files and obj not in handles
            data = files[path]
            handles[obj] = [path, data, 0]
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(data)))
            events.append({"operation": "open", "path": path})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(state[1])
            state[2] = offset
            events.append({"operation": "seek", "path": state[0], "offset": offset})
            result = 1
        elif address == READ:
            state = handles[obj]
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            start = state[2]
            assert start + count <= len(state[1])
            uc.mem_write(target, state[1][start:start + count])
            state[2] += count
            events.append({"operation": "read", "path": state[0], "offset": start, "bytes": count})
            result = count
        else:
            events.append({"operation": "close", "path": handles.pop(obj)[0]})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    portraits, items, trades, compact = [], [], [], []
    try:
        for index in range(178):
            u.mem_write(BUFFER - 16, b"\xa5" * (3584 + 32))
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_R4, index)
            start = len(events)
            # Actual parent read fragment; later portrait-header copy/display is not executed.
            u.emu_start(0x02047A28, 0x02047A60, count=100000)
            assert u.reg_read(UC_ARM_REG_PC) == 0x02047A60 and u.reg_read(UC_ARM_REG_SP) == STACK
            assert u.reg_read(UC_ARM_REG_R4) == index and not handles
            loaded = bytes(u.mem_read(BUFFER, 3584))
            assert loaded == portrait[512 + index * 3584:512 + (index + 1) * 3584]
            assert bytes(u.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(BUFFER + 3584, 16)) == b"\xa5" * 16
            portraits.append({"index": index, "offset": 512 + index * 3584, "bytes": 3584,
                              "indices_sha256": sha(loaded), "native_read_and_guards_exact": True,
                              "events": events[start:]})
        for index in range(218):
            u.mem_write(BUFFER - 16, b"\xa5" * (1024 + 32))
            start = len(events)
            resource_call(u, 0x47864, (0, index))
            loaded = bytes(u.mem_read(BUFFER, 1024))
            assert loaded == bytes(item.indices[index * 1024:(index + 1) * 1024])
            assert bytes(u.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(BUFFER + 1024, 16)) == b"\xa5" * 16
            assert not handles
            items.append({"index": index, "offset": 532 + index * 1024, "bytes": 1024,
                          "indices_sha256": sha(loaded), "complete_native_read_and_return_exact": True,
                          "events": events[start:]})
        owner = struct.unpack_from("<I", arm, 0x47974)[0]
        for index in range(124):
            u.mem_write(VIEW - 16, b"\xa5" * 80)
            u.mem_write(VIEW, bytes(48))
            call(u, 0xD3D80, (VIEW,))
            resource_call(u, 0x47940, (0, index, VIEW))
            fields = struct.unpack("<12I", u.mem_read(VIEW, 48))
            assert fields[3] == owner and fields[7:9] == (0, index * 24)
            resource_call(u, 0xD4170, (VIEW,))
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(files["/_pxl/itemtrade.pxl"]))) == files["/_pxl/itemtrade.pxl"]
            assert bytes(u.mem_read(VIEW - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(VIEW + 48, 16)) == b"\xa5" * 16
            assert 0 <= index * 24 < (index + 1) * 24 <= trade.height and not handles
            trades.append({"index": index, "actual_owner": owner, "source_origin": [0, index * 24],
                           "native_view": list(fields), "complete_atlas_cache_palette_pixels_exact": True,
                           "24x24_source_cell_within_atlas": True,
                           "caller_clip_extent_and_GPU_not_verified": True})
        for path, count, routine, owner in (("/_pxl/item16.pxl", 218, 0x47774, 0x02313BC8),
                                           ("/_pxl/itemtrade16.pxl", 124, 0x478D0, 0x02313BB4)):
            image = PxlImage.from_bytes(files[path])
            assert (image.width, image.height, image.bits_per_pixel) == (16, count * 16, 8)
            for index in range(count):
                u.mem_write(VIEW - 16, b"\xa5" * 80)
                u.mem_write(VIEW, bytes(48))
                call(u, 0xD3D80, (VIEW,))
                resource_call(u, routine, (0, index, VIEW))
                fields = struct.unpack("<12I", u.mem_read(VIEW, 48))
                assert fields[3] == owner and fields[7:9] == (0, index * 16)
                assert fields[10:12] == (16, 16)
                resource_call(u, 0xD4170, (VIEW,))
                pointer = u.reg_read(UC_ARM_REG_R0)
                assert bytes(u.mem_read(pointer, len(files[path]))) == files[path]
                assert bytes(u.mem_read(VIEW - 16, 16)) == b"\xa5" * 16
                assert bytes(u.mem_read(VIEW + 48, 16)) == b"\xa5" * 16
                assert (index + 1) * 16 <= image.height and not handles
                compact.append({"path": path, "index": index, "native_routine": routine,
                                "native_owner": owner, "source_origin": [0, index * 16],
                                "native_extent": [16, 16], "view": list(fields),
                                "complete_native_atlas_palette_pixels_and_crop_bounds_exact": True,
                                "physical_GUI_GPU_not_verified_by_constructor": True})
    finally:
        u.hook_del(hook)
    units = [(f"main-{n}", s.ramAddress, bytes(s.data))
             for n, s in enumerate(MainCodeFile(arm, 0x02000000).sections)]
    for index, overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid]).items():
        units.append((f"overlay-{index}", overlay.ramAddress, bytes(overlay.data)))
    literals = []
    for label, base, data in units:
        for name in (b"CMMNIMG.DK4", b"CMMNIMG.000"):
            start = 0
            while (offset := data.lower().find(name.lower(), start)) >= 0:
                literals.append({"unit": label, "address": base + offset, "literal": name.decode("ascii")})
                start = offset + len(name)
    assert not any(r["literal"] == "CMMNIMG.DK4" for r in literals)
    report = {"format": "dk4-common-native-atlas-consumer-proof-v1", "ROM_sha256": sha(ROM.read_bytes()),
              "file_hashes": {p: sha(data) for p, data in files.items()}, "portrait_reads": portraits,
              "complete_item_reads": items, "trade_origin_and_cache_cases": trades,
              "compact_native_crop_cases": compact,
              "native_checks": len(portraits) + len(items) + len(trades) + len(compact), "source_atlases_preserved": True,
              "common_filename_literals_in_main_and_all_ARM9_overlays": literals,
              "legacy_CMMNIMG_DK4_not_equated_to_native_atlases": True,
              "legacy_four_blocks_consumer_mapping_still_open": True,
              "SDK_filesystem_bridge_only": True, "all_handles_closed": not handles,
              "scope": "178 actual portrait read fragments with supplied preceding index/stack context; 218 complete native item reader calls; 124 original large-trade source-origin constructors and full native cache loads; 342 complete compact source-origin/crop constructors and native cache loads. Portrait subsequent header copies and large-trade caller clip extents/GPU are not inferred. Fixed-name absence is not global unused-data proof.",
              "native_GUI_all_cell_display_not_verified": True, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"portrait_native_reads": len(portraits), "item_native_reads": len(items),
                      "trade_native_origins": len(trades), "compact_native_crops": len(compact),
                      "complete_cases": report["native_checks"]}))


if __name__ == "__main__":
    main()
