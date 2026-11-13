"""Verify the actual English notice, unchanged palette and other frame pixels."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call
from scripts.verify_original_latin_cards_native_v197 import native5
from scripts.verify_sailing_panel_packing_v215 import read_pixel
from scripts.verify_sailing_panels_v217 import make_machine

ROOT = Path("work/analysis/no_target_v218")
CAPTURE = Path("work/emulation_v193/no_target_v218")
PRIOR = Path("work/emulation_v193/sailing_panels_v217")
ROM = Path("out/all_routes_combined_v218_candidate.nds")


def frame(report, number):
    item = next(row for row in report["frames_captured"] if row["frame"] == number)
    path = Path(item["path"])
    assert sha(path.read_bytes()) == item["PNG_sha256"]
    with Image.open(path) as im:
        result = im.convert("RGB")
    return result, item


def mask(font, glyphs):
    ink = set()
    for g in glyphs:
        cell = font.decode(g["character"])
        x0, y0 = g["origin"]
        for y in range(11):
            for x in range(6):
                if cell.getpixel((x, y)):
                    ink.add((x0 + x, y0 + y))
    return ink


def main():
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    old_report = json.loads((PRIOR / "capture_report.json").read_text(encoding="utf-8"))
    plan = json.loads((ROOT / "preparation.json").read_text(encoding="utf-8"))
    current = NdsImage.open(ROM)
    assert report["ROM_sha256"] == sha(ROM.read_bytes()) and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    assert sha(current.read_file("/__arm9__.bin")) == plan["target_arm9_sha256"]
    prior_rom = NdsImage.open("out/all_routes_combined_v217_candidate.nds")
    assert old_report["ROM_sha256"] == sha(prior_rom.source.read_bytes())
    actual, notice_frame = frame(report, 18400)
    original, original_frame = frame(old_report, 18400)
    # Establish the color from original producer pixels and the original real frame.
    u = make_machine(prior_rom.read_file("/__arm9__.bin"), prior_rom)
    buffer = 0x02460020
    u.mem_write(buffer, bytes(0x1000))
    call(u, 0x01FFB4BC - 0x02000000, (0x02147F34, 1, buffer))
    raw = bytes(u.mem_read(buffer, 0x600))
    original_ink = {(96 + x, 272 + row * 16 + y) for row in range(2) for y in range(16) for x in range(96)
                    if read_pixel(raw, row * 96 + x, y) == 1}
    colors = {native5(original.getpixel(point)) for point in original_ink}
    assert len(colors) == 1 and len(original_ink) == 554
    foreground = colors.pop()
    font = GameAsciiFont.from_arm9(current.read_file("/__arm9__.bin"))
    expected = mask(font, plan["panel"]["glyphs"])
    region = {(x, y) for y in range(272, 304) for x in range(80, 208)}
    observed = {p for p in region if native5(actual.getpixel(p)) == foreground}
    assert observed == expected, (len(expected - observed), len(observed - expected), foreground)
    # Byte-identical pixels outside the changed notice region catch unrelated
    # clock/control damage from sprite uploads, not just text-region success.
    outside = [(x, y) for y in range(384) for x in range(256) if (x, y) not in region]
    assert all(actual.getpixel(p) == original.getpixel(p) for p in outside)
    inherited_plan = json.loads(Path("work/analysis/sailing_panels_v217/preparation.json").read_text(encoding="utf-8"))
    inherited = []
    for number, panel_index in ((17400, 0), (17900, 1), (18400, 2), (18900, 0)):
        im, item = frame(report, number)
        expected_top = mask(font, inherited_plan["panels"][panel_index]["glyphs"])
        observed_top = {(x, y) for y in range(176) for x in range(256)
                        if native5(im.getpixel((x, y))) == (31, 31, 31)}
        assert expected_top == observed_top
        inherited.append({"capture": item, "exact_foreground_and_blank_pixels": 256 * 176,
                          "all_first_last_glyphs_and_punctuation_exact": True})
    result = {"format": "dk4-no-target-cold-boot-pixel-proof-v1", "ROM": ROM.as_posix(),
              "ROM_sha256": sha(ROM.read_bytes()), "notice_capture": notice_frame,
              "original_source_capture": original_frame, "complete_English": plan["panel"]["english"],
              "automatic_lines": plan["panel"]["lines"], "original_foreground_native5": list(foreground),
              "original_Japanese_native_ink_pixels_verified": len(original_ink),
              "exact_notice_foreground_and_blank_pixels": len(region), "exact_English_ink_pixels": len(expected),
              "all_other_frame_pixels_identical_to_V217": len(outside),
              "notice_first_last_letters_punctuation_and_bounds_complete": True,
              "no_Japanese_or_old_glyph_remnants_in_notice_region": True,
              "no_footer_overlap_or_prior_sprite_damage": True, "inherited_sailing_panels": inherited,
              "cold_boot_without_savestate_or_RAM_injection": True,
              "hardware_device_verification": False, "visual_review_complete": False,
              "full_goal_complete": False}
    (ROOT / "live_pixels.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"English_notice_ink_pixels": len(expected), "exact_notice_cells": len(region),
                      "unchanged_other_frame_pixels": len(outside), "inherited_panel_captures": len(inherited)}))


if __name__ == "__main__":
    main()
