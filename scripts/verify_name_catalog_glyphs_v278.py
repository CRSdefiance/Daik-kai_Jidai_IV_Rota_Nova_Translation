"""All expanded catalog bodies: real glyph painting and independent full pixels."""

import argparse
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.codec import parse_markup
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine
from scripts.research_online_loader_v190 import resource_call as call

ROOT = Path("work/analysis/name_macro_v278")
CATALOG = Path("work/analysis/name_catalog_v277")
WIDTH, HEIGHT = 216, 64


def raster(arm, text, *, canvas_height=HEIGHT):
    assert canvas_height in (64, 96)
    cpu = machine(arm)
    cpu.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    header, view, ctx, string = 0x02450000, 0x02453000, 0x02454000, 0x02455000
    size = WIDTH * canvas_height // 2
    raw_header = struct.pack("<5I", 4, WIDTH // 4, canvas_height, 0x02452000 - header, 20)
    cpu.mem_write(header - 16, b"\xA5" * (size + 52))
    cpu.mem_write(header, raw_header + bytes(size))
    call(cpu, 0xD3D80, (view,))
    cpu.mem_write(STACK, struct.pack("<4I", WIDTH, canvas_height, 0, 0))
    call(cpu, 0xD3AFC, (view, header, 0, 0))
    metrics = struct.unpack_from("<I", arm, 0xD5088)[0]
    cpu.mem_write(metrics + 4, struct.pack("<2I", 6, 16))
    font = NdsImage.open("work/clean.nds").read_file("/GRP/KANJI.FNT")
    cpu.mem_write(struct.unpack_from("<I", arm, 0xD19B8)[0], font)
    call(cpu, 0xD5160, (ctx, view, 1))
    cpu.mem_write(string - 16, b"\xA5" * (len(text) + 33))
    cpu.mem_write(string, text + b"\0")
    events = []

    def observe(uc, address, size, _):
        if address in (BASE + 0xD16B4, 0x01FF83AC):
            stack = uc.reg_read(UC_ARM_REG_SP)
            code, style = struct.unpack("<2I", uc.mem_read(stack, 8))
            events.append({"kind": "ascii" if address == BASE + 0xD16B4 else "cp932",
                           "code": code, "style": style, "x": uc.reg_read(UC_ARM_REG_R2),
                           "y": uc.reg_read(UC_ARM_REG_R3)})
    cpu.hook_add(UC_HOOK_CODE, observe)
    call(cpu, 0xD5404, (ctx, string))
    assert cpu.reg_read(UC_ARM_REG_R0) - string == len(text)
    assert bytes(cpu.mem_read(string, len(text) + 1)) == text + b"\0"
    assert bytes(cpu.mem_read(string - 16, 16)) == bytes(cpu.mem_read(string + len(text) + 1, 16)) == b"\xA5" * 16
    assert bytes(cpu.mem_read(header, 20)) == raw_header
    assert bytes(cpu.mem_read(header - 16, 16)) == bytes(cpu.mem_read(header + 20 + size, 16)) == b"\xA5" * 16
    pixels = bytes(n for b in cpu.mem_read(header + 20, size) for n in (b & 15, b >> 4))
    return pixels, events, font


def expected_pixels(arm, font, events, *, canvas_height=HEIGHT):
    glyphs = GameAsciiFont.from_arm9(arm)
    mapping = struct.unpack_from("<3340H", arm, 0x125EC4)
    canvas = bytearray(WIDTH * canvas_height)
    occupied = set()
    for event in events:
        x, y, code, style = [event[k] for k in ("x", "y", "code", "style")]
        width, height = (6, 11) if event["kind"] == "ascii" else (12, 12)
        if event["kind"] == "ascii":
            bitmap = glyphs.decode(chr(code))
            ink = [(xx, yy) for yy in range(11) for xx in range(6) if bitmap.getpixel((xx, yy))]
        else:
            assert code in mapping
            index = mapping.index(code)
            cell = font[index * 22:(index + 1) * 22]
            ink = [(xx, yy) for yy in range(11) for xx in range(11)
                   if cell[yy * 2 + xx // 8] & (0x80 >> (xx % 8))]
        if ink:
            assert 0 <= x <= WIDTH - width and 0 <= y <= canvas_height - height
            bounds = {(x + xx, y + yy) for yy in range(height) for xx in range(width)}
            assert not occupied & bounds, "Later visible glyph overlaps an earlier cell"
            occupied |= bounds
        for yy in range(height):
            for xx in range(width):
                if 0 <= x + xx < WIDTH and 0 <= y + yy < canvas_height:
                    canvas[(y + yy) * WIDTH + x + xx] = 0
        for xx, yy in ink:
            canvas[(y + yy) * WIDTH + x + xx] = style
        if event["kind"] == "cp932":
            shadow = 14 if style == 15 else 0 if 7 <= style <= 14 else 15
            for yy in range(11, 0, -1):
                for xx in range(11):
                    if canvas[(y + yy - 1) * WIDTH + x + xx] and not canvas[(y + yy) * WIDTH + x + xx + 1]:
                        canvas[(y + yy) * WIDTH + x + xx + 1] = shadow
    return bytes(canvas)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--macro-proof", type=Path, default=ROOT / "actual_player_macro_proof.json")
    parser.add_argument("--out", type=Path, default=ROOT)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    plan = json.loads((CATALOG / "catalog_plan.json").read_text(encoding="utf-8"))
    macro = json.loads(args.macro_proof.read_text(encoding="utf-8"))
    outputs = {r["key_hex"]: bytes.fromhex(r["output_hex"]) for r in macro["catalog_copy_cases"]}
    arm = (CATALOG / "catalog_research_only_arm9.bin").read_bytes()
    assert sha(arm) == plan["target_arm9_sha256"] == macro["ARM9_sha256"]
    cases, pictures = [], []
    failures = []
    for row in plan["prepared_records"]:
        text = outputs[row["current_key_hex"]]
        tokens = parse_markup(row["formatted_markup"])
        if tokens and tokens[0].kind == "speaker":
            text = text[1:]
        try:
            assert all(c >= 32 or c == 10 for c in text)
            pixels, events, font = raster(arm, text)
            expected = expected_pixels(arm, font, events)
            assert pixels == expected
            decoded = text.decode("cp932")
            semantic = [("ascii", ord(c)) if len(c.encode("cp932")) == 1 else
                        ("cp932", int.from_bytes(c.encode("cp932"), "big"))
                        for c in decoded if c not in " \n"]
            visible = [(e["kind"], e["code"]) for e in events if e["code"] != 32]
            assert visible == semantic
            lines = sorted({e["y"] for e in events if e["code"] != 32})
            assert lines == list(range(0, len(lines) * 16, 16)) and len(lines) <= 4
            image = Image.new("RGB", (WIDTH, HEIGHT))
            colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
            image.putdata([colors[value] for value in pixels])
            pictures.append((row["file_path"] + " " + row["id"], image.resize((WIDTH * 2, HEIGHT * 2), Image.Resampling.NEAREST)))
            cases.append({"file_path": row["file_path"], "id": row["id"], "expanded_text_hex": text.hex(),
                          "visible_glyphs": len(semantic), "native_ink_and_shadow_pixels": sum(bool(x) for x in pixels),
                          "all_visible_cells_distinct_and_independent_pixels_exact": True,
                          "first_and_final_glyph_complete": True, "lines": lines,
                          "blank_requests_clipped_by_native_view": sum(e["kind"] == "ascii" and e["code"] == 32 and
                              not (0 <= e["x"] <= WIDTH - 6 and 0 <= e["y"] <= HEIGHT - 11) for e in events),
                          "native_header_input_pixel_and_ABI_guards_pass": True})
        except (ValueError, AssertionError) as error:
            failures.append({"file_path": row["file_path"], "id": row["id"], "error": str(error)})
    sheets = []
    for start in range(0, len(pictures), 8):
        group = pictures[start:start + 8]
        sheet = Image.new("RGB", (WIDTH * 4, 4 * (HEIGHT * 2 + 26)), "#333333")
        draw = ImageDraw.Draw(sheet)
        for n, (label, image) in enumerate(group):
            x, y = n % 2 * WIDTH * 2, n // 2 * (HEIGHT * 2 + 26)
            draw.text((x + 3, y + 4), label, fill="white")
            sheet.paste(image, (x, y + 26))
        path = args.out / f"native_glyph_review_{start // 8:02d}.png"
        sheet.save(path)
        sheets.append(str(path))
    proof = {"format": "dk4-name-catalog-mixed-native-glyphs-v278", "ARM9_sha256": sha(arm), "cases": cases,
             "failures": failures, "sheets": sheets, "all76_complete_native_glyphs_verified": len(cases) == 76,
             "scope": "Actual immediate native ASCII/CP932 painting of expanded catalog bodies into a controlled216x64 bitmap; original progressive scenes remain unproved.",
             "editorial_and_visual_sheet_review_pending": True, "playable_ROM_modified": False, "full_goal_complete": False}
    (args.out / "native_glyph_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verified": len(cases), "failed": len(failures), "sheets": len(sheets)}))
    if failures:
        print(json.dumps(failures[:6]))


if __name__ == "__main__":
    main()
