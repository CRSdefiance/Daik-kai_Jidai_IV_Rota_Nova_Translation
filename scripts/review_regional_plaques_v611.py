"""Original/current/source-repair regional fleet material review, before integration."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_fleet_plaques import DONOR, FILE, render
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/regional_plaques_v611")
PARENT = Path("out/all_routes_combined_v610_candidate.nds")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    parent, clean = NdsImage.open(PARENT), NdsImage.open("work/clean.nds")
    data, report = render(parent.read_file(FILE), clean.read_file(FILE), clean.read_file(DONOR),
                          parent.read_file("/__arm9__.bin"))
    target = ROOT / "regional_RESEARCH_ONLY.pxl"
    target.write_bytes(data)
    atlases = [PxlImage.from_bytes(d) for d in (clean.read_file(FILE), parent.read_file(FILE), data)]
    sheet = Image.new("RGB", (1000, 650), "#263238")
    draw = ImageDraw.Draw(sheet)
    for n, name in enumerate(("Original Japanese", "Current V610", "Source-framed repair prototype")):
        draw.text((n * 330 + 8, 8), name, fill="white")
    for i, row in enumerate(report["records"]):
        draw.text((8, 40 + i * 120), row["English"], fill="#e7d9aa")
        for j, atlas in enumerate(atlases):
            l, t, r, b = row["restore_box"]
            box = (max(0, l - 3), t - 2, r + 4, b + 2)
            crop = atlas.render().crop(box).convert("RGB")
            sheet.paste(crop.resize((crop.width * 5, crop.height * 5), Image.Resampling.NEAREST),
                        (j * 330 + 8, 60 + i * 120))
    sheet.save(ROOT / "regional_source_current_prototype_5x.png")
    config = {"format": "dk4-regional-fleet-plaques-v1", **report}
    Path("translations/regional_fleet_plaques_v1.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    proof = {"parent": str(PARENT), "parent_sha256": sha(PARENT.read_bytes()), **report,
             "research_only_asset": str(target), "native_display_not_yet_verified": True,
             "production_ROM_changed": False, "full_goal_complete": False}
    (ROOT / "prototype_proof.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Regional fleet: five source-framed plaques, complete native font; original wallpaper restored. Prototype only.")


if __name__ == "__main__":
    main()
