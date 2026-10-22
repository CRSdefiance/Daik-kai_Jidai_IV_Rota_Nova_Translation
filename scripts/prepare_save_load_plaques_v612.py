"""Review source/native Save/Load geometry and register its complete integration."""

import copy
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.save_load_plaques import DONOR, FILE, transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path("work/analysis/save_load_plaques_v612")


def main():
    parent, clean = NdsImage.open("out/all_routes_combined_v611_candidate.nds"), NdsImage.open("work/clean.nds")
    data, report = transform(parent.read_file(FILE), clean.read_file(FILE), clean.read_file(DONOR), parent.read_file("/__arm9__.bin"))
    (ROOT / "save_load_RESEARCH_ONLY.pxl").write_bytes(data)
    save(ROOT / "transform_proof.json", report)
    save("translations/save_load_plaques_v1.json", {"format": "dk4-save-load-plaques-v1", **report})
    atlases = [PxlImage.from_bytes(d) for d in (clean.read_file(FILE), parent.read_file(FILE), data)]
    sheet = Image.new("RGB", (1000, 300), "#263238")
    draw = ImageDraw.Draw(sheet)
    for col, label in enumerate(("Original Japanese", "Current V611", "Source-frame/fine-grain repair")):
        draw.text((col * 330 + 8, 8), label, fill="white")
    for n, row in enumerate(report["records"]):
        draw.text((8, 35 + n * 130), row["English"], fill="#e7d9aa")
        l, t, r, b = row["restore_box"]
        for col, atlas in enumerate(atlases):
            crop = atlas.render().crop((l - 2, t - 2, r + 2, b + 2)).convert("RGB")
            sheet.paste(crop.resize((crop.width * 5, crop.height * 5), Image.Resampling.NEAREST), (col * 330 + 8, 55 + n * 130))
    sheet.save(ROOT / "source_current_repair_5x.png")
    run = read("E:/Rota Nova translations/Generated/work/emulation_v193/save_load_plaques_v612_initial/capture_report.json")
    assert run["frames"] == 14200 and not run["callback_errors"]
    save(ROOT / "complete_inputs.json", run["scripted_input_schedule"])
    path = Path("translations/release_stack.json")
    registry = read(path)
    profile = copy.deepcopy(registry["profiles"]["all-routes-unified-v611"])
    profile.update({"save_load_plaques": "translations/save_load_plaques_v1.json", "status": "experimental",
                    "description": "Complete V611 plus original Save/Load plaque geometry/rims and fine source wood.",
                    "note": "Normal Save/Load testing required. Inherited regional-fleet plaques still await actual native context; V610 remains latest verified."})
    if "all-routes-unified-v612" in registry["profiles"]:
        assert registry["profiles"]["all-routes-unified-v612"] == profile
    registry["profiles"]["all-routes-unified-v612"] = profile
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Prepared two source-geometry Save/Load plaques; inherited V611 repair retained; registered complete V612.")


if __name__ == "__main__":
    main()
