"""Register the observed marine-quarters terminology correction atop V581."""

import copy
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_quarters_label import FILE, render
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/ship_quarters_v591")
PARENT = Path("out/all_routes_combined_v581_candidate.nds")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(PARENT), NdsImage.open("work/clean.nds")
    assert sha(PARENT.read_bytes()) == "542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68"
    report_path = Path("E:/Rota Nova translations/Generated/work/emulation_v193/menu_context_v590/capture_report.json")
    r = json.loads(report_path.read_text(encoding="utf-8"))
    assert r["ROM_sha256"] == sha(PARENT.read_bytes()) and r["frames"] == 5840
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert not any(value for key, value in r.items() if key.startswith("synthetic_"))
    assert r["battery_save_preloaded"]["source_sha256"] == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
    assert sha(Path(r["battery_save_preloaded"]["source"]).read_bytes()) == r["battery_save_preloaded"]["source_sha256"]
    output, plan = render(current, clean)
    (ROOT / "reviewed_shipinfo.pxl").write_bytes(output)
    plan.update({"source_report": str(report_path), "source_report_sha256": sha(report_path.read_bytes()),
                 "same_ship_observed_frames": {"Ships_Marines1": 5360, "Assign_Quarters1": 5840},
                 "ordinary_sailing_inspection_and_crew_setup": True,
                 "meaning": "Count of marine quarters, not number of marines. Match established Assign Sailors wording.",
                 "source_Japanese_original_crop_review": "work/analysis/plaque_families_v556/ship_texture_prototype_review.png",
                 "inherited_Admiral_format_not_observed_or_changed": True,
                 "ordinary_miniature_and_Confirm_parents_still_open": True})
    (ROOT / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    config = {"format": "dk4-ship-quarters-label-v1", "file_path": FILE,
              "source_sha256": sha(current.read_file(FILE)), "target_sha256": sha(output),
              "clean_sha256": sha(clean.read_file(FILE)),
              "font_arm9_sha256": sha(current.read_file("/__arm9__.bin")),
              "donor_sha256": sha(clean.read_file("/_pxl/towninfo.pxl")),
              "Japanese": "海兵詰所", "English": "Quarters", "previous_English": "Marines",
              "reason": plan["meaning"], "status": "experimental-native-verification-pending"}
    Path("translations/ship_quarters_label_v1.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    images = [PxlImage.from_bytes(data).render().crop((5, 104, 68, 120))
              for data in (clean.read_file(FILE), current.read_file(FILE), output)]
    sheet = Image.new("RGB", (3 * 280, 100), (35, 45, 50))
    painter = ImageDraw.Draw(sheet)
    for n, (label, img) in enumerate(zip(("Original marine quarters", "V581 Marines", "Quarters, source grain retained"), images, strict=True)):
        painter.text((n * 280 + 5, 5), label, fill="white")
        sheet.paste(img.convert("RGB").resize((252, 64), Image.Resampling.NEAREST), (n * 280 + 5, 25))
    sheet.save(ROOT / "source_current_proposed_4x.png")
    (ROOT / "replay_inputs.json").write_text(json.dumps(r["scripted_input_schedule"], indent=2) + "\n", encoding="utf-8")
    registry = Path("translations/release_stack.json")
    stack = json.loads(registry.read_text(encoding="utf-8"))
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v581"])
    profile["ship_quarters_label"] = "translations/ship_quarters_label_v1.json"
    profile["description"] = "Complete V581 stack plus source-faithful Quarters graphic in Ship Info, matching Assign Sailors."
    profile["note"] = "Experimental; only the Marines-to-Quarters glyph pixels change. Ordinary full-goal audit and user acceptance remain open."
    existing = stack["profiles"].get("all-routes-unified-v591")
    assert existing is None or existing == profile
    stack["profiles"]["all-routes-unified-v591"] = profile
    registry.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared registered V591 Quarters correction: {plan['changed_pixels']} pixel indices; complete100-point glyph mask; all other pixels exact.")


if __name__ == "__main__":
    main()
