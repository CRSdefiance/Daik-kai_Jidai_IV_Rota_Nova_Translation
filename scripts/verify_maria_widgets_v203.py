"""Verify complete Maria portrait and name fields in the explicit selection fixture."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROOT = Path("work/analysis/maria_widgets_v203")
CAPTURE = Path("work/emulation_v193/maria_widgets_v203")


def main():
    manifest = json.loads((ROOT / "fixture_manifest.json").read_text(encoding="utf-8"))
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == manifest["research_ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    rom_path = Path(manifest["research_ROM"])
    assert sha(rom_path.read_bytes()) == manifest["research_ROM_sha256"]
    rom = NdsImage.open(rom_path)
    source = NdsImage.open(manifest["source_ROM"])
    path = CAPTURE / "frame_002300_final.png"
    capture = next(row for row in report["frames_captured"] if Path(row["path"]) == path)
    assert sha(path.read_bytes()) == capture["PNG_sha256"]
    with Image.open(path) as im:
        image = im.convert("RGB")
    resource = "/_pxl/personbustup03.pxl"
    raw = rom.read_file(resource)
    assert raw == source.read_file(resource)
    portrait = PxlImage.from_bytes(raw).render()
    assert portrait.size == (104, 136)
    for y in range(136):
        for x in range(104):
            assert native5(portrait.getpixel((x, y))) == native5(image.getpixel((76 + x, 28 + y))), (x, y)
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    assert font.glyphs == GameAsciiFont.from_arm9(source.read_file("/__arm9__.bin")).glyphs
    fields = []
    for label, text, y in (("given", "Maria", 220), ("middle", "Huamei", 242),
                           ("surname", "Li", 264), ("company", "Li Clan", 286)):
        count, bounds = complete_mask(font, text, image, 89, y, (230, 230, 230))
        assert 0 <= bounds[0] < bounds[2] <= 256 and 0 <= bounds[1] < bounds[3] <= 384
        fields.append({"field": label, "text": text, "bounds": bounds,
                       "complete_native_font_ink_pixels": count, "all_ink_and_blank_cells_exact": True,
                       "first_and_last_letters_included": True})
    proof = {"format": "dk4-maria-native-widget-and-portrait-fixture-proof-v1",
             "research_ROM_sha256": manifest["research_ROM_sha256"],
             "PNG": path.as_posix(), "PNG_sha256": capture["PNG_sha256"],
             "portrait": {"resource": resource, "resource_sha256": sha(raw),
                          "native_bounds": [76, 28, 180, 164], "complete_native5_pixels": 14144,
                          "all_edge_and_background_pixels_exact": True},
             "fields": fields, "native_ink_pixels": sum(row["complete_native_font_ink_pixels"] for row in fields),
             "original_native_font_and_resource_preserved": True,
             "fixture_selector_exposes_fourth_captain": True, "legitimate_gameplay_unlock_proved": False,
             "no_savestate_or_emulator_memory_injection": True,
             "visual_review": "pending", "not_for_normal_gameplay_release_or_handoff": True,
             "registered_ROM_changed": False, "goal_complete": False}
    (ROOT / "native_widget_pixels.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_portrait_pixels": 14144, "complete_widget_fields": len(fields),
                      "complete_font_ink_pixels": proof["native_ink_pixels"], "test_fixture_only": True}))


if __name__ == "__main__":
    main()
