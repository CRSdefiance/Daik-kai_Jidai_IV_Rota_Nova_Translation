"""Original/source-framed Golden Route atlas review; no native clearance inferred."""

import copy
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.golden_route_plaques import FILES, transform
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path("work/analysis/golden_route_plaques_v613")


def main():
    parent, clean = NdsImage.open("out/all_routes_combined_v612_candidate.nds"), NdsImage.open("work/clean.nds")
    before, source = ({p: r.read_file(p) for p in FILES} for r in (parent, clean))
    output, reports = transform(before, source, parent.read_file("/__arm9__.bin"))
    save("translations/golden_route_plaques_v1.json", {"format": "dk4-golden-route-plaques-v1", "files": reports})
    save(ROOT / "source_transform_proof.json", {"files": reports, "production_ROM_changed": False,
                                               "native_verification_still_pending": True, "full_goal_complete": False})
    for p, data in output.items():
        (ROOT / (Path(p).stem + "_RESEARCH_ONLY.pxl")).write_bytes(data)
    all_rows = [(report, row) for report in reports for row in report["records"]]
    sheet = Image.new("RGB", (1350, len(all_rows) * 100 + 36), "#263238")
    draw = ImageDraw.Draw(sheet)
    for col, label in enumerate(("Original Japanese", "Current V612", "Source-frame repair prototype")):
        draw.text((col * 450 + 6, 7), label, fill="white")
    for n, (report, row) in enumerate(all_rows):
        p = report["file_path"]
        draw.text((6, 32 + n * 100), Path(p).stem + " / " + row["English"], fill="#e7d9aa")
        l, t, r, b = row["restore_box"]
        for col, data in enumerate((source[p], before[p], output[p])):
            atlas = PxlImage.from_bytes(data)
            crop = atlas.render().crop((l, max(0, t - 1), r, b + 1)).convert("RGB")
            scale = 2 if crop.width > 100 else 4
            sheet.paste(crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.NEAREST),
                        (col * 450 + 6, 48 + n * 100))
    sheet.save(ROOT / "source_current_repair_sheet.png")
    path = Path("translations/release_stack.json")
    registry = read(path)
    profile = copy.deepcopy(registry["profiles"]["all-routes-unified-v612"])
    profile.update({"golden_route_plaques": "translations/golden_route_plaques_v1.json", "status": "experimental",
                    "description": "Complete V612 plus source-framed Golden Route Discovery and both Records headers.",
                    "note": "Golden Route native verification required; isolated record/cost fixtures explicitly synthetic. Inherited regional native gap remains; V610 stays latest verified."})
    if "all-routes-unified-v613" in registry["profiles"]:
        assert registry["profiles"]["all-routes-unified-v613"] == profile
    registry["profiles"]["all-routes-unified-v613"] = profile
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Eight Golden Route labels: Goods,Profit %,Reward,Total Rewards; original frames/metadata and coherent source grain verified statically.")


if __name__ == "__main__":
    main()
