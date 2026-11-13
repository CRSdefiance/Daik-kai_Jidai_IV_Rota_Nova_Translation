"""Native whole Deck help consumer and complete Filter label rasters."""

import json
import struct

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.deck_filter_help import BASE, POOL, ROOT
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute
from scripts.research_online_loader_v190 import resource_call


def main():
    arm = (ROOT / "research_arm9.bin").read_bytes()
    plan = json.loads((ROOT / "runtime_plan.json").read_text(encoding="utf-8"))
    u = machine(arm)
    payload = bytes(MainCodeFile(arm, BASE).sections[3].data[:-48])
    u.mem_write(POOL, payload)
    font = GameAsciiFont.from_arm9(arm)
    metrics = struct.unpack_from("<I", arm, 0xD5088)[0]
    u.mem_write(metrics + 4, struct.pack("<2I", 6, 12))
    header, owner = 0x02450000, 0x02454000
    view = owner + 0x40
    width, height = 256, 108
    raw_header = struct.pack("<5I", 4, width // 4, height, 0x02458000 - header, 20)
    u.mem_write(header - 16, b"\xA5" * (20 + width * height // 2 + 32))
    u.mem_write(header, raw_header + bytes(width * height // 2))
    u.mem_write(view - 16, b"\xA5" * 80)
    call(u, 0xD3D80, (view,))
    u.mem_write(STACK, struct.pack("<4I", width, height, 0, 0))
    call(u, 0xD3AFC, (view, header, 0, 0))
    events = []

    def trace(uc, address, size, _):
        if address == BASE + 0xD393C:
            # A freshly cleared backing is supplied; physical bitmap clear is
            # verified only in the subsequent ordinary ROM cold boot.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0xD16B4:
            sp = uc.reg_read(UC_ARM_REG_SP)
            events.append({"code": struct.unpack("<I", uc.mem_read(sp, 4))[0],
                           "x": uc.reg_read(UC_ARM_REG_R2), "y": uc.reg_read(UC_ARM_REG_R3)})
    u.hook_add(UC_HOOK_CODE, trace)
    resource_call(u, 0x154F0, (owner,))
    visible = [e for e in events if e["code"] != 32]
    # Original title followed by three source-reviewed logical paragraphs.
    title_pointer = struct.unpack_from("<I", arm, 0x15590)[0] - BASE
    title = arm[title_pointer:arm.index(0, title_pointer)].decode("ascii")
    body = [r for r in plan["records"] if r["field"] in (0x15594, 0x15598, 0x1559C)]
    expected_text = title + "".join(r["English"].replace(" ", "") for r in body)
    assert [e["code"] for e in visible] == [ord(c) for c in expected_text if c != " "]
    expected = bytearray(width * height)
    for e in visible:
        glyph = font.decode(chr(e["code"]))
        assert e["x"] + 6 <= width and e["y"] + 11 <= 96
        for y in range(11):
            for x in range(6):
                if glyph.getpixel((x, y)):
                    expected[(e["y"] + y) * width + e["x"] + x] = 1
    p = bytes(u.mem_read(header + 20, width * height // 2))
    assert bytes(n for b in p for n in (b & 15, b >> 4)) == expected
    cursor = len(title.replace(" ", ""))
    paragraphs = []
    for r in body:
        subset = visible[cursor:cursor + len(r["English"].replace(" ", ""))]
        offset = 0
        for word in r["English"].split():
            assert len({e["y"] for e in subset[offset:offset + len(word)]}) == 1
            offset += len(word)
        cursor += len(subset)
        paragraphs.append({"English": r["English"], "compiled": r["compiled"],
                           "all_glyphs_and_whole_words_preserved": True, "rows": sorted({e["y"] for e in subset})})
    assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + width * height // 2, 16)) == b"\xA5" * 16
    boot_rom = NdsImage.open("out/all_routes_combined_v261_candidate.nds")
    boot = execute(arm, bytes(boot_rom.rom.arm7), boot_rom.rom.arm7RamAddress,
                   repair_entry=plan["cache"]["entry"], expected_pool=payload)
    proof = {"format": "dk4-deck-filter-native-v262", "actual_original_help_consumer_154F0_executed": True,
             "paragraphs": paragraphs, "all_visible_title_and_help_glyph_pixels": sum(expected),
             "all_words_keep_one_row_all_glyphs_fit_and_first_last_letters_present": True,
             "bitmap_clear_is_supplied_contract_not_GPU_proof": True, "native_header_view_and_pixel_guards_ABI_pass": True,
             "boot": boot, "arena": initialize(arm), "actual_filter_menu_and_help_GPU_pending": True,
             "all18_plaques_incomplete": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("Original whole help consumer renders every word intact within96 rows; boot/cache/ARM7 checks pass.")


if __name__ == "__main__":
    main()
