"""Check actual Extras title pixels and normal menu navigation in V218."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_original_latin_cards_native_v197 import native5

ROM = Path("out/all_routes_combined_v218_candidate.nds")
ROM_SHA = "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"
ROOT = Path("work/emulation_v193/alternate_title_v238")
OUT = Path("work/analysis/alternate_title_v238")


def main():
    assert sha(ROM.read_bytes()) == ROM_SHA
    rom = NdsImage.open(ROM)
    expected = {}
    for index in (3, 5):
        path = f"/_pxl/title/title{index:02d}.pxl"
        data = rom.read_file(path)
        pxl = PxlImage.from_bytes(data)
        assert (pxl.width, pxl.height) == (256, 192)
        expected[index] = (path, sha(data), [native5(pxl.palette[n]) for n in pxl.indices])
    cases, identities = [], []
    for folder, schedule, frames in (
        (ROOT, Path("work/emulation_v193/extras_inputs.json"), [(n, 5) for n in range(1300, 1801, 100)]),
        (ROOT / "navigation", ROOT / "navigation_inputs.json",
         [(1300, 5), (1800, 5), (2100, 5), (2300, 5), (2500, 5), (2600, 5), (2900, 3), (3000, 3), (3100, 3)]),
    ):
        report = json.loads((folder / "capture_report.json").read_text(encoding="utf-8"))
        assert report["ROM_sha256"] == ROM_SHA
        assert report["cold_boot"] and not report["savestate_loaded"]
        assert not report["callback_errors"]
        assert report["scripted_input_schedule"] == json.loads(schedule.read_text())
        assert report["core_DLL_sha256"] == "42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b"
        for row in report["frames_captured"]:
            assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
        identities.append({"report": str(folder / "capture_report.json"),
                           "sha256": sha((folder / "capture_report.json").read_bytes()),
                           "checked_PNGs": len(report["frames_captured"])})
        for frame, index in frames:
            row = next(r for r in report["frames_captured"] if r["frame"] == frame)
            actual = Image.open(row["path"]).convert("RGB").crop((0, 0, 256, 192))
            path, digest, pixels = expected[index]
            assert [native5(c) for c in actual.get_flattened_data()] == pixels
            cases.append({"frame": frame, "capture": row["path"], "PNG_sha256": row["PNG_sha256"],
                          "resource": path, "resource_sha256": digest,
                          "complete_screen_pixels_exact": 49152})
    proof = {"format": "dk4-alternate-title-display-v238", "ROM_sha256": ROM_SHA,
             "previous_goal_turn_classification": "no-progress-existing-naming-documentation-confirmed",
             "current_goal_turn_classification": "progress-actual-alternate-title-display-and-menu-navigation",
             "capture_identities": identities, "complete_frame_matches": cases,
             "title05_actual_display": "Extras menu and About Extras, reached through normal START/DOWN/A input",
             "visual_navigation_frames_reviewed": [2100, 2500, 3000],
             "normal_back_navigation_returns_to_Extras_then_main_menu": True,
             "both_complete_logos_edges_background_and_screen_bounds_verified": True,
             "RAM_injection_or_savestate": False, "ROM_modified": False,
             "standalone_logo_and_other_graphics_consumers_pending": True,
             "physical_device_and_user_acceptance_not_claimed": True, "full_goal_complete": False}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "native_display_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_frame_matches": len(cases), "pixels_checked": len(cases) * 49152,
                      "normal_navigation_verified": True, "ROM_modified": False}))


if __name__ == "__main__":
    main()
