"""Ordinary Guild purchase and real player-inventory glyph/art verification."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/equipment_purchase_v259")
ROM = Path("out/all_routes_combined_v258_candidate.nds")
CAPTURE = Path("work/emulation_v193/purchased_inventory_v259")


def main():
    digest = sha(ROM.read_bytes())
    assert digest == "da3826983959c31104b7c1e3b66b65e3f69abb89fb71501a4d2a4c63a5bac613"
    report = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert report["ROM_sha256"] == digest and report["cold_boot"] and not report["savestate_loaded"]
    assert report["frames"] == 32000 and not report["callback_errors"]
    for row in report["frames_captured"]:
        assert sha(Path(row["path"]).read_bytes()) == row["PNG_sha256"]
    image = Image.open(CAPTURE / "frame_032000_final.png").convert("RGB")
    rom = NdsImage.open(ROM)
    font = GameAsciiFont.from_arm9(rom.read_file("/__arm9__.bin"))
    labels = []
    for text, x, y, right in [("Old Dagger Map 1", 56, 24, 232), ("Ancient Map", 8, 64, 88),
                               ("Map fragment. Collect all four.", 8, 112, 232)]:
        expected = {(x + n * 5 + gx, y + gy) for n, ch in enumerate(text)
                    for gy in range(11) for gx in range(6) if font.decode(ch).getpixel((gx, gy))}
        actual = {(xx, yy) for yy in range(y, y + 11) for xx in range(x, right)
                  if min(image.getpixel((xx, yy))) > 200
                  and max(image.getpixel((xx, yy))) - min(image.getpixel((xx, yy))) < 5}
        assert actual == expected, (text, len(actual), len(expected))
        labels.append({"text": text, "origin": [x, y], "advance": 5, "complete_native_ink_pixels": len(expected),
                       "all_first_internal_and_final_glyphs_exact": True})
    atlas = PxlImage.from_bytes(rom.read_file("/_pxl/item.pxl"))
    colors = [tuple(c // 8 for c in value[:3]) for value in atlas.palette]
    actual_icon = [tuple(c // 8 for c in image.getpixel((16 + x, 24 + y))) for y in range(32) for x in range(32)]
    matching = []
    for index in range(218):
        pixels = atlas.indices[index * 1024:(index + 1) * 1024]
        if all(actual_icon[n] == colors[value] for n, value in enumerate(pixels)):
            matching.append(index)
    assert matching == [202]
    for file in ["translations/graphics_completion_campaign_v1.json", "translations/graphics_visual_audit_v150.json"]:
        audit = json.loads(Path(file).read_text(encoding="utf-8"))["plaque_style_v247"]
        assert len(audit["ongoing_plaque_inventory"]) == 18 and not audit["full_plaque_audit_complete"]
        assert all(not row["fully_completed"] for row in audit["ongoing_plaque_inventory"])
    proof = {"format": "dk4-purchased-inventory-live-v259", "candidate": str(ROM), "candidate_sha256": digest,
             "ordinary_cold_boot_purchase_and_player_inventory_path_recorded": True,
             "actual_purchase_confirmation_frame": 27400, "actual_thank_you_frame": 27600,
             "displayed_money_before": 35000, "displayed_money_after": 32000,
             "money_values_visually_observed_not_game_internal_arithmetic_proof": True,
             "actual_player_inventory_frame": 32000, "complete_glyph_labels": labels,
             "exact_native_atlas_index": 202, "complete_32x32_art_pixels_exact_at_native5bit": 1024,
             "observed_Guild_stock": ["Rainbow Marbles", "Moya Lead", "Old Dagger Map 1"],
             "acquired_item_is_Ancient_Map_not_occupied_weapon_or_armor": True,
             "occupied_equipment_hint_width_and_paper_audit_remains_open": True,
             "normal_equipped_game_save_requested_from_user": True,
             "all18_base_plaques_and_all_variants_incomplete": True,
             "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "saved_live_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print("Purchased map inventory:652 complete glyph pixels and1024 exact original art pixels; equipment audit remains open.")


if __name__ == "__main__":
    main()
