"""Register the observed room/count terminology repair with its complete stack."""

import copy
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_battery_labels import ARM, FILE, render
from dk4tool.patch.ship_quarters_label import apply_release as apply_quarters
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path("work/analysis/ship_batteries_v593")
PARENT = Path("out/all_routes_combined_v591_candidate.nds")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = NdsImage.open(PARENT), NdsImage.open("work/clean.nds")
    assert sha(PARENT.read_bytes()) == "7f2d10824e18d276adb23b01be48dac2d27adc2c4ec8ec16bb39a93a90dc3d73"
    # Generalizing the existing painter must reproduce the exact V591 plaque.
    previous = NdsImage.open("out/all_routes_combined_v581_candidate.nds")
    _, quarters, _ = apply_quarters(previous, clean, "translations/ship_quarters_label_v1.json")
    assert quarters == current.read_file(FILE)
    source = Path("E:/Rota Nova translations/Generated/work/emulation_v193/ship_batteries_v592/capture_report.json")
    r = json.loads(source.read_text(encoding="utf-8"))
    assert r["ROM_sha256"] == sha(PARENT.read_bytes()) and r["frames"] == 6920
    assert r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"]
    assert not any(value for key, value in r.items() if key.startswith("synthetic_"))
    assert r["battery_save_preloaded"]["source_sha256"] == "958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb"
    assert sha(Path(r["battery_save_preloaded"]["source"]).read_bytes()) == r["battery_save_preloaded"]["source_sha256"]
    shots = {row["frame"]: row for row in r["frames_captured"]}
    font = GameAsciiFont.from_arm9(current.read_file(ARM))
    masks = []
    for frame, word in ((5560, "Gun Deck"), (5640, "Marines"), (6760, "Gun Deck"), (6920, "Marines")):
        image = Image.open(shots[frame]["path"]).convert("RGB")
        count, bounds = complete_mask(font, word, image, 72, 24, (230, 230, 230))
        masks.append({"frame": frame, "text": word, "ink": count, "bounds": bounds})
    outputs, plan = render(current, clean)
    config = {"format": "dk4-ship-battery-labels-v1", "source_sha256": {p: sha(current.read_file(p)) for p in outputs},
              "clean_sha256": {p: sha(clean.read_file(p)) for p in (*outputs, "/_pxl/towninfo.pxl")},
              "target_sha256": {p: sha(data) for p, data in outputs.items()},
              "status": "experimental", "source_Japanese": {"海兵詰所": "Quarters", "武装砲台": "Battery / Batteries"},
              "reason": "Count gun positions that accept a Gunner separately from individual cannons; match existing Help gun-battery wording. Marine room uses established Quarters."}
    Path("translations/ship_battery_labels_v1.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plan.update(source_report=str(source), source_report_sha256=sha(source.read_bytes()),
                source_label_masks=masks, original_Help_page=129,
                original_source_description="船の砲台です。配置した航海士は「砲撃手」になります。",
                existing_Help_term="Gun Batteries", generalized_Quarters_painter_exact_V591=True,
                native_first_last_and_Graphics_verification_pending=True)
    (ROOT / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "deck_replay_inputs.json").write_text(json.dumps(r["scripted_input_schedule"], indent=2) + "\n", encoding="utf-8")
    images = [PxlImage.from_bytes(data).render().crop((132, 104, 196, 120))
              for data in (clean.read_file(FILE), current.read_file(FILE), outputs[FILE])]
    sheet = Image.new("RGB", (850, 100), (35, 45, 50)); painter = ImageDraw.Draw(sheet)
    for n, (label, image) in enumerate(zip(("Original gun positions", "V591 Guns", "Batteries, original grain retained"), images, strict=True)):
        painter.text((n * 280 + 5, 5), label, fill="white")
        sheet.paste(image.convert("RGB").resize((256, 64), Image.Resampling.NEAREST), (n * 280 + 5, 25))
    sheet.save(ROOT / "source_current_proposed_4x.png")
    registry = Path("translations/release_stack.json")
    stack = json.loads(registry.read_text(encoding="utf-8"))
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v591"])
    profile.update(ship_battery_labels="translations/ship_battery_labels_v1.json",
                   description="Complete V591 stack plus consistent Battery/Batteries and Quarters room labels.",
                   note="Experimental; one ship-plaque lettering mask and two fixed12-byte Deck text slots change. All other artwork, code and data stay exact to V591.")
    existing = stack["profiles"].get("all-routes-unified-v593")
    assert existing is None or existing == profile
    stack["profiles"]["all-routes-unified-v593"] = profile
    registry.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared V593: {plan['image']['changed_pixels']} plaque indices and two bounded room-label slots; whole V591 stack retained.")


if __name__ == "__main__":
    main()
