"""All widths, complete framebuffer bytes, ABI, and invalid-contract tests."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.direct_equipment_paper import FRAMEBUFFER, ORIGIN_X, ORIGIN_Y
from dk4tool.patch.equipment_source_grain import transform
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROOT = Path("work/analysis/equipment_texture_v543")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean = NdsImage.open("work/clean.nds")
    arm = NdsImage.open("out/all_routes_combined_v542_candidate.nds").read_file("/__arm9__.bin")
    result, plan = transform(arm, clean)
    (ROOT / "research_arm9.bin").write_bytes(result)
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    old_tile = Path("work/analysis/direct_equipment_v270/paper_tile.bin").read_bytes()
    u = machine(result)
    u.mem_write(POOL, bytes(MainCodeFile(result, BASE).sections[3].data[:-48]))
    manager = 0x02450000
    u.mem_write(ORIGIN_X, bytes(4))
    u.mem_write(ORIGIN_Y, bytes(4))
    seed = b"\xA5" * 0x30000
    cases = []
    for screen in (0, 1):
        for width in range(10, 245):
            u.mem_write(FRAMEBUFFER - 16, b"\xA5" * (0x30000 + 32))
            u.mem_write(plan["state_pointer"], struct.pack("<I", manager))
            u.mem_write(manager + 0x18, struct.pack("<I", screen))
            u.mem_write(manager + 0x20, struct.pack("<4I", 6, 12, 6 + width, 28))
            call(u, plan["entry"] - BASE, (manager, 0, 255, 255))
            expected = bytearray(seed)
            for y in range(16):
                for x in range(width):
                    dx = x if x < 2 else 42 + x - (width - 2) if x >= width - 2 else 2 + (x - 2) % 40
                    if 2 <= y < 14 and 2 <= x < width - 2:
                        rgb = donor.palette[donor.indices[(60 + y) * donor.width + dx]][:3]
                        r, g, b = [(v * 31 + 127) // 255 for v in rgb]
                        color = 0x8000 | r | (g << 5) | (b << 10)
                    else:
                        color = struct.unpack_from("<H", old_tile, (y * 44 + dx) * 2)[0]
                    at = screen * 0x18000 + ((12 + y) * 256 + 6 + x) * 2
                    struct.pack_into("<H", expected, at, color)
            assert bytes(u.mem_read(FRAMEBUFFER, 0x30000)) == expected, (screen, width)
            assert bytes(u.mem_read(FRAMEBUFFER - 16, 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(FRAMEBUFFER + 0x30000, 16)) == b"\xA5" * 16
            cases.append({"screen": screen, "width": width,
                          "source_grain_and_retained_bevel_pixels": width * 16,
                          "all_other_framebuffer_bytes_guards_and_saved_register_stack_ABI_exact": True})
    fallbacks = []

    def catch_original(uc, address, _size, _data):
        if address == plan["old_dispatcher"]:
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
        count = len(fallbacks)
        call(u, plan["entry"] - BASE, (manager, 0, 255, 255))
        assert len(fallbacks) == count + 1
        assert bytes(u.mem_read(FRAMEBUFFER, 0x30000)) == seed
    u.hook_del(hook)
    proof = {"plan": plan, "complete_native_painter_cases": cases,
             "all235_widths_on_both_framebuffers": True,
             "heading_88_and_short_34_40_use_same_source_grain": True,
             "nine_invalid_contracts_delegate_at_original_dispatcher_without_new_writes": True,
             "original_fallback_gpu_execution_not_claimed": True,
             "cold_boot_gameplay_pending": True, "all18_entries_remain_incomplete": True}
    (ROOT / "native_painter_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("470 complete direct-painter cases and nine guarded fallbacks pass; no new memory/code slots.")


if __name__ == "__main__":
    main()
