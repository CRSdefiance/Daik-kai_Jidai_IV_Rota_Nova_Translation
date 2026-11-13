"""Check complete cold-boot smoke dialogue against the candidate's native font."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/confirmed_names_v201")
CAPTURE = Path("work/emulation_v193/confirmed_name_catalog_v201/smoke")


def main():
    plan = json.loads((ROOT / "smoke_plan.json").read_text(encoding="utf-8"))
    capture = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert capture["ROM_sha256"] == plan["research_ROM_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    image_path = CAPTURE / "frame_004125_cold_boot.png"
    with Image.open(image_path) as im:
        pixels = im.convert("RGB")
    font = GameAsciiFont.from_arm9(NdsImage.open(plan["research_ROM"]).read_file("/__arm9__.bin"))
    # These lines were observed in the previous real smoke run. Revalidate every
    # glyph against the new ROM/capture instead of inheriting that run's approval.
    template = json.loads(Path("work/analysis/confirmed_names_v200/smoke_native_pixels.json").read_text(encoding="utf-8"))
    lines, expected_ink = [], set()
    for row in template["complete_rendered_lines"]:
        count = 0
        for index, character in enumerate(row["text"]):
            glyph = font.decode(character)
            assert glyph.size == (6, 11)
            for y in range(11):
                for x in range(6):
                    at = row["x"] + index * 6 + x, row["y"] + y
                    ink = bool(glyph.getpixel((x, y)))
                    assert (pixels.getpixel(at) == tuple(row["color"])) == ink, (row["text"], at)
                    if ink:
                        count += 1
                        expected_ink.add(at)
        assert count == row["ink_pixels"]
        lines.append(dict(row, all_native_ink_and_blank_cells_exact=True))
    foreground = {(x, y) for y in range(296, 352) for x in range(16, 232)
                  if pixels.getpixel((x, y)) == (0, 8, 0)}
    assert foreground == expected_ink
    aliases = [r for r in plan["entry_keys"] if r["form"] == "explicit-research-smoke-alias"]
    whole = max(aliases, key=lambda r: len(bytes.fromhex(r["key_hex"])))
    report = {"format": "dk4-confirmed-name-catalog-native-smoke-pixel-proof-v1",
              "research_ROM_sha256": plan["research_ROM_sha256"],
              "image": image_path.as_posix(), "image_sha256": sha(image_path.read_bytes()),
              "source_record_bytes": len(bytes.fromhex(whole["key_hex"])),
              "full_catalog_record_bytes": len(bytes.fromhex(whole["target_hex"])),
              "complete_rendered_lines": lines, "exact_native_ink_pixels": len(expected_ink),
              "no_extra_foreground_in_complete_text_region": True,
              "first_last_glyphs_and_blank_cells_exact": True,
              "explicit_artificial_smoke_alias_not_original_scene_translation": True,
              "original_deep_scene_control_and_GPU_checks_pending": True,
              "research_only": True, "goal_complete": False}
    (ROOT / "smoke_native_pixels.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_lines": len(lines), "native_ink_pixels": len(expected_ink), "first_last_and_blank_cells_exact": True}))


if __name__ == "__main__":
    main()
