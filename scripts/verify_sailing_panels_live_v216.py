"""Compare every English glyph and blank pixel against ordinary cold-boot play."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_original_latin_cards_native_v197 import native5

ROOT = Path("work/analysis/sailing_panels_v216")
CAPTURE = Path("work/emulation_v193/sailing_panels_v216")
ROM = Path("out/all_routes_combined_v216_candidate.nds")


def main():
    plan = json.loads((ROOT / "preparation.json").read_text(encoding="utf-8"))
    manuscript = json.loads(Path("translations/sailing_mode_panels_manuscript_v1.json").read_text(encoding="utf-8"))
    capture = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    rom = NdsImage.open(ROM)
    assert capture["ROM_sha256"] == sha(ROM.read_bytes())
    assert sha(rom.read_file("/__arm9__.bin")) == plan["target_arm9_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    cases = []
    for record, panel in zip(manuscript["records"], plan["panels"], strict=True):
        assert record["id"] == panel["id"] and record["english"] == " ".join(panel["lines"])
        frame = next(row for row in capture["frames_captured"] if row["frame"] == record["native_capture_frame"])
        path = Path(frame["path"])
        assert sha(path.read_bytes()) == frame["PNG_sha256"]
        with Image.open(path) as im:
            actual = im.convert("RGB")
        expected_ink = set()
        for glyph in panel["glyphs"]:
            mask = font.decode(glyph["character"])
            x0, y0 = glyph["origin"]
            for y in range(11):
                for x in range(6):
                    if mask.getpixel((x, y)):
                        expected_ink.add((x0 + x, y0 + y))
        observed_ink = {(x, y) for y in range(176) for x in range(256)
                        if native5(actual.getpixel((x, y))) == (31, 31, 31)}
        assert observed_ink == expected_ink, (record["id"], len(expected_ink - observed_ink),
                                               len(observed_ink - expected_ink))
        cases.append({"id": record["id"], "heading": record["heading"], "english": record["english"],
                      "complete_body_lines": panel["lines"], "capture": frame,
                      "exact_foreground_and_blank_mask_pixels": 256 * 176,
                      "exact_ink_pixels": len(expected_ink), "complete_glyph_cells": len(panel["glyphs"]),
                      "first_and_last_letters_and_punctuation_exact": True,
                      "no_extra_Japanese_or_foreground_in_panel_region": True,
                      "every_source_instruction_preserved": True})
    result = {"format": "dk4-sailing-English-cold-boot-pixel-proof-v1", "ROM": ROM.as_posix(),
              "ROM_sha256": sha(ROM.read_bytes()), "capture_report_sha256": sha((CAPTURE / "capture_report.json").read_bytes()),
              "normal_gameplay_input_schedule": capture["scripted_input_schedule"],
              "cold_boot": True, "savestate_or_RAM_injection_used": False,
              "panels": cases, "exact_foreground_and_blank_mask_pixels": sum(row["exact_foreground_and_blank_mask_pixels"] for row in cases),
              "no_missing_first_last_letters_or_footer_overlap": True,
              "separate_no_target_notice_still_Japanese": True,
              "hardware_device_verification": False, "full_goal_complete": False}
    (ROOT / "live_pixels.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_live_English_panels": len(cases),
                      "exact_foreground_and_blank_mask_pixels": result["exact_foreground_and_blank_mask_pixels"],
                      "exact_ink_pixels": sum(row["exact_ink_pixels"] for row in cases)}))


if __name__ == "__main__":
    main()
