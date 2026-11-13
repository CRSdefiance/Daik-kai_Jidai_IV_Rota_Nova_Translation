"""Native Square canvas ABI, category isolation, bounds and startup checks.

The header and goods index are controlled input contracts. Actual GPU adoption
and full caption pixels require the separately recorded ordinary cold boot.
"""

import json
import struct

from ndspy.code import MainCodeFile
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.square_shop_labels import ROOT, SLOT_BYTES
from dk4tool.rom.nds import NdsImage
from scripts.prepare_plaque_style_v247 import save
from scripts.probe_button_prompt_native import SAVED, STACK, STOP, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute


def main():
    arm = (ROOT / "research_arm9.bin").read_bytes()
    plan = json.loads((ROOT / "runtime_plan.json").read_text(encoding="utf-8"))
    u = machine(arm)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    u.mem_write(POOL, payload)
    header, view, palette = 0x02450000, 0x02451000, 0x02452000
    table = struct.unpack_from("<I", arm, 0xCB12C)[0]
    font_object = struct.unpack_from("<I", arm, 0xD5088)[0]
    u.mem_write(font_object + 4, struct.pack("<2I", 6, 12))
    font = GameAsciiFont.from_arm9(arm)
    cases = []
    for category in range(19):
        # Supply one goods row, without replacing either native category getter.
        u.mem_write(table + 16, bytes([category]))
        original = struct.pack("<5I", 4, 12, 12, palette - header, 20)
        u.mem_write(header, original + bytes(288))
        u.mem_write(view - 16, b"\xA5" * 80)
        call(u, 0xD3D80, (view,))
        saved = {reg: 0xA5A51000 + n for n, reg in enumerate(SAVED)}
        saved[UC_ARM_REG_R4] = 0
        for reg, value in saved.items():
            u.reg_write(reg, value)
        for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (view, header, 0, 0)):
            u.reg_write(reg, value)
        u.mem_write(STACK, struct.pack("<4I", 48, 12, 0, 0))
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.emu_start(plan["helpers"]["canvas"]["entry"], STOP, count=100000)
        assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
        assert all(u.reg_read(reg) == value for reg, value in saved.items())
        assert bytes(u.mem_read(header, len(original))) == original
        assert bytes(u.mem_read(view - 16, 16)) == bytes(u.mem_read(view + 48, 16)) == b"\xA5" * 16
        width, height = struct.unpack("<2I", u.mem_read(view + 40, 8))
        assert (width, height) == ((64, 12) if category < 18 else (48, 12))
        if category < 18:
            destination = plan["buffers"] + category * SLOT_BYTES
            depth, words, rows, pal, pixels = struct.unpack("<5I", u.mem_read(destination, 20))
            assert (depth, words, rows, pixels) == (4, 16, 12, 20)
            assert (destination + pal) & 0xFFFFFFFF == palette
            assert bytes(u.mem_read(destination + 404, 12)) == bytes(12)
        call(u, 0xC5BA0, (category,))
        original_pointer = u.reg_read(UC_ARM_REG_R0)
        call(u, plan["helpers"]["category"]["entry"] - BASE, (category,))
        result = u.reg_read(UC_ARM_REG_R0)
        if category == 11:
            assert bytes(u.mem_read(result, 8)) == b"Jewelry\0" and result != original_pointer
        else:
            assert result == original_pointer
        if category < 18:
            text = bytes(u.mem_read(result, 32)).split(b"\0", 1)[0].decode("ascii") + " Shop"
            context, string = 0x02453000, 0x02453100
            u.mem_write(string, text.encode("ascii") + b"\0")
            # A cleared pixel plane is supplied; native clear/GPU adoption
            # belong to the ordinary cold-boot verification.
            u.mem_write(destination + 20, bytes(384))
            call(u, 0xD5160, (context, view, 1))
            call(u, plan["helpers"]["paint"]["entry"] - BASE, (context, string))
            assert struct.unpack("<i", u.mem_read(context + 28, 4))[0] == -1
            assert bytes(u.mem_read(context + 68, 4)) == bytes(4)
            actual = bytes(u.mem_read(destination + 20, 384))
            indices = [value >> shift & 15 for value in actual for shift in (0, 4)]
            expected = [0] * (64 * 12)
            for n, character in enumerate(text):
                glyph = font.decode(character)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            col = n * 5 + x
                            assert col < 64
                            expected[y * 64 + col] = 1
            assert indices == expected, (category, text, sum(indices), sum(expected))
            assert bytes(u.mem_read(destination + 404, 12)) == bytes(12)
        cases.append({"category": category, "width": width, "height": height,
                      "native_constructor_full_ABI_header_palette_and_guards_pass": True,
                      "only_category11_name_changed_in_this_caller": True})
        if category < 18:
            cases[-1].update({"full_English": text, "all_glyph_ink_first_internal_final_exact": True,
                              "original_derived_context_field_preserved": True})
    rom = NdsImage.open("out/all_routes_combined_v252_candidate.nds")
    boot = execute(arm, bytes(rom.rom.arm7), rom.rom.arm7RamAddress,
                   repair_entry=plan["cache"]["entry"], expected_pool=payload)
    save(ROOT / "native_proof.json", {"format": "dk4-square-native-v253", "cases": cases,
         "boot": boot, "arena": initialize(arm), "actual_GPU_complete_captions_pending": True,
         "all18_base_plaque_hint_audit_entries_remain_incomplete": True,
         "controlled_header_goods_index_contract_not_live_inventory_proof": True})
    print("19 native canvas/category cases and original ABI, bounds, palette, boot/cache/ARM7 checks passed.")


if __name__ == "__main__":
    main()
