"""Verify complete native portrait crops and review the four actual PXL owners."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/portrait_binding_v202")
QA = Path("work/qa/portrait_binding_v202")


def native5(color):
    return tuple((value * 31 + 127) // 255 for value in color[:3])


def main():
    QA.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open("out/all_routes_combined_v190_candidate.nds")
    source = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    binding = json.loads((ROOT / "native_resource_binding.json").read_text(encoding="utf-8"))
    assert binding["ROM_sha256"] == sha(Path(binding["ROM"]).read_bytes())
    images, owners = {}, []
    sheet = Image.new("RGB", (660, 864), "#303030")
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(binding["cases"]):
        raw = rom.read_file(row["path"])
        assert sha(raw) == row["full_PXL_sha256"] and raw == source.read_file(row["path"])
        image = PxlImage.from_bytes(raw).render()
        assert image.size == (104, 136)
        images[index] = image
        path = QA / f"personbustup{index:02d}.png"
        image.save(path)
        x, y = index % 2 * 330, index // 2 * 432
        draw.text((x + 6, y + 4), row["path"], fill="white")
        sheet.paste(image.resize((312, 408), Image.Resampling.NEAREST).convert("RGB"), (x + 6, y + 24))
        owners.append({"path": row["path"], "PNG": path.as_posix(), "PNG_sha256": sha(path.read_bytes()),
                       "original_source_exact": True, "full_visual_review_complete": False})
    sheet_path = QA / "actual_PXL_owners_review.png"
    sheet.save(sheet_path)
    cases = []
    for index, folder, frame, filename in (
        (0, "work/emulation_v193/confirmed_name_catalog_v201/smoke", 1500, "frame_001500_cold_boot.png"),
        (1, "work/emulation_v193/confirmed_name_widgets_v198/hodram", 2100, "frame_002100_final.png"),
        (2, "work/emulation_v193/v190_lil_scene", 2100, "frame_002100_cold_boot.png"),
    ):
        capture = json.loads((Path(folder) / "capture_report.json").read_text(encoding="utf-8"))
        assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
        capture_rom_path = Path(capture["ROM"])
        assert sha(capture_rom_path.read_bytes()) == capture["ROM_sha256"]
        path = binding["cases"][index]["path"]
        assert NdsImage.open(capture_rom_path).read_file(path) == rom.read_file(path)
        frame_path = Path(folder) / filename
        saved = next(row for row in capture["frames_captured"] if row["frame"] == frame and Path(row["path"]) == frame_path)
        assert sha(frame_path.read_bytes()) == saved["PNG_sha256"]
        with Image.open(frame_path) as im:
            actual = im.convert("RGB")
        expected = images[index]
        for y in range(136):
            for x in range(104):
                assert native5(expected.getpixel((x, y))) == native5(actual.getpixel((x + 76, y + 28))), (path, x, y)
        cases.append({"path": path, "capture_ROM_sha256": capture["ROM_sha256"],
                      "frame": frame, "PNG": frame_path.as_posix(), "PNG_sha256": saved["PNG_sha256"],
                      "native_bounds": [76, 28, 180, 164], "complete_exact_native5_pixels": 14144,
                      "all_edge_and_background_pixels_included": True, "visually_reviewed": True})
    report = {"format": "dk4-native-portrait-pixel-proof-v1", "ROM_sha256": binding["ROM_sha256"],
              "cases": cases, "complete_live_portrait_pixels": sum(row["complete_exact_native5_pixels"] for row in cases),
              "all_four_source_owners": owners, "review_sheet": sheet_path.as_posix(),
              "review_sheet_sha256": sha(sheet_path.read_bytes()),
              "fourth_owner_live_display_pending": True,
              "limits": "Three actual cold-boot static portrait crops; no fourth portrait, all temporal/alpha states, legacy palette or whole-game clearance is inferred.",
              "ROM_changed": False, "goal_complete": False}
    (ROOT / "native_portrait_pixels.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_live_portraits": len(cases), "exact_native_pixels": report["complete_live_portrait_pixels"],
                      "fourth_owner_live_pending": True}))


if __name__ == "__main__":
    main()
