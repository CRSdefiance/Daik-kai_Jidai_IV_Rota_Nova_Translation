"""Verify every real SLACK viewer slot; do not infer raw-comic display usage."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.research_online_loader_v190 import resource_call

ROOT = Path("work/analysis/slack_consumers_v209")
ROM = Path("out/all_routes_combined_v205_candidate.nds")
VIEW = 0x02470020
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == "88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0"
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    arm, old = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    ranges = [(0x4704C, 0x47184), (0xD3D30, 0xD42AC), (0xD6524, 0xD6C90), (0x115EA8, 0x115EFC)]
    assert all(arm[lo:hi] == old[lo:hi] for lo, hi in ranges)
    u = machine(arm)
    registration = resource_call(u, 0x10E190, ())
    manager = struct.unpack_from("<I", arm, 0x5D24)[0]
    call(u, 0xD6C0C, (manager,))
    handles, events, raw_buffer_reads = {}, [], []

    def bridge(uc, address, size, _):
        if address == 0x020E5650:
            raise ValueError("Native loader assertion")
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 128)).split(b"\0")[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            assert path.startswith("/_pxl/slackimg") and obj not in handles
            data = rom.read_file(path)
            handles[obj] = [path, data, 0]
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(data)))
            events.append({"operation": "open", "path": path, "sha256": sha(data)})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(state[1])
            state[2] = offset
            result = 1
        elif address == READ:
            state = handles[obj]
            target, size = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert state[2] + size <= len(state[1])
            uc.mem_write(target, state[1][state[2]:state[2] + size])
            state[2] += size
            events.append({"operation": "read", "path": state[0], "bytes": size})
            result = size
        else:
            events.append({"operation": "close", "path": handles.pop(obj)[0]})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def observe(uc, access, address, size, value, _):
        if address < 0x02233040 + 0x20000 and address + size > 0x02233040:
            raw_buffer_reads.append([uc.reg_read(UC_ARM_REG_PC), address, size])

    h1 = u.hook_add(UC_HOOK_CODE, bridge)
    h2 = u.hook_add(UC_HOOK_MEM_READ, observe)
    slots = []
    try:
        for index in range(21):
            owner = struct.unpack("<I", u.mem_read(0x02115EA8 + index * 4, 4))[0]
            fields = struct.unpack("<5I", u.mem_read(owner, 20))
            assert fields[0] == 0x02160538
            name = bytes(u.mem_read(fields[3], 96)).split(b"\0")[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            expected = index if index <= 12 or index == 20 else 12
            assert path == f"/_pxl/slackimg{expected:02d}.pxl"
            data = rom.read_file(path)
            pxl = PxlImage.from_bytes(data)
            u.mem_write(VIEW - 16, b"\xa5" * 80)
            u.mem_write(VIEW, bytes(48))
            call(u, 0xD3D80, (VIEW,))
            start = len(events)
            trace = resource_call(u, 0x470B4, (index, VIEW))
            view = struct.unpack("<12I", u.mem_read(VIEW, 48))
            assert view[3] == owner and view[10:12] == (pxl.width, pxl.height)
            resource_call(u, 0xD4170, (VIEW,))
            pointer = u.reg_read(UC_ARM_REG_R0)
            assert bytes(u.mem_read(pointer, len(data))) == data
            assert bytes(u.mem_read(VIEW - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(VIEW + 48, 16)) == b"\xa5" * 16
            assert not handles and not raw_buffer_reads
            assert 0x0204716C in trace and 0x020D4018 in trace
            slots.append({"slot": index, "owner": owner, "actual_path": path,
                          "source_sha256": sha(data), "native_view": list(view),
                          "native_extent": [pxl.width, pxl.height], "complete_PXL_header_palette_pixels_exact": True,
                          "native_constructor_virtual_copy_and_return_verified": True,
                          "raw_archive_buffer_reads_in_helper_cache_path": 0, "events": events[start:]})
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    targets = (0x0204704C, 0x020470B4)
    direct_calls, pointers, thumb_calls = [], [], []
    units = [(f"main-section-{n}", section.ramAddress, bytes(section.data))
             for n, section in enumerate(MainCodeFile(arm, 0x02000000).sections)]
    overlays = loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid])
    originals = loadOverlayTable(clean.rom.arm9OverlayTable, lambda oid, fid: clean.rom.files[fid])
    assert rom.rom.arm9OverlayTable == clean.rom.arm9OverlayTable
    for index, overlay in overlays.items():
        assert overlay.data == originals[index].data
        units.append((f"overlay-{index}", overlay.ramAddress, bytes(overlay.data)))
    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for label, base, data in units:
        for offset in range(0, len(data) - 3, 4):
            word = struct.unpack_from("<I", data, offset)[0]
            address = base + offset
            if word in targets:
                pointers.append({"address": address, "target": word})
            if word & 0x0F000000 != 0x0B000000:
                continue
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 0x1000000
            target = address + 8 + delta * 4
            if target in targets:
                direct_calls.append({"address": address, "target": target})
        for offset in range(0, len(data) - 3, 2):
            first, second = struct.unpack_from("<2H", data, offset)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800):
                continue
            for instruction in thumb.disasm(data[offset:offset + 4], base + offset, count=1):
                if instruction.mnemonic not in ("bl", "blx") or not instruction.op_str.startswith("#0x"):
                    continue
                target = int(instruction.op_str[1:], 16)
                if target in targets:
                    thumb_calls.append({"unit": label, "address": instruction.address, "target": target})
    assert sorted((r["address"], r["target"]) for r in direct_calls) == [
        (0x02028F34, 0x020470B4), (0x020640EC, 0x020470B4), (0x0209EDE8, 0x0204704C)]
    assert not pointers
    assert not thumb_calls
    report = {"format": "dk4-slack-native-viewer-slot-proof-v1", "ROM_sha256": sha(ROM.read_bytes()),
              "registry_distinct_instructions": len(registration), "slots": slots,
              "alias_slots_13_to_19": list(range(13, 20)), "alias_resource": "/_pxl/slackimg12.pxl",
              "all21_complete_native_viewer_and_cache_cases": True,
              "source_legacy_raw_comics_thumbnail_portrait_images_not_selected_by_this_helper": True,
              "direct_ARM_BL_call_sites_in_all_main_code_sections": direct_calls,
              "literal_function_pointer_references_in_scanned_sections": pointers,
              "direct_Thumb_calls_to_helpers": thumb_calls,
              "scanned_code_units": [{"unit": label, "base": base, "bytes": len(data), "sha256": sha(data)}
                                     for label, base, data in units],
              "ARM9_overlay_table_bytes": len(rom.rom.arm9OverlayTable),
              "known_archive_reader_caller": "0209EDE8 selects blocks 14..17 for captain creation; see V202 proof.",
              "static_scan_limit": "Aligned ARM BL, direct Thumb BL/BLX and literal pointers in all MainCodeFile sections and every declared ARM9 overlay. Generated filenames and computed/indirect branches are not ruled out; absence of direct callers is not global unused-data proof.",
              "SDK_file_IO_bridge_only": True, "normal_UI_GPU_and_other_raw_consumers_not_proved": True,
              "all14_unique_loose_source_art_review": "pending", "unresolved_ILNK_count_unchanged": 11,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_viewer_slot_proof.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_native_viewer_cases": len(slots), "raw_slot_aliases": 7,
                      "direct_helper_callers": len(direct_calls), "raw_buffer_reads": len(raw_buffer_reads)}))


if __name__ == "__main__":
    main()
