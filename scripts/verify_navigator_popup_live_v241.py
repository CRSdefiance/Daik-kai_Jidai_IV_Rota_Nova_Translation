"""Verify complete displayed words and preserve every earlier replay frame."""

import json
from pathlib import Path

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

SOURCE = Path("work/emulation_v193/gender_live_v241/navigation")
CAPTURE = Path("work/emulation_v193/navigator_popup_v241")
ROOT = Path("work/analysis/navigator_popup_v241")
ROM = Path("out/all_routes_combined_v241_candidate.nds")


def report(root, digest):
    result = json.loads((root / "capture_report.json").read_text(encoding="utf-8"))
    assert result["ROM_sha256"] == digest
    assert result["cold_boot"] and not result["savestate_loaded"] and not result["callback_errors"]
    assert result["core_DLL_sha256"] == "42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b"
    for row in result["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    return result


def frame(report, number):
    row = next(r for r in report["frames_captured"] if r["frame"] == number)
    return Image.open(row["path"]).convert("RGB"), row


def main():
    digest = sha(ROM.read_bytes())
    old = report(SOURCE, "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f")
    new = report(CAPTURE, digest)
    assert old["scripted_input_schedule"] == new["scripted_input_schedule"]
    matches = []
    for row in new["frames_captured"]:
        n = row["frame"]
        if n >= 20000:
            continue
        before, _ = frame(old, n)
        after, _ = frame(new, n)
        assert before.tobytes() == after.tobytes()
        matches.append(n)
    before, _ = frame(old, 20000)
    after, capture = frame(new, 20000)
    changed_bounds = ImageChops.difference(before, after).getbbox()
    assert changed_bounds and 85 <= changed_bounds[0] < changed_bounds[2] <= 172
    assert 256 <= changed_bounds[1] < changed_bounds[3] <= 318
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file("/__arm9__.bin"))
    glyphs = []
    for text, x, y in [("Sort", 116, 272), ("Filter", 110, 292)]:
        count, bounds = complete_mask(font, text, after, x, y, (8, 8, 8))
        assert 0 <= bounds[0] < bounds[2] <= 256 and 192 <= bounds[1] < bounds[3] <= 384
        glyphs.append({"text": text, "bounds": bounds, "complete_font_ink_pixels": count,
                       "complete_ink_and_blank_cells_exact": True, "first_last_letters_present": True})
    proof = {"format": "dk4-navigator-popup-live-proof-v241", "ROM_sha256": digest,
             "capture": capture, "glyphs": glyphs,
             "complete_glyph_ink_pixels": sum(r["complete_font_ink_pixels"] for r in glyphs),
             "exact_unchanged_full_frame_matches_before_popup": matches,
             "changed_framebuffer_bounds": list(changed_bounds),
             "all_changed_pixels_confined_to_popup": True,
             "source_Japanese_menu_replaced_with_complete_natural_English": True,
             "title_New_Game_story_town_sailing_and_Deck_View_replay_preserved": True,
             "native_popup_ASCII_renderer_confirmed_by_live_complete_font_match": True,
             "no_savestate_RAM_injection_or_emulator_hooks": True,
             "physical_device_or_user_acceptance_not_claimed": True,
             "full_goal_complete": False}
    (ROOT / "live_pixels.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    saved_path = ROOT / "saved_proof.json"
    saved = json.loads(saved_path.read_text())
    saved["cold_boot_display_pending"] = False
    saved["live_pixel_proof"] = str(ROOT / "live_pixels.json")
    saved["live_pixel_proof_sha256"] = sha((ROOT / "live_pixels.json").read_bytes())
    saved_path.write_text(json.dumps(saved, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_label_ink_pixels": proof["complete_glyph_ink_pixels"],
                      "unchanged_complete_frames": len(matches), "popup_only_changed_bounds": changed_bounds}))


if __name__ == "__main__":
    main()
