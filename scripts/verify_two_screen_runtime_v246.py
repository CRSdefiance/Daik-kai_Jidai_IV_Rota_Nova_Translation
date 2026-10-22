"""Verify bounded bar widths, scoped tooltip styling and boot/cache safety."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
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

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute

ROOT = Path("work/analysis/two_screen_layout_v246")
RECORD = 0x02460020


def main():
    arm = (ROOT / "research_arm9.bin").read_bytes()
    plan = json.loads((ROOT / "runtime_plan.json").read_text(encoding="utf-8"))
    u = machine(arm)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    u.mem_write(POOL, payload)
    width_cases = []
    for value in [-100, -1, 0, 1, 2, 47, 58, 88, 99, 100, 101, 255]:
        u.mem_write(RECORD - 16, b"\xa5" * 48)
        call(u, plan["helpers"]["bar_width"]["entry"] - BASE, (value & 0xffffffff, 0, RECORD))
        actual = struct.unpack("<I", u.mem_read(RECORD + 8, 4))[0]
        assert actual == max(0, min(value, 100)) // 2
        assert bytes(u.mem_read(RECORD - 16, 24)) == b"\xa5" * 24
        assert bytes(u.mem_read(RECORD + 12, 20)) == b"\xa5" * 20
        width_cases.append([value, actual])
    seen = []

    def intercept(uc, address, size, _):
        if address == BASE + 0x7430:
            args = [uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
            stack = list(struct.unpack("<4I", uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 16)))
            seen.append({"operation": "original_tooltip_constructor", "args": args, "stack_args": stack})
            uc.reg_write(UC_ARM_REG_R0, 0)
        elif address == BASE + 0xD393C:
            seen.append({"operation": "original_bitmap_clear", "bitmap": uc.reg_read(UC_ARM_REG_R0)})
        elif address == BASE + 0xD13F8:
            seen.append({"operation": "original_rectangle_fill", "manager": uc.reg_read(UC_ARM_REG_R0),
                         "RGB": [uc.reg_read(UC_ARM_REG_R2), uc.reg_read(UC_ARM_REG_R3),
                                 struct.unpack("<I", uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 4))[0]]})
        else:
            return
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, intercept)
    state = plan["state_pointer"]
    try:
        manager = 0x02450000
        stacked = (0, 0, 0xfffffffc, 15)
        u.mem_write(STACK, struct.pack("<4I", *stacked))
        call(u, plan["helpers"]["equipment_tooltip"]["entry"] - BASE, (manager, 0x02451000, 0x02452000, 0))
        assert seen[-1]["args"] == [manager, 0x02451000, 0x02452000, 0]
        assert seen[-1]["stack_args"] == list(stacked)
        assert struct.unpack("<I", u.mem_read(state, 4))[0] == manager
        for obj, rgb in [(manager, [205,190,141]), (manager+0x1000, [255,255,255])]:
            u.mem_write(STACK, struct.pack("<3I", 255,0,0))
            call(u, plan["helpers"]["tooltip_fill"]["entry"] - BASE, (obj, 0x02453000,255,255))
            assert seen[-1]["RGB"] == rgb
        call(u, plan["helpers"]["tooltip_reset"]["entry"] - BASE, (manager+0x30,))
        assert struct.unpack("<I", u.mem_read(state, 4))[0] == 0
        u.mem_write(STACK, struct.pack("<3I",255,0,0))
        call(u, plan["helpers"]["tooltip_fill"]["entry"] - BASE, (manager,0x02453000,255,255))
        assert seen[-1]["RGB"] == [255,255,255]
    finally:
        u.hook_del(hook)
    rom = NdsImage.open("out/all_routes_combined_v245_candidate.nds")
    boot = execute(arm, bytes(rom.rom.arm7), rom.rom.arm7RamAddress,
                   repair_entry=plan["cache"]["entry"], expected_pool=payload)
    arena = initialize(arm)
    proof = {"format": "dk4-two-screen-runtime-native-v246", "width_cases": width_cases,
             "tooltip_constructor_original_registers_stack_and_saved_register_ABI_verified": True,
             "same_manager_theme_and_other_manager_default_verified": True,
             "next_generic_tooltip_reset_prevents_theme_leak": True,
             "rectangle_fill_and_constructor_calls_are_captured_contracts_not_GPU_proof": seen,
             "boot": boot, "arena": arena, "cold_boot_both_screens_pending": True,
             "full_goal_complete": False}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("Native width bounds, stacked tooltip ABI, theme isolation/reset and startup/cache/ARM7 verification passed.")


if __name__ == "__main__":
    main()
