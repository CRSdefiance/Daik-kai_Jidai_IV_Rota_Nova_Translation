"""Review clean frame edges without changing localized label geometry or ink."""

import copy
import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.source_plaque_bevels import transform_arm, transform_files
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/plaque_borders_v546")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current = NdsImage.open("out/all_routes_combined_v545_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    groups = copy.deepcopy(read("translations/source_plaque_grain_v1.json")["files"])
    for group in groups:
        group["source_sha256"] = sha(current.read_file(group["file_path"]))
    results, reports = transform_files(current, clean, groups)
    font = GameAsciiFont.from_arm9(current.read_file("/__arm9__.bin"))
    for group, name, report in zip(groups, ("crew", "person"), reports, strict=True):
        group["target_sha256"] = report["target_sha256"]
        old = PxlImage.from_bytes(current.read_file(group["file_path"]))
        new = PxlImage.from_bytes(results[group["file_path"]])
        for row in group["records"]:
            l, t, r, b = row["draw_box"]
            tx, ty = l + (r - l - len(row["english"]) * 5) // 2, t + (b - t - 11) // 2
            expected = {(tx + n * 5 + x, ty + y) for n, char in enumerate(row["english"])
                        for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))}
            x0, y0, x1, y1 = row["plaque_box"]
            actual = {(x, y) for y in range(y0, y1) for x in range(x0, x1)
                      if new.indices[y * new.width + x] == row["ink_palette_index"]}
            assert actual == expected, row["english"]
        sheet = Image.new("RGB", (720, len(group["records"]) * 110 + 30), (40, 45, 50))
        draw = ImageDraw.Draw(sheet)
        draw.text((5, 5), "V545 edges", fill="white")
        draw.text((365, 5), "Clean original bevel at retained layout", fill="white")
        for n, row in enumerate(group["records"]):
            draw.text((5, n * 110 + 30), row["english"], fill="white")
            for col, asset in enumerate((old, new)):
                crop = asset.render().crop(row["plaque_box"]).convert("RGB")
                sheet.paste(crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST),
                            (col * 360 + 5, n * 110 + 50))
        sheet.save(ROOT / f"{name}_bevel_review.png")
        (ROOT / f"{name}_RESEARCH_ONLY.pxl").write_bytes(new.source[:new.pixels_offset] + results[group["file_path"]][new.pixels_offset:])
    arm, plan = transform_arm(current.read_file("/__arm9__.bin"), clean)
    (ROOT / "research_arm9.bin").write_bytes(arm)
    write(ROOT / "stage_proof.json", {"files": reports, "equipment": plan,
                                      "complete_17_font_masks": True,
                                      "native_review_pending": True, "all18_entries_incomplete": True})
    cfg = {"format": "dk4-source-plaque-bevel-release-v1", "files": groups,
           "donor_sha256": sha(clean.read_file("/_pxl/towninfo.pxl")),
           "target_arm9_sha256": sha(arm), "status": "experimental"}
    write("translations/source_plaque_bevels_v1.json", cfg)
    stack = read("translations/release_stack.json")
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v545"])
    profile["source_plaque_bevels"] = "translations/source_plaque_bevels_v1.json"
    profile["description"] = profile["note"] = "Complete V545 stack plus original native bevels at retained localized geometry. All plaque audits remain open."
    stack["profiles"]["all-routes-unified-v546"] = profile
    write("translations/release_stack.json", stack)
    print("Registered V546: 17 full masks preserved; true original bevel donor [8,20,48,36].")


if __name__ == "__main__":
    main()
