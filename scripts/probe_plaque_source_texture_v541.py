"""Research-only restoration of plaque grain from unlettered clean-ROM pixels.

No ROM, registered batch, or old preparation dependency is modified. This is a
visual review prototype, not proof that every plaque is corrected.
"""

import copy
import hashlib
import json
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_pxl_native_label_batch

ROOT = Path("work/analysis/plaque_texture_v541")
CLEAN_SHA = "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
CURRENT_SHA = "9f2e4c47c059b0606141d93c0f17a34f16a75fd66ceefe63c04e8a2a54577859"
BASE_SHA = "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    paths = ["work/clean.nds", "out/all_routes_combined_v540_candidate.nds",
             "out/raphael_natural_v2_accepted_base.nds"]
    expected = [CLEAN_SHA, CURRENT_SHA, BASE_SHA]
    for path, sha in zip(paths, expected, strict=True):
        assert digest(Path(path).read_bytes()) == sha, path
    clean, current, base = [NdsImage.open(p) for p in paths]
    donor = PxlImage.from_bytes(clean.read_file("/_pxl/towninfo.pxl"))
    # Share plaque: two continuous blank strips, excluding Japanese and bevel.
    # Together they provide 80 source columns, enough for all 17 interiors.
    columns = list(range(2, 43)) + list(range(85, 124))
    samples = [[donor.palette[donor.indices[y * donor.width + x]][:3]
                for x in columns] for y in range(62, 74)]
    assert len(columns) == 80
    assert all(sum(rgb) >= 300 for row in samples for rgb in row)
    proofs = []
    for group, batch_name in [("crew", "assign_sailors_graphics_v5"),
                              ("person", "person_info_graphics_v3")]:
        batch = copy.deepcopy(read_json(f"translations/{batch_name}.json"))
        file_path = batch["file_path"]
        parent_data = base.read_file(file_path)
        original = PxlImage.from_bytes(clean.read_file(file_path))
        parent = PxlImage.from_bytes(parent_data)
        old = PxlImage.from_bytes(current.read_file(file_path))
        colors = {rgb: min(range(len(parent.palette)), key=lambda i: sum(
            (parent.palette[i][k] - rgb[k]) ** 2 for k in range(3)))
            for row in samples for rgb in row}
        rows = []
        for record in batch["records"]:
            x0, y0, x1, y1 = record["plaque_box"]
            bx, by, ex, _ey = record["box"]
            background = bytearray(zlib.decompress(bytes.fromhex(
                record["background_indices_zlib_hex"])))
            assert x1 - x0 - 4 <= 80 and y1 - y0 - 4 <= 12
            for y in range(y0 + 2, y1 - 2):
                for x in range(x0 + 2, x1 - 2):
                    rgb = samples[y - y0 - 2][x - x0 - 2]
                    background[(y - by) * (ex - bx) + x - bx] = colors[rgb]
            record["background_indices_zlib_hex"] = zlib.compress(background, 9).hex()
            record["research_texture_source"] = "clean towninfo Share blank strips"
            rows.append({"id": record["id"], "english": record["text"],
                         "plaque_box": record["plaque_box"], "box": record["box"]})
        batch["scope"] = "RESEARCH ONLY: original grain, existing ink and bevel"
        batch["style_donor"] = "work/clean.nds towninfo Share blank strips"
        batch_path = ROOT / f"{group}_RESEARCH_ONLY.json"
        batch_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
        data, ids = apply_pxl_native_label_batch(batch_path, parent_data,
                                               base.read_file("/__arm9__.bin"))
        result = PxlImage.from_bytes(data)
        # Outer background rectangles can overlap another plaque's last rows.
        # Finish all interiors after the batch's erase/draw passes, retaining ink.
        for row in rows:
            x0, y0, x1, y1 = row["plaque_box"]
            for y in range(y0 + 2, y1 - 2):
                for x in range(x0 + 2, x1 - 2):
                    position = y * result.width + x
                    if result.indices[position] != batch["color_index"]:
                        rgb = samples[y - y0 - 2][x - x0 - 2]
                        result.indices[position] = colors[rgb]
        data = result.to_bytes()
        assert data[:parent.pixels_offset] == parent_data[:parent.pixels_offset]
        allowed = set()
        for row in rows:
            x0, y0, x1, y1 = row["plaque_box"]
            region = [y * old.width + x for y in range(y0, y1) for x in range(x0, x1)]
            # Independent preservation check: exact complete English ink mask.
            assert [p for p in region if old.indices[p] == 1] == [
                p for p in region if result.indices[p] == 1], row["id"]
            interior = {y * old.width + x for y in range(y0 + 2, y1 - 2)
                        for x in range(x0 + 2, x1 - 2)}
            assert all(old.indices[p] == result.indices[p] for p in region
                       if p not in interior), row["id"]
            allowed.update(interior)
        assert all(a == b for p, (a, b) in enumerate(zip(old.indices, result.indices))
                   if p not in allowed)
        (ROOT / f"{group}_RESEARCH_ONLY.pxl").write_bytes(data)
        sheet = Image.new("RGB", (1050, len(rows) * 130 + 35), (40, 45, 50))
        draw = ImageDraw.Draw(sheet)
        for col, label in enumerate(["Japanese source", "V540", "Source grain prototype"]):
            draw.text((col * 350 + 8, 8), label, fill="white")
        for n, row in enumerate(rows):
            for col, image in enumerate([original, old, result]):
                box = row["box"]
                crop = image.render().crop(box).convert("RGB")
                crop = crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.NEAREST)
                sheet.paste(crop, (col * 350 + 8, n * 130 + 55))
            draw.text((8, n * 130 + 35), row["english"], fill="white")
        sheet.save(ROOT / f"{group}_source_grain_review.png")
        proofs.append({"group": group, "file_path": file_path, "ids": ids,
                       "complete_english_masks_preserved": len(rows),
                       "palette_header_dimensions_preserved": True,
                       "all_current_bevel_pixels_preserved": True,
                       "all_pixels_outside_plaque_interiors_preserved": True,
                       "maximum_palette_channel_error": max(abs(
                           parent.palette[colors[rgb]][k] - rgb[k])
                           for row in samples for rgb in row for k in range(3)),
                       "prototype_sha256": digest(data)})
    proof = {"format": "dk4-plaque-source-texture-prototype-v541",
             "source_rom_sha256": CLEAN_SHA, "current_rom_sha256": CURRENT_SHA,
             "source_file": "/_pxl/towninfo.pxl",
             "source_blank_bounds": [[2, 62, 43, 74], [85, 62, 124, 74]],
             "groups": proofs, "production_rom_or_batches_modified": False,
             "source_strips_joined_at_column": 41,
             "overlapping_outer_backgrounds_resolved_after_label_draw": True,
             "remaining": ["Review strip join and texture against individual originals",
                           "Audit all other plaques, including inherited town labels",
                           "Correct dynamic equipment heading and item hints",
                           "Register, integrate and verify actual native rendering"],
             "all18_entries_remain_incomplete": True}
    (ROOT / "source_texture_prototype_proof.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof))


if __name__ == "__main__":
    main()
