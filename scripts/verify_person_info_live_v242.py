"""Verify full gender cells in their actual palette bank and four live plaques."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path("out/all_routes_combined_v241_candidate.nds")
ROM_SHA = "d863f74ba3e5466f5a221ba93e00d53fd1588a32cecdd349006b7eb0698e8027"
ROOT = Path("work/analysis/person_info_v242")
CAPTURES = Path("work/emulation_v193/person_info_v242")
PLAQUES = (("Health", (3, 103, 49, 118)), ("Mood", (3, 123, 49, 138)),
           ("Level", (3, 143, 49, 158)), ("HP", (3, 163, 49, 178)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lil-frame", type=int, required=True)
    args = parser.parse_args()
    assert sha(ROM.read_bytes()) == ROM_SHA
    rom = NdsImage.open(ROM)
    previous = NdsImage.open("out/all_routes_combined_v218_candidate.nds")
    raw = rom.read_file("/_pxl/__marker.pxl")
    assert raw == previous.read_file("/_pxl/__marker.pxl")
    marker = PxlImage.from_bytes(raw)
    _, _, _, palette_start, pixels_start = struct.unpack_from("<5I", raw)
    assert (pixels_start - palette_start) == 83 * 32
    # The original parent places 0x30 in view field+36. This selects bank 48,
    # not entry offset 48 and not the decoder's first-bank thumbnail palette.
    bank = 48
    palette_bytes = raw[palette_start + bank * 32:palette_start + (bank + 1) * 32]
    palette = [native5(bgr555(v)) for (v,) in struct.iter_unpack("<H", palette_bytes)]
    crop_proof = json.loads(Path("work/analysis/gender_consumers_v240/native_proof.json").read_text())
    assert all(c["native_view_fields"][9] == bank for c in crop_proof["actual_crop_cases"])
    plaques = PxlImage.from_bytes(rom.read_file("/_pxl/personinfo.pxl"))
    assert plaques.source == previous.read_file("/_pxl/personinfo.pxl")
    cases, captures = [], []
    for folder, selections in (("town", [(16600, "Rafael", "male"), (16900, "Janus", "male"),
                                        (17200, "Claudio", "male"), (17500, "Julio", "male")]),
                               ("lil", [(args.lil_frame, "Lil", "female")])):
        report_path = CAPTURES / folder / "capture_report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["ROM_sha256"] == ROM_SHA and report["cold_boot"]
        assert not report["savestate_loaded"] and not report["callback_errors"]
        assert report["core_DLL_sha256"] == "42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b"
        for row in report["frames_captured"]:
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        captures.append({"report": str(report_path), "sha256": sha(report_path.read_bytes())})
        for frame, character, gender in selections:
            row = next(r for r in report["frames_captured"] if r["frame"] == frame)
            image = Image.open(row["path"]).convert("RGB")
            origin = (232, 96) if gender == "male" else (240, 112)
            for y in range(16):
                for x in range(16):
                    index = marker.indices[(origin[1] + y) * marker.width + origin[0] + x]
                    assert native5(image.getpixel((84 + x, 76 + y))) == palette[index]
            plaque_rows = []
            for text, (x0, y0, x1, y1) in PLAQUES:
                for y in range(y0, y1):
                    for x in range(x0, x1):
                        assert native5(image.getpixel((x, y))) == native5(plaques.palette[plaques.indices[y * 256 + x]])
                plaque_rows.append({"text": text, "source_and_screen_bounds": [x0, y0, x1, y1],
                                    "complete_cell_pixels_exact": (x1 - x0) * (y1 - y0)})
            cases.append({"character": character, "gender": gender, "frame": frame,
                          "capture": row, "gender_source_origin": list(origin),
                          "gender_screen_bounds": [84, 76, 100, 92],
                          "complete_gender_cell_pixels_exact": 256,
                          "circle_arrow_or_cross_and_original_border_exact": True,
                          "plaques": plaque_rows})
    proof = {"format": "dk4-live-person-info-gender-and-plaques-v242", "ROM_sha256": ROM_SHA,
             "marker_source_sha256": sha(raw), "stored_marker_palette_banks": 83,
             "actual_gender_palette_bank": bank, "palette_bank_sha256": sha(palette_bytes),
             "palette_selection_matches_original_native_parent_field": True,
             "native_palette_bank_must_not_be_inferred_from_first_bank_preview": True,
             "capture_reports": captures, "cases": cases,
             "complete_gender_cell_pixels_checked": sum(c["complete_gender_cell_pixels_exact"] for c in cases),
             "complete_plaque_cell_pixels_checked": sum(p["complete_cell_pixels_exact"] for c in cases for p in c["plaques"]),
             "no_savestate_RAM_injection_or_fixture_ROM": True,
             "observed_complete_parent_and_normal_navigation_verified": True,
             "other_parent_palette_banks_embedded_copy_and_all_devices_not_inferred": True,
             "ROM_modified": False, "full_goal_complete": False}
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "live_pixels.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"live_characters": len(cases), "complete_gender_pixels": proof["complete_gender_cell_pixels_checked"],
                      "complete_plaque_pixels": proof["complete_plaque_cell_pixels_checked"], "native_palette_bank": bank}))


if __name__ == "__main__":
    main()
