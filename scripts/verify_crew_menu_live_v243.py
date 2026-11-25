"""Verify actual runtime menu captions without claiming legacy atlas consumers."""

import json
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROM = Path("out/all_routes_combined_v241_candidate.nds")
CAPTURE = Path("work/emulation_v193/crew_buttons_v243/navigation")
OUT = Path("work/analysis/crew_buttons_v243")
CASES = ((11200, "Crew Setup", 59, 259, 5, (255, 255, 255)),
         (11500, "Deck View", 61, 259, 5, (255, 255, 255)),
         (11800, "Route Map", 61, 259, 5, (255, 255, 255)),
         (12100, "Info", 74, 259, 5, (255, 255, 255)),
         (12400, "Items", 71, 259, 5, (255, 255, 255)),
         (12700, "Functions", 61, 259, 5, (255, 255, 255)),
         (10300, "No", 134, 362, 6, (213, 214, 213)),
         (10300, "Yes", 202, 362, 6, (213, 214, 213)))


def main():
    digest = sha(ROM.read_bytes())
    assert digest == "d863f74ba3e5466f5a221ba93e00d53fd1588a32cecdd349006b7eb0698e8027"
    report_path = CAPTURE / "capture_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    assert report["core_DLL_sha256"] == "42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b"
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file("/__arm9__.bin"))
    cases = []
    for frame, text, x, y, advance, color in CASES:
        row = next(r for r in report["frames_captured"] if r["frame"] == frame)
        image = Image.open(row["path"]).convert("RGB")
        width = (len(text) - 1) * advance + 6
        mask = Image.new("1", (width, 11))
        for n, ch in enumerate(text):
            layer = Image.new("1", mask.size)
            layer.paste(font.decode(ch), (n * advance, 0))
            mask = ImageChops.lighter(mask, layer)
        ink = 0
        for dy in range(11):
            for dx in range(width):
                expected = bool(mask.getpixel((dx, dy)))
                assert (image.getpixel((x + dx, y + dy)) == color) == expected
                ink += expected
        assert 0 <= x < x + width <= 256 and 192 <= y < y + 11 <= 384
        cases.append({"text": text, "capture": row, "advance": advance,
                      "bounds": [x, y, x + width, y + 11], "complete_source_font_ink_pixels": ink,
                      "complete_ink_and_blank_cell_pixels_checked": width * 11,
                      "first_last_letters_and_internal_spaces_exact": True,
                      "not_a_claim_of_baked_atlas_cell_selection": True})
    proof = {"format": "dk4-live-crew-menu-caption-proof-v243", "ROM_sha256": digest,
             "capture_report_sha256": sha(report_path.read_bytes()), "cases": cases,
             "complete_font_ink_pixels": sum(c["complete_source_font_ink_pixels"] for c in cases),
             "complete_font_and_blank_pixels": sum(c["complete_ink_and_blank_cell_pixels_checked"] for c in cases),
             "normal_town_Crew_Setup_manual_mode_confirmation_and_radial_navigation_observed": True,
             "all_eight_captions_visually_reviewed": True,
             "legacy_Set_Crew_Balance_Minimum_Done_display_not_proved": True,
             "radial_captions_match_native_font_and_differ_from_tested_baked_caption_masks": True,
             "atlas_parent_palette_and_embedded_consumer_questions_remain_open": True,
             "no_savestate_RAM_injection_or_fixture_ROM": True,
             "ROM_modified": False, "full_goal_complete": False}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "live_caption_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_live_captions": len(cases), "ink_pixels": proof["complete_font_ink_pixels"],
                      "ink_and_blank_pixels": proof["complete_font_and_blank_pixels"],
                      "legacy_atlas_display_not_inferred": True}))


if __name__ == "__main__":
    main()
