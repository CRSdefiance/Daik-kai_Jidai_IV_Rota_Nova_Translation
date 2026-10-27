"""Check complete native name-widget glyphs from the isolated research ROM."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/emulation_v193/confirmed_name_widgets_v198")
ANALYSIS = Path("work/analysis/confirmed_names_v198")


def complete_mask(font, text, image, x, y, color):
    mask = Image.new("1", (len(text) * 6, 11))
    for index, character in enumerate(text):
        mask.paste(font.decode(character), (index * 6, 0))
    count = 0
    for row in range(11):
        for column in range(mask.width):
            ink = bool(mask.getpixel((column, row)))
            if (image.getpixel((x + column, y + row)) == color) != ink:
                raise ValueError("Complete native glyph/background mask differs")
            count += ink
    return count, [x, y, x + mask.width, y + 11]


def main():
    probe = json.loads((ANALYSIS / "widget_probe_manifest.json").read_text(encoding="utf-8"))
    source = NdsImage.open("out/all_routes_combined_v190_candidate.nds")
    research = NdsImage.open(probe["research_ROM"])
    before_font = GameAsciiFont.from_arm9(source.read_file("/__arm9__.bin"))
    font = GameAsciiFont.from_arm9(research.read_file("/__arm9__.bin"))
    assert font.glyphs == before_font.glyphs
    cases = []
    for name, text, frame, x, y, color in (
        ("rafael", "Rafael", 2100, 89, 220, (230, 230, 230)),
        ("hodram", "Joakim", 2100, 89, 242, (230, 230, 230)),
        ("camille", "Camille Overijssel", 4900, 16, 276, (98, 97, 98)),
    ):
        report_path = ROOT / name / "capture_report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["ROM_sha256"] == probe["research_ROM_sha256"]
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        path = ROOT / name / f"frame_{frame:06d}_final.png"
        capture = next(r for r in report["frames_captured"] if Path(r["path"]) == path)
        assert sha(path.read_bytes()) == capture["PNG_sha256"]
        image = Image.open(path).convert("RGB")
        count, bounds = complete_mask(font, text, image, x, y, color)
        assert 0 <= bounds[0] < bounds[2] <= 256 and 0 <= bounds[1] < bounds[3] <= 384
        cases.append({"name": text, "field": name, "frame": frame, "image": path.as_posix(),
                      "image_sha256": capture["PNG_sha256"], "glyph_bounds": bounds,
                      "exact_native_font_ink_pixels": count, "unexpected_foreground_pixels": 0,
                      "leading_and_trailing_glyphs_included": True, "visually_reviewed": True})
    maria_report = json.loads((ROOT / "maria" / "capture_report.json").read_text(encoding="utf-8"))
    assert not maria_report["callback_errors"] and maria_report["ROM_sha256"] == probe["research_ROM_sha256"]
    # The attempted third RIGHT selects Rafael. This failed navigation is not
    # evidence of Maria's intended surname/middle-name widgets or a general
    # assertion that Maria can never be selected.
    maria_image = ROOT / "maria" / "frame_002150_final.png"
    complete_mask(font, "Rafael", Image.open(maria_image).convert("RGB"), 89, 220, (230, 230, 230))
    report = {"format": "dk4-confirmed-name-widget-pixel-proof-v1",
              "research_ROM_sha256": probe["research_ROM_sha256"], "research_only": True,
              "cases": cases, "all_complete_lettering_masks_exact": True,
              "native_font_source_preserved": True,
              "Maria_attempt": {"reached_intended_character": False,
                                "observed_name": "Rafael", "image": maria_image.as_posix(),
                                "image_sha256": sha(maria_image.read_bytes()),
                                "remaining": "Determine legitimate selection/unlock/input path or execute a documented native Maria widget fixture."},
              "limits": "Changed-name widgets only. No release/patch, dialogue-macro migration, all temporal states or physical device acceptance is claimed.",
              "registered_playable_ROM_modified": False, "goal_complete": False}
    (ANALYSIS / "widget_pixels_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"exact_widget_cases": len(cases), "exact_ink_pixels": sum(r["exact_native_font_ink_pixels"] for r in cases),
                      "Maria_target_not_reached": True, "research_only": True}))


if __name__ == "__main__":
    main()
