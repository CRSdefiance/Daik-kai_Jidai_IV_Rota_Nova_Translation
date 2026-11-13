"""Fresh V272 town actions and complete Sailor Info status/plaque pixels."""

import hashlib
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_short_equipment_release_v252 import numeric_field

ROOT = Path("work/analysis/plaque_states_v274")
CAPTURE = Path("work/emulation_v193/plaque_states_v274")
ROM = Path("out/all_routes_combined_v272_candidate.nds")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    digest = sha(ROM)
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and report["frames"] == 32200
    for row in report["frames_captured"]:
        assert sha(row["path"]) == row["PNG_sha256"]
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    batch = json.loads(Path("translations/person_info_graphics_v3.json").read_text(encoding="utf-8"))
    art = PxlImage.from_bytes(rom.read_file(batch["file_path"]))
    cases = []
    for frame, name, action in [(26400, "Raphael Castor", "Treat Everyone"),
                                (27000, "Janus Pasar", "Treat Everyone"),
                                (27600, "Claudio Manaus", "Treat Everyone"),
                                (28200, "Julio Erneco", "Treat Everyone"),
                                (32200, "Raphael Castor", "Order Drink")]:
        path = CAPTURE / f"frame_{frame:06d}_navigation.png"
        image = Image.open(path).convert("RGB")
        regions = []
        for row in batch["records"]:
            x0, y0, x1, y1 = row["plaque_box"]
            for y in range(y0, y1):
                for x in range(x0, x1):
                    expected = art.palette[art.indices[y * 256 + x]][:3]
                    assert tuple(c // 8 for c in image.getpixel((x, y))) == tuple(c // 8 for c in expected), (frame, x, y)
            regions.append([x0, y0, x1, y1])
        status = []
        for label, text, y in [("Health", "Healthy", 108), ("Mood", "Normal", 128)]:
            ink, bounds = complete_mask(font, text, image, 56, y, (230, 230, 230))
            status.append({"label": label, "text": text, "ink_pixels": ink,
                           "complete_bounds": bounds, "first_and_last_characters_complete": True})
        skills = []
        for name_label, x, y in [("Command", 16, 272), ("Sailing", 96, 272), ("Survey", 176, 272),
                                 ("Finance", 16, 296), ("Observe", 96, 296), ("Vigor", 176, 296),
                                 ("Aim", 16, 320), ("Swords", 96, 320), ("Speech", 176, 320), ("Guile", 16, 344)]:
            value = numeric_field(font, image, x + 42, y)
            ink, bounds = complete_mask(font, f"{name_label:>7}{value:3d}", image, x, y, (230, 230, 230))
            skills.append({"label": name_label, "value": value, "ink_pixels": ink, "bounds": bounds})
        cases.append({"frame": frame, "displayed_name": name, "town_action": action,
                      "capture": str(path), "capture_sha256": sha(path), "status": status,
                      "all10_complete_plaque_regions_exact": regions, "all10_skill_lines_exact": skills})
    for fn in ["graphics_completion_campaign_v1.json", "graphics_visual_audit_v150.json"]:
        audit = json.loads((Path("translations") / fn).read_text(encoding="utf-8"))
        plaque = audit["plaque_style_v247"]
        assert len(plaque["ongoing_plaque_inventory"]) == 18
        assert not plaque["full_plaque_audit_complete"]
        assert all(not row["fully_completed"] for row in plaque["ongoing_plaque_inventory"])
        assert audit["user_scope_exceptions"]["low_resolution_online_images"]["translation_required"] is False
    proof = {"format": "dk4-sailor-status-display-audit-v274", "candidate": str(ROM),
             "candidate_sha256": digest, "capture_report": str(CAPTURE / "capture_report.json"),
             "ordinary_cold_boot_controller_and_stylus_actions_no_loaded_state": True,
             "frames": report["frames"], "cases": cases,
             "both_town_actions_failed_to_produce_alternate_officer_status": True,
             "complete_status_label_composites": 10, "complete_plaque_composites": 50,
             "complete_skill_label_number_lines": 50,
             "alternate_status_gameplay_display_remains_unproved": True,
             "all18_plaque_hint_entries_remain_incomplete": True, "full_goal_complete": False}
    (ROOT / "saved_display_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status_labels": 10, "full_plaque_regions": 50, "complete_skill_lines": 50,
                      "alternate_status_seen": False, "candidate_sha256": digest}))


if __name__ == "__main__":
    main()
