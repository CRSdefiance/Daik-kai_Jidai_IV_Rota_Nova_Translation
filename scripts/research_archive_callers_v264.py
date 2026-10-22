"""Map every direct ILNK caller and execute its native filename selection.

Stops after each native archive open; this is not a complete parent/GPU test.
Only SDK file I/O is bridged. Caller registers and route selection are contracts.
"""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R6,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, call, machine

ROOT = Path("work/analysis/archive_callers_v264")
ROM = Path("out/all_routes_combined_v263_candidate.nds")
TARGETS = {BASE + n for n in (0xD2018, 0xD1EF0, 0xD1F50, 0x4704C)}
OPEN, READ, SEEK, CLOSE = (BASE + n for n in (0xDED50, 0xDEBDC, 0xDEB70, 0xDED08))
OBJECT, BUFFER = 0x02460000, 0x02480000


def census(rom, arm):
    units = [(f"main-{n}", s.ramAddress, bytes(s.data)) for n, s in enumerate(MainCodeFile(arm, BASE).sections)]
    for n, overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda oid, fid: rom.rom.files[fid]).items():
        units.append((f"overlay-{n}", overlay.ramAddress, bytes(overlay.data)))
    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    calls, pointers, thumb_calls = [], [], []
    for name, base, data in units:
        for offset in range(0, len(data) - 3, 4):
            value = struct.unpack_from("<I", data, offset)[0]
            address = base + offset
            if value in TARGETS:
                pointers.append({"unit": name, "address": address, "target": value})
            if value & 0x0F000000 == 0x0B000000:
                delta = value & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 0x1000000
                target = address + 8 + delta * 4
                if target in TARGETS:
                    calls.append({"unit": name, "address": address, "target": target})
        for offset in range(0, len(data) - 3, 2):
            first, second = struct.unpack_from("<2H", data, offset)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800):
                continue
            for i in thumb.disasm(data[offset:offset + 4], base + offset, count=1):
                if i.mnemonic in ("bl", "blx") and i.op_str.startswith("#0x") and int(i.op_str[1:], 16) in TARGETS:
                    thumb_calls.append({"unit": name, "address": i.address, "target": int(i.op_str[1:], 16)})
    return {"units": [{"name": n, "base": b, "bytes": len(d), "sha256": sha(d)} for n, b, d in units],
            "aligned_ARM_BL_calls": calls, "literal_pointers": pointers, "Thumb_calls": thumb_calls}


def open_parent(rom, arm, start, end, args, route=None, mes=False):
    u = machine(arm)
    u.mem_write(OBJECT, bytes(0x100))
    u.mem_write(OBJECT + 4, struct.pack("<I", 0xFFFFFFFF))
    if route is not None:
        u.mem_write(0x02279668 + 0x48, struct.pack("<I", route))
    if mes:
        call(u, 0xD2100, (OBJECT,))
        u.reg_write(UC_ARM_REG_R8, OBJECT)
        u.reg_write(UC_ARM_REG_R6, 0)
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), args):
        u.reg_write(reg, value)
    handles, events, archive_objects = {}, [], []

    def bridge(uc, address, size, _):
        if address == BASE + 0xD2018:
            archive_objects.append(uc.reg_read(UC_ARM_REG_R0))
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 128)).split(b"\0")[0].decode("ascii")
            path = "/" + name.replace("\\", "/").lstrip("/")
            matches = [p for p in rom.path_map() if p.casefold() == path.casefold()]
            assert len(matches) == 1
            requested = path
            path = matches[0]
            raw = rom.read_file(path)
            handles[obj] = [path, raw, 0]
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(raw)))
            events.append({"operation": "open", "requested_filename": requested, "path": path,
                           "case_insensitive_SDK_bridge_resolution": True, "sha256": sha(raw), "bytes": len(raw)})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset, origin = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert origin == 0 and 0 <= offset <= len(state[1])
            state[2] = offset
            result = 1
        elif address == READ:
            state = handles[obj]
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            begin = state[2]
            assert begin + count <= len(state[1])
            uc.mem_write(target, state[1][begin:begin + count])
            state[2] += count
            events.append({"operation": "read", "offset": begin, "bytes": count})
            result = count
        else:
            events.append({"operation": "close", "path": handles.pop(obj)[0]})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    u.hook_add(UC_HOOK_CODE, bridge)
    u.emu_start(BASE + start, BASE + end, count=200000)
    assert u.reg_read(UC_ARM_REG_PC) == BASE + end
    assert len(archive_objects) == len(handles) == 1 and u.reg_read(UC_ARM_REG_R0) == 1
    obj = archive_objects[0]
    path, raw, _ = next(iter(handles.values()))
    container = IlnkContainer.parse(raw)
    block_count = struct.unpack("<I", u.mem_read(obj + 0x28, 4))[0]
    assert block_count == len(container.blocks)
    # Explicit harness cleanup after a deliberately interrupted parent.
    call(u, 0xD2004, (obj,))
    call(u, 0xD20E0, (obj,))
    assert not handles
    return {"parent_start": BASE + start, "stop_after_native_open": BASE + end,
            "supplied_arguments": list(args), "supplied_route": route,
            "actual_path": path, "native_block_count": block_count,
            "native_filename_open_and_directory_header_executed": True,
            "SDK_events": events, "interrupted_parent_cleaned_by_harness": True,
            "full_parent_block_read_or_display_not_claimed": True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    manifest = json.loads(ROM.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert manifest["candidate_sha256"] == sha(ROM.read_bytes())
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    arm, source = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    scan = census(rom, arm)
    opens = [r["address"] for r in scan["aligned_ARM_BL_calls"] if r["target"] == BASE + 0xD2018]
    assert opens == [BASE + n for n in (0x972C, 0x97A8, 0x24170, 0x47074, 0x53544, 0x6E59C, 0x7CE3C)]
    assert not scan["Thumb_calls"] and not scan["literal_pointers"]
    ranges = [(0x9710, 0x9808), (0x24134, 0x241CC), (0x4704C, 0x470B4),
              (0x53530, 0x535D4), (0x6E578, 0x6E5DC), (0x7CE1C, 0x7D070), (0xD1EE0, 0xD2128)]
    assert all(arm[a:b] == source[a:b] for a, b in ranges)
    cases = [(0x9710, 0x9730, (0,), None, False), (0x977C, 0x97AC, (1,), None, False)]
    cases += [(0x24134, 0x24174, (OBJECT, 0), n, False) for n in range(4)]
    cases += [(0x4704C, 0x47078, (14, BUFFER, 0, 14144), None, False),
              (0x53530, 0x53548, (), None, True), (0x6E578, 0x6E5A0, (OBJECT, 0), None, False),
              (0x7CE1C, 0x7CE40, (OBJECT, 0), None, False)]
    rows = [open_parent(rom, arm, *case) for case in cases]
    proof = {"format": "dk4-archive-caller-census-v264", "candidate": str(ROM), "candidate_sha256": sha(ROM.read_bytes()),
             "candidate_manifest_and_current_registry_hash_match": True,
             "scan": scan, "native_filename_selection_cases": rows,
             "all_seven_direct_archive_open_call_sites_classified": True,
             "no_additional_direct_raw_comic_archive_parent_found": True,
             "computed_generated_and_indirect_consumers_not_ruled_out": True,
             "no_global_unused_data_or_native_comic_display_claim": True,
             "all18_plaques_incomplete": True, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_cases": len(rows), "actual_paths": sorted({r['actual_path'] for r in rows}), "scan_calls": len(scan['aligned_ARM_BL_calls'])}))


if __name__ == "__main__":
    main()
