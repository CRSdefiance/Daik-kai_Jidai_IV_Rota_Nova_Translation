"""Verify trace ABI, source-rectangle contracts, deduplication and bounded overflow."""

import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_blitter_trace_v603 import (
    CAPACITY,
    CONTROL,
    CORNER,
    END,
    ENTRY,
    FIELDS,
    RECORDS,
    ROOT,
    STRIDE,
    TILE,
)
from scripts.probe_button_prompt_native import STACK, machine

REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_LR)
HEADER, XY, SIZE, DEST, VIEW = (0x02380000, 0x02381000, 0x02381010, 0x02381020, 0x02381100)


def read_log(u):
    control = struct.unpack("<6I", u.mem_read(CONTROL, 24))
    assert control[2] <= CAPACITY and control[5] == 0x603B117
    return control, [dict(zip(FIELDS, struct.unpack("<20I", u.mem_read(RECORDS + i * STRIDE, STRIDE)), strict=True))
                     for i in range(control[2])]


def main():
    manifest = json.loads((ROOT / "fixture_manifest.json").read_text(encoding="utf-8"))
    path = Path(manifest["research_ROM"])
    assert sha(path.read_bytes()) == manifest["research_ROM_sha256"]
    rom = NdsImage.open(path)
    arm = rom.read_file("/__arm9__.bin")
    u = machine(arm)
    overlay = loadOverlayTable(rom.rom.arm9OverlayTable, lambda _id, fid: rom.rom.files[fid])[0]
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    initial = bytes(u.mem_read(CONTROL, END - CONTROL))
    u.mem_write(ENTRY - 16, b"\xA5" * 16)
    u.mem_write(END, b"\xA5" * 16)
    u.mem_write(VIEW, struct.pack("<4I", 0x0216017C, 0, 0, 0x02313F60))
    cases = []

    def reset():
        u.mem_write(CONTROL, initial)

    def invoke(kind, width=64, height=256, crop=(208, 32, 48, 8), depth=4, dx=12, flags=0xA0000000, adapter=True):
        payload = struct.pack("<5I", depth, width, height, 20, 52) + bytes(32) + b"\x12\x34\x56\x78" * 8
        u.mem_write(HEADER, payload)
        u.mem_write(XY, struct.pack("<4i", *crop))
        u.mem_write(SIZE, struct.pack("<2i", *crop[2:]))
        u.mem_write(DEST, struct.pack("<4i", dx, 22, dx + crop[2], 22 + crop[3]))
        u.mem_write(STACK, struct.pack("<2I", *((SIZE, DEST) if not kind else (DEST, 0))))
        values = [0xA5100000 + i for i in range(14)]
        values[0:4] = [1, HEADER, 9, XY]
        values[5] = VIEW
        values[13] = 0x020CFDE0 if adapter and not kind else 0x027E0000
        cpsr = (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | flags
        u.reg_write(UC_ARM_REG_CPSR, cpsr)
        u.reg_write(UC_ARM_REG_SP, STACK)
        for register, value in zip(REGS, values, strict=True):
            u.reg_write(register, value)
        address = TILE if kind else CORNER
        handle = u.hook_add(UC_HOOK_CODE, lambda uc, a, size, data: uc.emu_stop() if a == address + 4 else None)
        try:
            u.emu_start(address, address + 4, count=100000)
        finally:
            u.hook_del(handle)
        assert u.reg_read(UC_ARM_REG_PC) == address + 4
        assert [u.reg_read(r) for r in REGS] == values
        assert u.reg_read(UC_ARM_REG_CPSR) == cpsr
        saved_values = values[4:12] + [values[13]] if kind else values[4:10] + [values[13]]
        sp = STACK - len(saved_values) * 4
        assert u.reg_read(UC_ARM_REG_SP) == sp
        assert bytes(u.mem_read(sp, len(saved_values) * 4)) == struct.pack("<" + "I" * len(saved_values), *saved_values)
        assert bytes(u.mem_read(HEADER, len(payload))) == payload
        assert bytes(u.mem_read(XY, 16)) == struct.pack("<4i", *crop)
        assert bytes(u.mem_read(ENTRY - 16, 16)) == bytes(u.mem_read(END, 16)) == b"\xA5" * 16
        return read_log(u)

    for kind in (0, 1):
        for width, height, crop in ((64, 256, (208, 32, 48, 8)), (128, 256, (464, 40, 32, 8)),
                                    (12, 20, (0, 0, 48, 20)), (6, 8, (0, 0, 24, 8)),
                                    (64, 256, (208, 32, 0, 0))):
            for flags in (0, 0xF0000000):
                reset()
                control, records = invoke(kind, width, height, crop, flags=flags)
                assert control[:4] == (1, 1, 1, 0)
                row = records[0]
                assert [row[k] for k in FIELDS[5:9]] == list(crop)
                assert [row[k] for k in FIELDS[9:13]] == [12, 22, crop[2], crop[3]]
                assert row["kind"] == kind and row["header"] == HEADER and row["bank"] == 9
                assert row["adapter_owner"] == (0x02313F60 if not kind else 0)
                assert row["first_pixel_word"] == 0x78563412 and row["hits"] == 1
                invoke(kind, width, height, crop, flags=flags)
                control, records = read_log(u)
                assert control[:4] == (2, 2, 1, 0) and records[0]["hits"] == 2
                cases.append({"kind": kind, "dimensions_words_height": [width, height], "crop": crop,
                              "flags": flags, "full_register_stack_flags_source_and_trace_contract": True})
    for kind in (0, 1):
        reset()
        for depth in (8, 16):
            control, records = invoke(kind, depth=depth)
            assert not records
        control, records = invoke(kind, width=40, height=90)
        assert not records
        # A normal atlas crop records one positive control. Subsequent unrelated
        # atlas crops are excluded without hiding overflow or claiming nonuse.
        control, records = invoke(kind, crop=(0, 104, 16, 8))
        assert len(records) == 1 and control[4] == 1 << kind
        control, records = invoke(kind, crop=(16, 104, 16, 8))
        assert len(records) == 1
        reset()
        for index in range(CAPACITY + 3):
            control, records = invoke(kind, dx=index, adapter=False)
        assert control[:4] == (CAPACITY + 3, CAPACITY + 3, CAPACITY, 3)
        invoke(kind, dx=0, adapter=False)
        control, records = read_log(u)
        assert control[3] == 3 and records[0]["hits"] == 2
    proof = {"fixture_manifest_sha256": sha((ROOT / "fixture_manifest.json").read_bytes()),
        "script_sha256": sha(Path(__file__).read_bytes()), "ABI_source_contract_cases": cases,
        "deduplication_both_routines": True, "bounded_overflow_both_routines": True,
        "wrong_depth_and_dimensions_rejected": True, "one_positive_control_per_routine": True,
        "original_resource_coordinate_and_destination_inputs_unchanged": True,
        "unicorn_stops_after_displaced_prologue_not_full_native_gameplay": True, "goal_complete": False}
    (ROOT / "ABI_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"V603 ABI: {len(cases)} full register/flags/stack/source cases; both dedup/overflow/negative filters pass.")


if __name__ == "__main__":
    main()
