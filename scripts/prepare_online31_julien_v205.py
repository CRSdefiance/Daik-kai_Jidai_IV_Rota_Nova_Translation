"""Prepare one clear screenshot name; leave uncertain dialogue/chat unchanged."""

import json
import zlib
from pathlib import Path

from PIL import Image

from dk4tool.graphics.compact_font import GLYPHS
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.online27_bubbles_v177 import nearest

ROOT = Path("work/analysis/online31_julien_v205")
QA = Path("work/qa/online31_julien_v205")
RESOURCE = "/_pxl/online/Online31.pxl"
BOX = (36, 105, 61, 112)
NAME_GLYPHS = {letter: GLYPHS[letter] for letter in "lien"}
NAME_GLYPHS.update({"J": ("0011", "0001", "0001", "0001", "0001", "1001", "0110"),
                    "u": ("000", "000", "101", "101", "101", "101", "011")})


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file(RESOURCE)
    assert sha(source) == "e583731cc70adf5334b9208924df6f9c49742b93c2632208bb84633ffe3a17de"
    image = PxlImage.from_bytes(source)
    original = bytes(image.indices)
    x0, y0, x1, y1 = BOX
    mask = Image.new("L", (x1 - x0, y1 - y0))
    cursor, origins = 0, []
    for letter in "Julien":
        rows = NAME_GLYPHS[letter]
        assert len(rows) == 7 and all(len(row) == len(rows[0]) and set(row) <= {"0", "1"} for row in rows)
        origins.append({"letter": letter, "x": x0 + cursor, "y": y0, "width": len(rows[0]), "height": 7})
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                assert cursor + x < mask.width
                mask.putpixel((cursor + x, y), 255 if value == "1" else 0)
        cursor += len(rows[0]) + 1
    used = [image.palette[original[y * image.width + x]][:3] for y in range(y0, y1) for x in range(x0, x1)]
    blues = [c for c in used if c[2] > c[0] + 15 and c[1] > c[0] + 15]
    assert blues
    foreground = max(blues, key=sum)
    for y in range(y0, y1):
        # The name sits in a composited translucent panel. Same-row text-free
        # donors estimate only the newly owned name rectangle's background.
        donor = image.palette[original[y * image.width + 64]][:3]
        for x in range(x0, x1):
            alpha = mask.getpixel((x - x0, y - y0))
            color = tuple((a * alpha + b * (255 - alpha) + 127) // 255 for a, b in zip(foreground, donor, strict=True))
            image.indices[y * image.width + x] = nearest(image.palette, color)
    result = image.to_bytes()
    assert len(result) == len(source) and result[:image.pixels_offset] == source[:image.pixels_offset]
    assert all(a == b for k, (a, b) in enumerate(zip(original, image.indices, strict=True))
               if not x0 <= k % image.width < x1 or not y0 <= k // image.width < y1)
    pixels = bytes(image.indices[y * image.width + x] for y in range(y0, y1) for x in range(x0, x1))
    batch = {"format": "dk4-pxl-indexed-region-batch-v1", "file_path": RESOURCE,
             "target_locale": "en-US", "editorial_policy": "natural-dialogue-v2",
             "source_file_sha256": sha(source), "description": "Source-backed Online NPC name only; full screenshot dialogue/chat remains pending.",
             "records": [{"id": "DK4_ONLINE31_JULIEN_NAME_V1", "box": list(BOX),
                          "source_region_sha256": sha(bytes(original[y * image.width + x] for y in range(y0, y1) for x in range(x0, x1))),
                          "indices_zlib_hex": zlib.compress(pixels, 9).hex(), "indices_sha256": sha(pixels),
                          "source_japanese": "ジュリアン", "english": "Julien",
                          "source_meaning": "The speaking Online NPC's name.",
                          "localization_note": "Use the official English Online localization's Julien for the source ジュリアン. This is distinct from DK4's Julian crew name; no dialogue/location is inferred.",
                          "primary_Japanese_name": "https://www.gamecity.ne.jp/dol/topics_cms/update/9787.html",
                          "primary_English_name": "https://uwo.papayaplay.com/uwo.do?tp=lost_memories",
                          "source_scope": "Later official Online episodes support NPC naming, not this historical screenshot's unreadable sentence.",
                          "background_recovery": "Same-row donor at x64; estimate inside owned name rectangle only."}]}
    path = Path("translations/online31_julien_name_art_v1.json")
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "prepared_Online31.pxl").write_bytes(result)
    image.render().save(QA / "translated_preview.png")
    with Image.open(QA / "translated_preview.png") as im:
        im.resize((1024, 768), Image.Resampling.NEAREST).save(QA / "translated_preview_4x.png")
    proof = {"format": "dk4-Online31-name-preparation-v1", "source_sha256": sha(source), "target_sha256": sha(result),
             "box": list(BOX), "English": "Julien", "foreground_from_original_name_palette": list(foreground),
             "font_face": "compact-name-7px-research-v1", "glyphs": NAME_GLYPHS,
             "font_sha256": sha(json.dumps(NAME_GLYPHS, sort_keys=True).encode("ascii")), "glyph_origins": origins,
             "mask_bbox": list(mask.getbbox()), "all_headers_palette_dimensions_unowned_indices_exact": True,
             "complete_seven_row_glyphs_without_resampling_or_clipping": True,
             "background_inside_owned_box_estimated": True, "body_and_chat_translation_pending": True,
             "visual_and_native_review_pending": True, "batch_not_registered": path.as_posix(), "goal_complete": False}
    (ROOT / "preparation.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"name": "Julien", "box": list(BOX), "font_mask_bbox": proof["mask_bbox"], "all_unowned_pixels_preserved": True}))


if __name__ == "__main__":
    main()
