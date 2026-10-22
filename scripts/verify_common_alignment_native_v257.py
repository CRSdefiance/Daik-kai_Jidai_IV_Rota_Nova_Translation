"""Complete native first-line shift, continuation fidelity and guard/boot checks."""

import json
import struct

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.common_dialogue_alignment import BASE, POOL, ROOT
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.probe_common_itcm_arena_reservation import initialize
from scripts.probe_persistent_name_arm7_boot_overlap import execute


def raster(arm, text, entry, tracking=0, size=(240, 64), complete=True, instruction_limit=100000, glyph_events=None):
    u = machine(arm)
    u.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    header, view, ctx, string = 0x02450000, 0x02453000, 0x02454000, 0x02455000
    width, height = size
    pixels = width * height // 2
    original = struct.pack("<5I", 4, width // 4, height, 0x02452000 - header, 20)
    u.mem_write(header - 16, b"\xA5" * (20 + pixels + 32))
    u.mem_write(header, original + bytes(pixels))
    u.mem_write(view - 16, b"\xA5" * 80)
    call(u, 0xD3D80, (view,))
    u.mem_write(STACK, struct.pack("<4I", width, height, 0, 0))
    call(u, 0xD3AFC, (view, header, 0, 0))
    font = struct.unpack_from("<I", arm, 0xD5088)[0]
    u.mem_write(font + 4, struct.pack("<2I", 6, 16))
    kanji = NdsImage.open("out/all_routes_combined_v255_candidate.nds").read_file("/GRP/KANJI.FNT")
    u.mem_write(struct.unpack_from("<I", arm, 0xD19B8)[0], kanji)
    call(u, 0xD5160, (ctx, view, 1))
    call(u, 0xD5A10, (ctx, 1))
    u.mem_write(ctx + 28, struct.pack("<i", tracking))
    u.mem_write(string, text + b"\0")
    if glyph_events is not None:
        def observe(cpu, address, instruction_size, unused):
            if address in (BASE + 0xD16B4, 0x01FF83AC):
                code, style = struct.unpack('<2I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 8))
                glyph_events.append({'code': code, 'style': style,
                                     'x': cpu.reg_read(UC_ARM_REG_R2), 'y': cpu.reg_read(UC_ARM_REG_R3)})
        u.hook_add(UC_HOOK_CODE, observe)
    call(u, entry, (ctx, string), instruction_limit=instruction_limit)
    returned = u.reg_read(UC_ARM_REG_R0) - string
    if complete:
        assert returned == len(text)
    assert bytes(u.mem_read(string, len(text) + 1)) == text + b"\0"
    assert bytes(u.mem_read(header, 20)) == original
    assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + pixels, 16)) == b"\xA5" * 16
    assert bytes(u.mem_read(view - 16, 16)) == bytes(u.mem_read(view + 48, 16)) == b"\xA5" * 16
    assert struct.unpack("<i", u.mem_read(ctx + 28, 4))[0] == tracking
    packed = bytes(u.mem_read(header + 20, pixels))
    indices = bytes(n for b in packed for n in (b & 15, b >> 4))
    return indices if complete else (indices, returned)


def main():
    rom = NdsImage.open("out/all_routes_combined_v255_candidate.nds")
    old = rom.read_file("/__arm9__.bin")
    new = (ROOT / "research_arm9.bin").read_bytes()
    plan = json.loads((ROOT / "runtime_plan.json").read_text(encoding="utf-8"))
    font = GameAsciiFont.from_arm9(new)
    cases = []
    for first in ["A", "Fair. I wish a good", "Even phase", "Odd phase!", "Business? Fair. I wish a good"]:
        for continuation in ["Janus", "opportunity would arise."]:
            raw = ("  " + first + "\n  " + continuation).encode("ascii")
            before = raster(old, raw, 0xD5404)
            after = raster(new, raw, plan["helper"] - BASE)
            expected = bytearray(240 * 64)
            for text, y in [(first, 0), (continuation, 16)]:
                for n, char in enumerate(text):
                    glyph = font.decode(char)
                    for gy in range(11):
                        for gx in range(6):
                            if glyph.getpixel((gx, gy)):
                                expected[(y + gy) * 240 + 6 + n * 6 + gx] = 1
            assert after == bytes(expected), (first, continuation)
            assert after[16 * 240:] == before[16 * 240:]
            cases.append({"first": first, "continuation": continuation, "first_line_origin_before": 12,
                          "both_line_origins_after": 6, "full_native_font_ink_exact": sum(after),
                          "continuation_every_pixel_unchanged": True})
    for text, tracking in [(b"Ordinary text", 0), (b"   Intended indent", 0), (b"  Nonzero tracking", -1), (b"\x02Control", 0)]:
        assert raster(old, text, 0xD5404, tracking) == raster(new, text, plan["helper"] - BASE, tracking)
    for size in [(8, 12), (240, 12)]:
        raw = b"  Clipped view"
        assert raster(old, raw, 0xD5404, size=size, complete=False) == raster(new, raw, plan["helper"] - BASE, size=size, complete=False)
    for text in ["  Ｆirst line\n  Janus", "  Ｉ wish a good\n  opportunity"]:
        raw = text.encode("cp932")
        before = raster(old, raw, 0xD5404)
        after = raster(new, raw, plan["helper"] - BASE)
        assert after[16 * 240:] == before[16 * 240:]
        for y in range(16):
            assert after[y * 240:y * 240 + 234] == before[y * 240 + 6:(y + 1) * 240]
        cases.append({"full_width_literal": text, "first_line_all_native_pixels_shift_left6": True,
                      "every_continuation_pixel_unchanged": True, "all_native_ink_retained": sum(before) == sum(after)})
    payload = bytes(MainCodeFile(new, BASE).sections[3].data[:-48])
    boot = execute(new, bytes(rom.rom.arm7), rom.rom.arm7RamAddress,
                   repair_entry=plan["cache"]["entry"], expected_pool=payload)
    proof = {"format": "dk4-common-alignment-native-v257", "cases": cases,
             "four_original_fallback_cases_byte_exact": True, "source_bytes_and_protected_LF_guards_unchanged": True,
             "two_undersized_view_pixel_and_return_pointer_cases_unchanged": True,
             "return_pointer_tracking_stack_saved_registers_and_pixel_guards_pass": True,
             "boot": boot, "arena": initialize(new), "actual_GPU_cold_boot_pending": True,
             "all18_plaques_remain_incomplete": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("12 full native alignment/Janus/phase/CP932 cases,4 untouched fallbacks and boot/cache/ARM7 checks passed.")


if __name__ == "__main__":
    main()
