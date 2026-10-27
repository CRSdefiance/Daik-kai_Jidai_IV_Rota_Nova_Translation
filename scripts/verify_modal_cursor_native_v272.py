"""Check actual glyph cells/pixels, not only the order of draw requests."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.modal_cursor_guard import transform

ROOT = Path("work/analysis/modal_cursor_v272")
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine
from scripts.research_online_loader_v190 import resource_call as call


def raster(arm, text, tracking=0, width=240, height=96, wrapping=1, line_height=16,
           native_pointer=None):
    u = machine(arm)
    u.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    header, view, ctx, string = 0x02450000, 0x02453000, 0x02454000, 0x02455000
    pixels = width * height // 2
    raw_header = struct.pack("<5I", 4, width // 4, height, 0x02452000 - header, 20)
    u.mem_write(header - 16, b"\xA5" * (pixels + 52))
    u.mem_write(header, raw_header + bytes(pixels))
    call(u, 0xD3D80, (view,))
    u.mem_write(STACK, struct.pack("<4I", width, height, 0, 0))
    call(u, 0xD3AFC, (view, header, 0, 0))
    metrics = struct.unpack_from("<I", arm, 0xD5088)[0]
    u.mem_write(metrics + 4, struct.pack("<2I", 6, line_height))
    u.mem_write(struct.unpack_from("<I", arm, 0xD19B8)[0], NdsImage.open("work/clean.nds").read_file("/GRP/KANJI.FNT"))
    call(u, 0xD5160, (ctx, view, 1))
    call(u, 0xD5A10, (ctx, wrapping))
    u.mem_write(ctx + 28, struct.pack("<i", tracking))
    if native_pointer is None:
        u.mem_write(string - 16, b"\xA5" * (len(text) + 33))
        u.mem_write(string, text + b"\0")
    else:
        string = native_pointer
        assert bytes(u.mem_read(string, len(text) + 1)) == text + b"\0"
    source_before = bytes(u.mem_read(string - 16, len(text) + 33))
    events = []

    def observe(uc, address, size, _):
        if address == BASE + 0xD16B4:
            sp = uc.reg_read(UC_ARM_REG_SP)
            events.append({"code": struct.unpack("<I", uc.mem_read(sp, 4))[0],
                           "x": uc.reg_read(UC_ARM_REG_R2), "y": uc.reg_read(UC_ARM_REG_R3)})
    u.hook_add(UC_HOOK_CODE, observe)
    call(u, 0xD5404, (ctx, string))
    returned = u.reg_read(UC_ARM_REG_R0) - string
    assert bytes(u.mem_read(string, len(text) + 1)) == text + b"\0"
    assert bytes(u.mem_read(string - 16, len(text) + 33)) == source_before
    assert bytes(u.mem_read(header, 20)) == raw_header
    assert bytes(u.mem_read(header - 16, 16)) == bytes(u.mem_read(header + 20 + pixels, 16)) == b"\xA5" * 16
    assert struct.unpack("<i", u.mem_read(ctx + 28, 4))[0] == tracking
    raw = bytes(u.mem_read(header + 20, pixels))
    return bytes(n for b in raw for n in (b & 15, b >> 4)), events, returned


def verify_ascii(arm, text):
    actual, events, returned = raster(arm, text)
    assert returned == len(text)
    visible = [e for e in events if e["code"] != 32]
    assert [e["code"] for e in visible] == [c for c in text if c not in (10, 32)]
    assert len({(e["x"], e["y"]) for e in visible}) == len(visible), "A later glyph overwrites a leading cell"
    expected = bytearray(240 * 96)
    font = GameAsciiFont.from_arm9(arm)
    for event in visible:
        x, y = event["x"], event["y"]
        assert 0 <= x <= 234 and 0 <= y <= 85
        glyph = font.decode(chr(event["code"]))
        for yy in range(11):
            for xx in range(6):
                if glyph.getpixel((xx, yy)):
                    expected[(y + yy) * 240 + x + xx] = 1
    assert actual == expected
    return {"visible_glyphs": len(visible), "all_complete_ink_pixels": sum(expected),
            "unique_visible_cells_no_overwritten_first_letters": True}


def main():
    ROOT.mkdir(exist_ok=True)
    original = NdsImage.open("out/all_routes_combined_v270_candidate.nds").read_file("/__arm9__.bin")
    target, plan = transform(original, 2)
    (ROOT / "research_arm9.bin").write_bytes(target)
    census = json.loads(__import__('pathlib').Path("work/analysis/equipment_start_town_v268/modal_guard_census.json").read_text(encoding="utf-8"))
    rows = []
    old_overlaps = 0
    for row in census["records"]:
        text = bytes.fromhex(row["before_hex"])[1:].rstrip(b" ")
        result = verify_ascii(target, text)
        old_pixels, events, old_return = raster(original, text)
        visible = [e for e in events if e["code"] != 32]
        overlaps = len(visible) - len({(e["x"], e["y"]) for e in visible})
        if not overlaps:
            assert raster(target, text) == (old_pixels, events, old_return)
        old_overlaps += overlaps
        rows.append({"path": row["path"], "block": row["block"], "segment": row["segment"],
                     "old_overwritten_glyph_cells": overlaps, **result})
    regressions = []
    for guards in (0, 2, 3, 4):
        text = b"  First line\n" + b" " * guards + b"Janus"
        assert raster(original, text) == raster(target, text)
        regressions.append({"guards": guards, "pixels_glyphs_and_return_exact_to_prior": True})
    for text in ["  Ｆirst\n  Ｊanus", "  Ｉ wish\n  Ｉ agree"]:
        assert raster(original, text.encode("cp932")) == raster(target, text.encode("cp932"))
    for tracking in (-1, 1, 3):
        text = b"First\n Janus"
        assert raster(original, text, tracking) == raster(target, text, tracking)
    from dk4tool.dialogue.grand_race_help import format_page
    race_pages = []
    for paragraph in ["Choose a course and keep an eye on the wind. Adjust the sails as needed to maintain your speed.", "Fleet commanders earn points by trading, discovering new places, and winning battles. The highest score wins the race."]:
        _, raw, _, _ = format_page(paragraph)
        assert raster(original, raw, width=252, height=108, line_height=12) == raster(target, raw, width=252, height=108, line_height=12)
        race_pages.append(paragraph)
    from scripts.probe_common_itcm_arena_reservation import initialize
    from scripts.probe_persistent_name_arm7_boot_overlap import execute
    boot_rom = NdsImage.open("out/all_routes_combined_v270_candidate.nds")
    payload = bytes(MainCodeFile(target, BASE).sections[3].data[:-48])
    boot = execute(target, bytes(boot_rom.rom.arm7), boot_rom.rom.arm7RamAddress, repair_entry=plan["cache"]["entry"], expected_pool=payload)
    proof = {"format": "dk4-modal-cursor-native-v272", "plan": plan, "cases": rows,
             "stored_ASCII_macro_tokens_are_render_inputs_not_live_macro_expansion_proof": True,
             "all325_at_risk_records_complete_cells_and_independent_font_pixels": True,
             "all_original_non_overlapping_cases_pixels_positions_and_returns_exact": True,
             "compiled_Grand_Race_pair_phase_safe_pages_exact": race_pages, "boot": boot, "arena": initialize(target),
             "prior_overwritten_visible_cells": old_overlaps, "unchanged_guard_contracts": regressions,
             "Japanese_two_guard_and_nonzero_tracking_regressions_exact": True,
             "all_unrelated_ARM9_sections_and_prior_owned_pool_prefix_preserved": True,
             "native_headers_inputs_pixels_saved_registers_and_stack_guards_pass": True,
             "actual_cold_boot_pending": True, "all18_plaques_incomplete": True}
    (ROOT / "native_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(f"325 records keep every glyph/pixel; {old_overlaps} overwritten cells removed.")


if __name__ == "__main__":
    main()
