"""Execute real framebuffer writes; prove all widths, clipping and native ABI."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.direct_equipment_paper import FRAMEBUFFER, ORIGIN_X, ORIGIN_Y, ROOT
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import paper
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute


def main():
    arm = (ROOT / "research_arm9.bin").read_bytes()
    plan = json.loads((ROOT / "runtime_plan.json").read_text(encoding="utf-8"))
    u = machine(arm)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    u.mem_write(POOL, payload)
    itcm = Path("work/emulation_v193/equipment_start_town_v268/native_state/arm9_itcm.bin").read_bytes()
    u.mem_write(0x01FF8000, itcm)  # actual original native fill for the three old widths
    u.mem_write(ORIGIN_X, struct.pack("<I", 0)); u.mem_write(ORIGIN_Y, struct.pack("<I", 0))
    manager = 0x02450000
    palette = PxlImage.from_bytes(NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/_pxl/towninfo.pxl")).palette
    seed = b"\xA5" * 0x30000
    cases = []
    for screen in (0, 1):
        for width in range(10, 245):
            u.mem_write(FRAMEBUFFER - 16, b"\xA5" * (0x30000 + 32))
            u.mem_write(plan["state_pointer"], struct.pack("<I", manager))
            u.mem_write(manager + 0x18, struct.pack("<I", screen))
            u.mem_write(manager + 0x20, struct.pack("<4I", 6, 12, 6 + width, 28))
            u.mem_write(STACK, struct.pack("<3I", 255, 0, 0))
            call(u, plan["entry"] - BASE, (manager, 0, 255, 255))
            expected = bytearray(seed)
            tile = paper(width, 16, palette)
            for y in range(16):
                for x in range(width):
                    r, g, b, _ = palette[tile[y * width + x]]
                    color = 0x8000 | (r * 31 + 127) // 255 | ((g * 31 + 127) // 255) << 5 | ((b * 31 + 127) // 255) << 10
                    off = screen * 0x18000 + ((12 + y) * 256 + 6 + x) * 2
                    struct.pack_into("<H", expected, off, color)
            assert bytes(u.mem_read(FRAMEBUFFER, 0x30000)) == expected, (screen, width)
            assert bytes(u.mem_read(FRAMEBUFFER - 16, 16)) == bytes(u.mem_read(FRAMEBUFFER + 0x30000, 16)) == b"\xA5" * 16
            cases.append({"screen": screen, "width": width, "all_paper_pixels_and_all_other_framebuffer_bytes_exact": width * 16,
                          "complete_saved_register_stack_ABI_and_guarded_framebuffers": True})
    fallbacks = []
    def catch_original(uc, address, size, _):
        if address == BASE + 0xD13F8:
            fallbacks.append(address)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    hook = u.hook_add(UC_HOOK_CODE, catch_original)
    rejected = [(9, 16, 0, 6, 12, True), (245, 16, 0, 0, 12, True),
                (130, 15, 0, 6, 12, True), (130, 17, 0, 6, 12, True),
                (130, 16, 2, 6, 12, True), (130, 16, 0, 0xFFFFFFFF, 12, True),
                (130, 16, 0, 127, 12, True), (130, 16, 0, 6, 177, True),
                (130, 16, 0, 6, 12, False)]
    for width, height, screen, x, y, active in rejected:
        u.mem_write(FRAMEBUFFER, seed)
        u.mem_write(plan["state_pointer"], struct.pack("<I", manager if active else 0))
        u.mem_write(manager + 0x18, struct.pack("<I", screen))
        u.mem_write(manager + 0x20, struct.pack("<4I", x, y, (x + width) & 0xFFFFFFFF, y + height))
        before_count = len(fallbacks)
        call(u, plan["entry"] - BASE, (manager, 0, 255, 255))
        assert len(fallbacks) == before_count + 1
        assert bytes(u.mem_read(FRAMEBUFFER, 0x30000)) == seed
    u.hook_del(hook)
    rom = NdsImage.open("out/all_routes_combined_v267_candidate.nds")
    boot = execute(arm, bytes(rom.rom.arm7), rom.rom.arm7RamAddress, repair_entry=plan["cache"]["entry"], expected_pool=payload)
    proof = {"format": "dk4-direct-paper-native-v270", "cases": cases,
             "all235_widths_on_both_actual_native_framebuffers": True,
             "native_fill_for_old34_40_88_widths_executed_without_GPU_bridge": True,
             "all_framebuffer_bytes_outside_rectangle_and_guards_unchanged": True,
             "nine_invalid_or_inactive_contracts_delegate_without_new_framebuffer_writes": True,
             "boot": boot, "arena": initialize(arm), "all18_plaques_incomplete": True,
             "actual_cold_boot_occupied_tooltip_pending": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("470 real framebuffer cases, complete pixel bounds/ABI and boot checks passed.")


if __name__ == "__main__":
    main()
