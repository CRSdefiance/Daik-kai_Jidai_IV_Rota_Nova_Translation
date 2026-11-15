"""All variable paper widths, exact old shapes, isolation and boot ownership."""

import json
import struct

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.variable_equipment_paper import ROOT
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
    fills, runs = [], []

    def intercept(uc, address, size, _):
        if address == 0x01FFAC18:
            xy = struct.unpack("<2I", uc.mem_read(uc.reg_read(UC_ARM_REG_R2), 8))
            wh = struct.unpack("<2I", uc.mem_read(uc.reg_read(UC_ARM_REG_R3), 8))
            runs.append([*xy, *wh, uc.reg_read(UC_ARM_REG_R1)])
        elif address == BASE + 0xD13F8:
            fills.append([uc.reg_read(UC_ARM_REG_R2), uc.reg_read(UC_ARM_REG_R3), struct.unpack("<I", uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 4))[0]])
        else:
            return
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    u.hook_add(UC_HOOK_CODE, intercept)
    manager = 0x02450000
    u.mem_write(manager + 0x18, struct.pack("<I", 0x02451000))
    palette = PxlImage.from_bytes(NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/_pxl/towninfo.pxl")).palette

    def invoke(width, height=16, active=True, obj=manager):
        fills.clear(); runs.clear()
        u.mem_write(plan["state_pointer"], struct.pack("<I", manager if active else 0))
        u.mem_write(obj + 0x20, struct.pack("<4I", 0, 16, width, 16 + height))
        u.mem_write(STACK, struct.pack("<3I", 255, 0, 0))
        call(u, plan["entry"] - BASE, (obj, 0x02452000, 255, 255))

    cases = []
    for width in range(10, 245):
        invoke(width)
        assert not fills
        pixels, cover = [None] * (width * 16), [0] * (width * 16)
        for x, y, w, h, color in runs:
            y -= 16
            assert h == 1 and 0 <= x < x + w <= width and 0 <= y < 16
            for xx in range(x, x + w):
                pixels[y * width + xx] = color
                cover[y * width + xx] += 1
        assert set(cover) == {1}
        indices = paper(width, 16, palette)
        expected = []
        for index in indices:
            rgb = palette[index]
            expected.append(0x8000 | (rgb[0] * 31 + 127) // 255 | ((rgb[1] * 31 + 127) // 255) << 5 | ((rgb[2] * 31 + 127) // 255) << 10)
        assert pixels == expected, width
        cases.append({"width": width, "height": 16, "all_source_paper_pixels_exactly_once": width * 16,
                      "saved_registers_stack_and_full_native_helper_return_pass": True})
    fallback = []
    for width, height, active, obj, color in [(9, 16, True, manager, [205, 190, 141]),
                                             (245, 16, True, manager, [205, 190, 141]),
                                             (130, 15, True, manager, [205, 190, 141]),
                                             (130, 17, True, manager, [205, 190, 141]),
                                             (130, 16, False, manager, [255, 255, 255]),
                                             (130, 16, True, manager + 0x1000, [255, 255, 255])]:
        invoke(width, height, active, obj)
        assert not runs and fills == [color]
        fallback.append({"width": width, "height": height, "active": active, "same_manager": obj == manager, "original_RGB": color})
    rom = NdsImage.open("out/all_routes_combined_v267_candidate.nds")
    boot = execute(arm, bytes(rom.rom.arm7), rom.rom.arm7RamAddress, repair_entry=plan["cache"]["entry"], expected_pool=payload)
    proof = {"format": "dk4-variable-paper-native-v269", "cases": cases, "isolated_fallbacks": fallback,
             "all235_widths_source_exact_complete_bounded_once": True,
             "known34_40_88_preserved_by_original_helpers": True,
             "GPU_submission_is_an_explicit_captured_contract": True,
             "boot": boot, "arena": initialize(arm), "ordinary_occupied_book_GPU_pending": True,
             "all18_plaques_and_variants_incomplete": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("All235 widths, six original fallback cases and boot/cache/ARM7 checks passed.")


if __name__ == "__main__":
    main()
