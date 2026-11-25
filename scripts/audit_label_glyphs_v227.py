"""Check full source-font ink against actual ROM label pixels, including edge glyphs."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.compact_font import glyph as compact_glyph
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/label_glyphs_v227")


def main():
    rom = NdsImage.open("out/all_routes_combined_v218_candidate.nds")
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    cases = []
    ROOT.mkdir(parents=True, exist_ok=True)
    for name in stack["profiles"]["all-routes-unified-v218"]["batches"]:
        batch = json.loads(Path(name).read_text(encoding="utf-8"))
        if batch.get("format") != "dk4-pxl-native-label-batch-v1":
            continue
        image = PxlImage.from_bytes(rom.read_file(batch["file_path"]))
        for record in batch["records"]:
            text = record["text"]
            left, top, right, bottom = record.get("draw_box", record["box"])
            face = record.get("font_face", "native-ascii")
            compact = face != "native-ascii"
            spacing = record.get("glyph_spacing", "fixed")
            trim = batch.get("trim_blank_top_rows", 0) if not compact else 0
            cells, offsets, cursor = [], [], 0
            for character in text:
                if compact:
                    word_width = record.get("compact_word_space_width", 2)
                    cell = Image.new("1", (word_width, 7)) if character == " " else compact_glyph(character, font_face=face)
                    offset = cursor
                    cursor += cell.width + 1
                else:
                    cell = font.decode(character)
                    assert not cell.crop((0, 0, 6, trim)).getbbox() if trim else True
                    bounds = cell.getbbox()
                    if spacing == "native-ink-v1":
                        offset = cursor - bounds[0] if bounds else cursor
                        cursor += bounds[2] - bounds[0] + 1 if bounds else 3
                    else:
                        offset = cursor
                        cursor += batch.get("advance", batch.get("glyph_width", 5))
                    cell = cell.crop((0, trim, 6, 11))
                cells.append(cell)
                offsets.append(offset)
            width = cursor - 1 if compact else cursor
            height = 7 if compact else 11 - trim
            x0, y0 = left + (right - left - width) // 2, top + (bottom - top - height) // 2
            color = record.get("color_index", batch.get("color_index", 1))
            expected = set()
            glyphs = []
            for character, offset, cell in zip(text, offsets, cells, strict=True):
                ink = {(x0 + offset + x, y0 + y) for y in range(cell.height) for x in range(cell.width) if cell.getpixel((x, y))}
                assert all(left <= x < right and top <= y < bottom for x, y in ink)
                assert all(image.indices[y * image.width + x] == color for x, y in ink), record["id"]
                expected |= ink
                glyphs.append({"character": character, "full_source_glyph_ink": len(ink), "origin": [x0 + offset, y0],
                               "complete_source_ink_inside_draw_box_and_present": True})
            observed = {(x, y) for y in range(y0, y0 + height) for x in range(x0, x0 + width)
                        if image.indices[y * image.width + x] == color}
            assert observed == expected, (record["id"], len(expected - observed), len(observed - expected))
            crop = image.render().crop((x0, y0, x0 + width, y0 + height))
            path = ROOT / (record["id"] + ".png")
            crop.save(path)
            cases.append({"id": record["id"], "batch": name, "file": batch["file_path"], "text": text,
                          "font_face": face, "draw_box": [left, top, right, bottom], "glyphs": glyphs,
                          "all_foreground_and_blank_text_pixels_exact": width * height,
                          "first_and_last_glyph_complete": True, "no_extra_source_letter_ink_in_text_extent": True,
                          "preview": path.as_posix(), "preview_sha256": sha(path.read_bytes())})
    assert len(cases) == 57
    sheet = Image.new("RGB", (600, 20 * 66), "white")
    draw = ImageDraw.Draw(sheet)
    for n, row in enumerate(cases):
        x, y = n % 3 * 200, n // 3 * 66
        with Image.open(row["preview"]) as preview:
            sheet.paste(preview.convert("RGB"), (x, y + 20))
        draw.text((x, y), row["text"], fill="black")
    sheet.save(ROOT / "all57_labels.png")
    report = {"format": "dk4-native-compact-label-complete-ink-proof-v1", "ROM_sha256": sha(rom.source.read_bytes()),
              "source_font_sha256": sha(font.glyphs), "cases": cases,
              "complete_leading_trailing_glyph_ink_verified": True,
              "native_GPU_crop_alpha_and_gameplay_not_inferred_from_ROM_pixels": True,
              "visual_review_complete": False, "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "glyph_proof.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_labels": len(cases), "first_last_letters_and_all_source_ink_pass": True,
                      "exact_foreground_and_blank_pixels": sum(x["all_foreground_and_blank_text_pixels_exact"] for x in cases)}))


if __name__ == "__main__":
    main()
