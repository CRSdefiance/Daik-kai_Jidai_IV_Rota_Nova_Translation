"""Original whole portrait loop, including metadata virtual calls and raw reads.

Captured parent/global state and a scratch stack are explicit replay contracts.
This is not the complete UI constructor or global unused-archive proof.
"""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.trace_frame_crop_arguments_v584 import branch

ROOT = Path("work/analysis/slack_caller_loop_v588")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/name_editor_v582")
RAW, SIZE = 0x02233040, 104 * 136
START, END, WRAPPER = 0x0209ED3C, 0x0209EE94, 0x0204704C
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def census(rom, arm):
    units = [(f"main{i}", s.ramAddress, bytes(s.data)) for i, s in enumerate(MainCodeFile(arm, BASE).sections)]
    units += [(f"overlay{i}", o.ramAddress, bytes(o.data)) for i, o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).items()]
    direct, pointers, thumb = [], [], []
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for name, base, data in units:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from("<I", data, at)[0]
            if branch(word, base + at) == WRAPPER:
                direct.append({"unit": name, "instruction": base + at,
                               "link": bool(word & 0x01000000), "condition": word >> 28})
        for at in range(len(data) - 3):
            value = struct.unpack_from("<I", data, at)[0]
            if value & ~1 == WRAPPER:
                pointers.append({"unit": name, "address": base + at, "value": value})
        for at in range(0, len(data) - 3, 2):
            first, second = struct.unpack_from("<2H", data, at)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800):
                continue
            for ins in decoder.disasm(data[at:at + 4], base + at, count=1):
                if ins.mnemonic in ("bl", "blx") and ins.op_str.startswith("#0x") and int(ins.op_str[1:], 16) == WRAPPER:
                    thumb.append({"unit": name, "instruction": ins.address})
    assert direct == [{"unit": "main0", "instruction": 0x0209EDE8, "link": True, "condition": 14}]
    assert not pointers and not thumb
    return {"all_ARM_B_BL_candidates": direct, "all_byte_stored_pointer_candidates": pointers,
            "Thumb_BL_BLX_candidates": thumb,
            "units": [{"name": n, "base": b, "bytes": len(d), "sha256": sha(d)} for n, b, d in units],
            "computed_indirect_targets_and_other_file_readers_not_excluded": True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open("out/all_routes_combined_v581_candidate.nds"), NdsImage.open("work/clean.nds")
    digest = sha(rom.source.read_bytes())
    assert digest == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    arm, original_arm = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    assert arm[START - BASE:END - BASE] == original_arm[START - BASE:END - BASE]
    assert arm[0x4704C:0x470B4] == original_arm[0x4704C:0x470B4]
    source_census = census(rom, arm)
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not report.get("battery_save_preloaded")
    row = next(r for r in report["read_only_pause_RAM_snapshots"] if r["frame"] == 2000)
    raw = Path(row["path"]).read_bytes()
    assert sha(raw) == row["sha256"] and len(raw) == 0x400000
    pattern = struct.pack("<3I", 8, 52, 136)
    headers = [BASE + at for at in range(0, len(raw) - 20, 4) if raw[at:at + 12] == pattern]
    assert headers == [0x02192E34]
    parent = headers[0] - 0x934
    assert parent == 0x02192500
    u = machine(arm)
    u.mem_write(BASE, raw)
    for overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _id, fid: rom.rom.files[fid]).values():
        u.mem_write(overlay.ramAddress, bytes(overlay.data))
    blocks = IlnkContainer.parse(rom.read_file("/GRP/SLACKIMG.DK4")).blocks
    assert all(len(blocks[n]) == SIZE for n in range(14, 18))
    handles, io, calls, metadata, loaded, accesses, dma = {}, [], [], [], [], [], []
    paths = {p.casefold(): p for p in rom.path_map()}
    phase = {"name": "header_setup", "iteration": None}

    def code(uc, address, size, data):
        if address == 0x020E5650:
            raise ValueError("Original whole loop reached a native assertion")
        if address == 0x0209EDA8:
            phase.update(name="metadata", iteration=uc.reg_read(UC_ARM_REG_R9))
        elif address == 0x0209EDD4:
            metadata.append({"iteration": phase["iteration"], "native_virtual_target": uc.reg_read(UC_ARM_REG_R2),
                             "character": uc.reg_read(UC_ARM_REG_R0), "output": uc.reg_read(UC_ARM_REG_R1)})
        elif address == WRAPPER:
            phase["name"] = "archive_read"
            args = [uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
            assert args == [14 + phase["iteration"], RAW, 0, 0]
            calls.append(args)
        elif address == 0x0209EDEC:
            data = bytes(uc.mem_read(RAW, SIZE))
            assert data == blocks[14 + phase["iteration"]]
            loaded.append({"block": 14 + phase["iteration"], "sha256": sha(data), "bytes": len(data)})
            phase["name"] = "PXL_view"
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 128)).split(b"\0")[0].decode("ascii")
            name = "/" + name.replace("\\", "/").lstrip("/")
            path = paths[name.casefold()]
            assert obj not in handles
            payload = rom.read_file(path)
            handles[obj] = [path, payload, 0]
            uc.mem_write(obj + 0x20, struct.pack("<2I", 0, len(payload)))
            io.append({"operation": "open", "path": path, "phase": dict(phase)})
            result = 1
        elif address == SEEK:
            state = handles[obj]
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(state[1])
            state[2] = offset
            result = 1
        elif address == READ:
            state = handles[obj]
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            assert state[2] + count <= len(state[1])
            uc.mem_write(target, state[1][state[2]:state[2] + count])
            io.append({"operation": "read", "path": state[0], "offset": state[2], "target": target,
                       "bytes": count, "phase": dict(phase)})
            state[2] += count
            result = count
        else:
            io.append({"operation": "close", "path": handles.pop(obj)[0], "phase": dict(phase)})
            result = 1
        uc.reg_write(UC_ARM_REG_R0, result)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    def observe(uc, access, address, size, value, user):
        if address < RAW + SIZE and address + size > RAW:
            accesses.append({"PC": uc.reg_read(UC_ARM_REG_PC), "address": address, "bytes": size, "phase": dict(phase)})

    def observe_dma(uc, access, address, size, value, user):
        if address < 0x040000E0 and address + size > 0x040000B0:
            dma.append({"PC": uc.reg_read(UC_ARM_REG_PC), "address": address, "bytes": size, "value": value})

    h1 = u.hook_add(UC_HOOK_CODE, code)
    h2 = u.hook_add(UC_HOOK_MEM_READ, observe)
    h3 = u.hook_add(UC_HOOK_MEM_WRITE, observe_dma)
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.reg_write(UC_ARM_REG_LR, STOP)
    u.reg_write(UC_ARM_REG_R10, parent)
    try:
        u.emu_start(START, END, count=1000000)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
        u.hook_del(h3)
    assert u.reg_read(UC_ARM_REG_PC) == END and u.reg_read(UC_ARM_REG_SP) == STACK
    assert u.reg_read(UC_ARM_REG_R9) == 4 and u.reg_read(UC_ARM_REG_R8) == 128
    assert u.reg_read(UC_ARM_REG_R7) == parent + 4 * 48
    assert u.reg_read(UC_ARM_REG_R4) == 104 and u.reg_read(UC_ARM_REG_R6) == 136
    assert [r[0] for r in calls] == [14, 15, 16, 17] and len(metadata) == len(loaded) == 4
    assert not handles and not accesses and not dma
    assert {r["path"] for r in io} == {"/GRP/SLACKIMG.DK4"}
    assert bytes(u.mem_read(headers[0], 20)) == raw[headers[0] - BASE:headers[0] - BASE + 20]
    views = []
    for index in range(4):
        address = parent + 0x5B0 + index * 48
        fields = bytes(u.mem_read(address, 44))
        assert fields == raw[address - BASE:address - BASE + 44]
        owner = int.from_bytes(u.mem_read(address + 8, 4), "little")
        filename = int.from_bytes(u.mem_read(owner + 12, 4), "little")
        path = bytes(u.mem_read(filename, 96)).split(b"\0")[0].decode("ascii")
        assert path == f"_pxl/personbustup{index:02d}.pxl"
        assert struct.unpack_from("<2I", fields, 36) == (104, 136)
        views.append({"index": index, "persistent_view": address, "all44_fields_exact_capture": True,
                      "owner": owner, "filename": path, "size": [104, 136]})
    result = {"candidate_sha256": digest, "source_snapshot": row, "source_report": str(CAPTURE / "capture_report.json"),
              "source_report_sha256": sha((CAPTURE / "capture_report.json").read_bytes()),
              "current_source_census": source_census, "original_loop": [START, END],
              "loop_code_sha256": sha(arm[START - BASE:END - BASE]),
              "original_initialization_sets_counter0_and_height136": True,
              "real_metadata_virtual_calls": metadata, "original_wrapper_calls": calls,
              "complete_loaded_raw_blocks": loaded, "all_file_IO": io, "raw_buffer_read_events": accesses,
              "ARM9_DMA_register_writes_in_loop": dma,
              "existing20_byte_synthetic_header_reproduced_exact": True,
              "four_persisted_actual_PXL_views": views,
              "full_original_loop_control_reaches_counter4_and_end": True,
              "only_SDK_filesystem_calls_bridged_no_metadata_or_view_stub": True,
              "captured_parent_globals_and_scratch_stack_are_replay_inputs": True,
              "not_complete_UI_constructor_or_actual_GPU_trace": True,
              "hardware_async_and_later_consumers_outside_loop_not_simulated": True,
              "other_indirect_computed_targets_and_other_readers_remain_open": True,
              "no_global_unused_or_comic_display_claim": True,
              "script_sha256": sha(Path(__file__).read_bytes()),
              "ROM_and_patch_changed": False, "full_goal_complete": False}
    (ROOT / "original_loop_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"V588: full original4-iteration loop selects14..17;4 real virtual metadata calls/4 captured PXL views;raw read events={len(accesses)};not global non-use.")


if __name__ == "__main__":
    main()
