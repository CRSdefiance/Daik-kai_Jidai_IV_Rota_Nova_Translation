"""Prepare complete English bitmap layouts; physical native packing stays gated."""

import json
import textwrap
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/sailing_panel_overlay_v214")


def main():
    manuscript = json.loads(Path("translations/sailing_mode_panels_manuscript_v1.json").read_text(encoding="utf-8"))
    rom = NdsImage.open("out/all_routes_combined_v211_candidate.nds")
    assert sha(rom.source.read_bytes()) == manuscript["candidate_source_sha256"]
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    rows = []
    for record in manuscript["records"]:
        lines = textwrap.wrap(record["english"], width=40, break_long_words=False, break_on_hyphens=False)
        assert " ".join(lines) == record["english"]
        assert 32 + (len(lines) - 1) * 16 + 11 <= 176
        image = Image.new("P", (256, 192), 0)
        image.putpalette([c for n in range(256) for c in ((0, 0, 0) if n == 0 else (255, 255, 255))])
        glyphs = []
        for line, text in enumerate([record["heading"]] + lines):
            x0 = (256 - len(text) * 6) // 2 if line == 0 else 8
            y0 = 0 if line == 0 else 32 + (line - 1) * 16
            for position, char in enumerate(text):
                mask = font.decode(char)
                assert 0 <= x0 + position * 6 <= x0 + position * 6 + 6 <= 256
                assert y0 + 11 <= 176
                ink = 0
                for y in range(11):
                    for x in range(6):
                        if mask.getpixel((x, y)):
                            image.putpixel((x0 + position * 6 + x, y0 + y), 15)
                            ink += 1
                glyphs.append({"line": line, "position": position, "character": char,
                               "origin": [x0 + position * 6, y0], "complete_cells": [6, 11], "ink_pixels": ink})
        path = ROOT / (record["id"].lower() + "_English_layout.png")
        image.save(path)
        rows.append({"id": record["id"], "heading": record["heading"], "logical_prose": record["english"],
                     "automatic_body_lines": lines, "complete_words_preserved": True,
                     "glyphs": glyphs, "all_first_last_glyphs_and_extents_inside_proposed_canvas": True,
                     "bitmap_dimensions": [256, 192], "reserved_footer_start": 176,
                     "preview": path.as_posix(), "preview_sha256": sha(path.read_bytes()),
                     "pixel_indices_sha256": sha(image.tobytes()), "visual_review": "pending",
                     "native_packing_and_callback_not_verified": True})
    result = {"format": "dk4-sailing-English-layout-preparation-v1", "ROM_sha256": manuscript["candidate_source_sha256"],
              "font_sha256": sha(font.glyphs), "records": rows,
              "original_producer_is_not_plain_ASCII_compatible": True,
              "these_previews_are_not_a_native_research_ROM_or_release": True,
              "formatting_gate_still_pending_native_pack_and_display": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "English_layouts.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_English_layouts": len(rows), "body_line_counts": [len(r["automatic_body_lines"]) for r in rows],
                      "no_words_or_instructions_dropped": True, "native_integration_pending": True}))


if __name__ == "__main__":
    main()
