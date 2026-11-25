"""Execute all village paragraphs against the actual captured portrait sprite."""

import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE, call, machine

ROOT = Path("work/analysis/village_wrap_v608")
CAP = Path("E:/Rota Nova translations/Generated/work/emulation_v193/village_wrap_v608_inuvik")
VT, WIDTH, HEIGHT, SIZE = 0x021438A0, 288, 48, 6912


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    arm = (ROOT / "research_arm9.bin").read_bytes()
    transform = read(ROOT / "transform_proof.json")
    assert sha(arm) == transform["target_arm9_sha256"]
    raw_path = CAP / "frame_007800_arm9_ram.bin"
    raw = raw_path.read_bytes()
    native_path = CAP / "native_state_007800/native_state.json"
    native = read(native_path)
    io_path, vram_path = [Path(native["regions"][tag]["path"]) for tag in ("9REG", "LCDM")]
    for path, tag in ((io_path, "9REG"), (vram_path, "LCDM")):
        assert sha(path.read_bytes()) == native["regions"][tag]["sha256"]
    io, vram = io_path.read_bytes(), vram_path.read_bytes()
    assert io[0x243] == 0x81  # Native bank D: main BG, offset zero.
    candidates = [o for o in range(0x170000, len(raw) - 0x90, 4)
                  if struct.unpack_from("<I", raw, o)[0] == VT]
    assert len(candidates) == 1
    offset = candidates[0]
    parent = offset + BASE
    assert struct.unpack_from("<6I", raw, offset + 0x28) == (228, 48, 0, 0, 228, 48)
    header = struct.unpack_from("<I", raw, offset + 0x10)[0]
    flags, words, height, palette_delta, pixels_delta = struct.unpack_from("<5I", raw, header - BASE)
    assert (flags, words, height) == (4, 72, HEIGHT)
    palette = header + (palette_delta if palette_delta < 0x80000000 else palette_delta - 0x100000000)
    pixels = header + pixels_delta
    assert pixels == 0x0601A000 and palette == 0x02125A20
    captured_plane = vram[0x60000 + pixels - 0x06000000:0x60000 + pixels - 0x06000000 + SIZE]
    assert len(captured_plane) == SIZE
    font = GameAsciiFont.from_arm9(arm)
    u = machine(arm)
    u.mem_write(BASE, raw)
    u.mem_map(0x06000000, 0x20000)
    u.mem_write(0x06000000, vram[0x60000:0x80000])
    header_before = bytes(u.mem_read(header, 20))
    palette_before = bytes(u.mem_read(palette, 32))
    glyphs = []

    def trace(uc, address, size, data):
        if address == BASE + 0xD16B4:
            code, style = struct.unpack("<2I", uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
            glyphs.append({"code": code, "style": style,
                           "x": uc.reg_read(UC_ARM_REG_R2), "y": uc.reg_read(UC_ARM_REG_R3)})

    hook = u.hook_add(UC_HOOK_CODE, trace)
    cases = []
    sheet = Image.new("RGB", (2 * 720, 14 * 170), (35, 45, 50))
    painter = ImageDraw.Draw(sheet)
    try:
        for index, row in enumerate(transform["compiled_contexts"]):
            text = row["compiled_expanded"]
            pointer = struct.unpack_from("<I", raw, row["field"])[0]
            assert pointer == row["target_pointer"]
            encoded = bytes.fromhex(row["compiled_hex"])
            assert raw[pointer - BASE:pointer - BASE + len(encoded) + 1] == encoded + b"\0"
            # The observed owners still select the compiled source text. Clues
            # are expanded with their unchanged literal prefix/template suffix.
            selected = encoded.decode("ascii")
            if row["id"].startswith("VILLAGE_CLUE_"):
                selected = "They say it means " + selected + "."
            assert selected == text
            u.mem_write(pixels, bytes(SIZE))
            u.mem_write(pixels - 16, b"\xA5" * 16)
            u.mem_write(pixels + SIZE, b"\xA5" * 16)
            u.mem_write(0x02440000, text.encode("ascii") + b"\0")
            glyphs.clear()
            executed = call(u, 0x548A8, (parent, 0x02440000), instruction_limit=1000000)
            assert {0x020548A8, 0x020D5160, 0x020D5404, 0x020D16B4, 0x020D5140} <= executed
            assert 0x02054E44 not in executed  # No page overflow/input wait.
            content = [g for g in glyphs if g["code"] != 32]
            expected_codes = [ord(c) for c in row["full_expanded_paragraph"] if c != " "]
            assert [g["code"] for g in content] == expected_codes
            cursor = 0
            for word in row["full_expanded_paragraph"].split():
                events = content[cursor:cursor + len(word)]
                assert len({g["y"] for g in events}) == 1, (row["id"], word)
                cursor += len(word)
            expected = bytearray(WIDTH * HEIGHT)
            for glyph in glyphs:
                assert glyph["style"] == 15
                x, y = glyph["x"], glyph["y"]
                assert 0 <= x <= 222 and 0 <= y <= HEIGHT - 11
                mask = font.decode(chr(glyph["code"]))
                for yy in range(11):
                    for xx in range(6):
                        if mask.getpixel((xx, yy)):
                            expected[(y + yy) * WIDTH + x + xx] = 15
            packed = bytes(expected[i] | expected[i + 1] << 4 for i in range(0, len(expected), 2))
            assert bytes(u.mem_read(pixels, SIZE)) == packed
            assert bytes(u.mem_read(pixels - 16, 16)) == bytes(u.mem_read(pixels + SIZE, 16)) == b"\xA5" * 16
            assert bytes(u.mem_read(header, 20)) == header_before and bytes(u.mem_read(palette, 32)) == palette_before
            rows = sorted({g["y"] for g in content})
            assert max(rows) <= 24  # All current paragraphs need at most three stored rows.
            if row["id"] == "VILLAGE_MESSAGE_0":
                assert packed == captured_plane  # Binds this exact sprite to the real scene.
                captured_binding = {"whole_captured_VRAM_plane_bytes_exact": SIZE, "glyphs": list(glyphs)}
            case = {"id": row["id"], "compiled": text, "complete_glyphs_including_first_final": len(content),
                    "all_words_on_single_rows": True, "stored_row_origins": rows,
                    "whole_native_plane_bytes": SIZE, "plane_sha256": sha(packed),
                    "no_page_overflow": True, "independent_font_pixels_and_header_palette_guards_exact": True}
            cases.append(case)
            preview = Image.new("RGB", (WIDTH, HEIGHT), (225, 218, 190))
            preview.putdata([(0, 8, 0) if v else (225, 218, 190) for v in expected])
            x, y = index % 2 * 720, index // 2 * 170
            painter.text((x + 8, y + 4), row["id"], fill="white")
            preview = preview.crop((0, 0, 228, 48)).resize((684, 144), Image.Resampling.NEAREST)
            sheet.paste(preview, (x + 8, y + 22))
    finally:
        u.hook_del(hook)
    assert len(cases) == 28
    sheet.save(ROOT / "all28_actual_canvas_previews.png")
    proof = {"research_ARM9_sha256": sha(arm), "script_sha256": sha(Path(__file__).read_bytes()),
        "actual_sprite_parent": parent, "actual_vtable": VT, "actual_client": [228, 48],
        "actual_storage": [288, 48, 4], "actual_pixels": pixels, "actual_palette": palette,
        "native_bank_D_control": io[0x243], "actual_scene_binding": captured_binding,
        "stored_rows_are12_pixels_physical_dialog_rows_are16_pixels": True,
        "all28_contexts": cases, "whole_replayed_canvas_bytes": SIZE * len(cases),
        "captured_RAM": str(raw_path), "captured_RAM_sha256": sha(raw),
        "native_state": str(native_path), "native_state_sha256": sha(native_path.read_bytes()),
        "all28_ordinary_event_screens_claimed": False, "transparent_canvas_reset_is_replay_contract": True,
        "renderer_fonts_or_results_bridged": False, "full_goal_complete": False}
    save(ROOT / "actual_canvas_proof.json", proof)
    print("V608 actual sprite:28 complete native canvases/193536 bytes;all words and letters fit;6912-byte captured scene binding exact.")


if __name__ == "__main__":
    main()
