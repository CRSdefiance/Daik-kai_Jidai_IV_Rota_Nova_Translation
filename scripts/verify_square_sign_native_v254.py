"""Execute all five native sign rectangles and original menu source comparison."""

import json
import struct

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.square_sign_bounds import OFFSET, ROOT, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine


def main():
    prior = NdsImage.open("out/all_routes_combined_v253_candidate.nds").read_file("/__arm9__.bin")
    proposed = (ROOT / "research_arm9.bin").read_bytes()
    rebuilt, plan = transform(prior)
    assert proposed == rebuilt
    assert proposed[:OFFSET] == prior[:OFFSET] and proposed[OFFSET + 4:] == prior[OFFSET + 4:]
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    original_menu = []
    for lo, hi in [(0x5E3A8, 0x5E458), (0x51F4C, 0x52600), (0x52D8C, 0x52F00)]:
        assert clean[lo:hi] == prior[lo:hi] == proposed[lo:hi]
        original_menu.append({"start": lo, "end": hi, "original_Japanese_candidate_code_exact": True,
                              "sha256": sha(proposed[lo:hi])})
    u = machine(proposed)
    u.reg_write(UC_ARM_REG_SP, STACK)
    rectangle = struct.pack("<4I", 20, 0, 116, 0)
    cases = []
    for row in range(5):
        u.reg_write(UC_ARM_REG_R7, 8 + row * 32)
        u.reg_write(UC_ARM_REG_R6, 32 + row * 32)
        u.reg_write(UC_ARM_REG_R8, STACK + 0xC)
        u.mem_write(STACK + 8, b"\xA5" * 24)
        u.mem_write(STACK + 0x1C, rectangle)
        u.emu_start(BASE + 0x5F144, BASE + 0x5F15C, count=100)
        assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x5F15C and u.reg_read(UC_ARM_REG_SP) == STACK
        actual = struct.unpack("<4I", u.mem_read(STACK + 0xC, 16))
        assert actual == (20, 8 + row * 32, 116, 32 + row * 32)
        assert bytes(u.mem_read(STACK + 8, 4)) == b"\xA5" * 4
        assert bytes(u.mem_read(STACK + 0x1C, 16)) == rectangle
        # Outer port frame is x68..188, y8..176 on the lower DS screen.
        assert 68 <= 68 + actual[0] < 68 + actual[2] < 188
        assert 8 <= 8 + actual[1] < 8 + actual[3] < 176
        cases.append({"row": row, "actual_native_rectangle": actual, "unchanged_vertical_bounds": True,
                      "entire96_pixel_row_inside_original_frame": True})
    proof = {"format": "dk4-square-sign-native-v254", "plan": plan, "five_native_rows": cases,
             "original_Japanese_Trends_choice_menu_code_preserved": original_menu,
             "choice_overlay_classification": "Original temporary selection menu; not a permanent missing-caption defect.",
             "only_four_byte_right_coordinate_changed": True, "caption_backings_glyphs_palettes_borders_unchanged": True,
             "actual_GPU_selection_and_activation_pending": True, "all18_plaque_entries_remain_incomplete": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("All5 native sign row bounds fit the original frame; original choice-menu behavior and every unrelated ARM9 byte remain exact.")


if __name__ == "__main__":
    main()
