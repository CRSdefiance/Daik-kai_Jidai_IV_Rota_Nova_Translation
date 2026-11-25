"""Expose every previously reduced asset at source size, without resampling.

Historical contact sheets cap previews at 272x342. Most images were never reduced;
their review evidence must not be called full-resolution merely because this
geometry passes. Actual visual review remains explicit and separate.
"""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/graphics_resolution_v230")
CURRENT = Path("out/all_routes_combined_v218_candidate.nds")
CURRENT_SHA = "be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f"


def save_view(name, panels):
    width = max(120, max(im.width for _, im, _ in panels))
    height = max(im.height for _, im, _ in panels) + 28
    columns = min(4, len(panels))
    rows = (len(panels) + columns - 1) // columns
    page = Image.new("RGB", (columns * (width + 8), rows * height), "#303030")
    draw = ImageDraw.Draw(page)
    regions = []
    for i, (label, im, record) in enumerate(panels):
        x, y = i % columns * (width + 8), i // columns * height
        draw.text((x + 2, y + 2), label, fill="white")
        page.paste(im.convert("RGB"), (x, y + 24))
        regions.append({**record, "canvas_box": [x, y + 24, x + im.width, y + 24 + im.height],
                        "RGB_pixels_sha256": sha(im.convert("RGB").tobytes())})
    path = ROOT / (name + ".png")
    page.save(path)
    saved = Image.open(path).convert("RGB")
    if any(sha(saved.crop(tuple(region["canvas_box"])).tobytes()) != region["RGB_pixels_sha256"]
           for region in regions):
        raise ValueError("Saved review sheet changes/crops original source pixels")
    return {"path": path.as_posix(), "sha256": sha(path.read_bytes()),
            "source_regions": regions, "all_saved_source_regions_pixel_exact": True,
            "resampling_used": False, "visually_reviewed": False}


def main():
    if sha(CURRENT.read_bytes()) != CURRENT_SHA:
        raise ValueError("Current registered ROM identity differs")
    ROOT.mkdir(parents=True, exist_ok=True)
    inventory_path = Path("work/analysis/graphics_v150/inventory.json")
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    historical_audit = json.loads(Path("translations/graphics_visual_audit_v150.json").read_text(encoding="utf-8"))
    if len(inventory["assets"]) != 921 or historical_audit["unreviewed_rendered_assets"] != 0:
        raise ValueError("Historical inventory/review-count evidence differs")
    reduced = [r for r in inventory["assets"] if r["width"] > 272 or r["height"] > 342]
    if len(reduced) != 29:
        raise ValueError("Historical reduced-asset census differs")
    current, clean = NdsImage.open(CURRENT), NdsImage.open("work/clean.nds")
    records, sheets, deck = [], [], []
    for row in reduced:
        path, texture_index = row["path"], row["texture_index"]
        raw, original = current.read_file(path), clean.read_file(path)
        if texture_index is None:
            if raw != original or sha(raw) != row["sha256"]:
                raise ValueError(f"Unchanged PXL source/current/historical lock differs: {path}")
            image = PxlImage.from_bytes(raw)
            if image.to_bytes() != raw:
                raise ValueError("Palette/index source reconstruction differs")
            rendered = image.render()
        else:
            archive = FlsArchive(raw)
            image = archive.texture(texture_index)
            source_image = FlsArchive(original).texture(texture_index)
            if (image.flags != source_image.flags or image.palette != source_image.palette
                    or image.indices != source_image.indices
                    or (image.width, image.height) != (source_image.width, source_image.height)):
                raise ValueError("Selected FLS asset differs from its complete clean source")
            # Original LZ10 streams need not use our encoder's byte choices.
            # Check complete decoded slot identity rather than rewriting the
            # source to make an unnecessary compressed-byte assertion pass.
            roundtrip = FlsArchive(archive.to_bytes()).texture(texture_index)
            if (roundtrip.flags != image.flags or roundtrip.palette != image.palette
                    or roundtrip.indices != image.indices
                    or (roundtrip.width, roundtrip.height) != (image.width, image.height)):
                raise ValueError("FLS decoded source reconstruction differs")
            rendered = image.render()
        if rendered.size != (row["width"], row["height"]):
            raise ValueError("Current decoded extent differs from historical review")
        historical_preview = Image.open(row["preview"]).convert("RGBA")
        if historical_preview.size != rendered.size or historical_preview.tobytes() != rendered.tobytes():
            raise ValueError("Selected asset's complete historical/native-size preview pixels differ")
        rendered_path = ROOT / f"asset_{row['asset_id']:04d}_full.png"
        rendered.save(rendered_path)
        record = {"asset_id": row["asset_id"], "path": path, "texture_index": texture_index,
                  "current_file_sha256": sha(raw), "clean_file_sha256": sha(original),
                  "historical_file_sha256": row["sha256"], "whole_file_equals_clean": raw == original,
                  "selected_asset_equals_clean_and_historical_pixels": True, "dimensions": list(rendered.size),
                  "full_preview": rendered_path.as_posix(), "full_preview_sha256": sha(rendered_path.read_bytes()),
                  "source_asset_palette_indices_dimensions_and_flags_exact": True,
                  "full_resolution_visual_review": False}
        records.append(record)
        if path.startswith("/_pxl/deckchip"):
            deck.append((path.split("/")[-1], rendered, {"asset_id": row["asset_id"], "box": [0, 0, rendered.width, rendered.height]}))
        elif path in {"/_pxl/item.pxl", "/_pxl/item16.pxl", "/_pxl/itemtrade.pxl", "/_pxl/itemtrade16.pxl"}:
            record["existing_full_cell_review"] = "docs/common_atlas_consumers_v210.md"
            record["existing_cell_review_is_source_content_not_all_runtime_clearance"] = True
        elif rendered.width <= 256 and rendered.height > 342:
            # Pure presentation windows, not a guessed native frame/record layout.
            # Overlap keeps small lettering crossing a window edge visible.
            panels = []
            for top in range(0, rendered.height, 256):
                lo, hi = max(0, top - 16), min(rendered.height, top + 256 + 16)
                panels.append((f"{Path(path).stem} y{lo}-{hi}", rendered.crop((0, lo, rendered.width, hi)),
                               {"asset_id": row["asset_id"], "box": [0, lo, rendered.width, hi]}))
            for start in range(0, len(panels), 4):
                sheets.append(save_view(f"{Path(path).stem}_windows_{start // 4}", panels[start:start + 4]))
        else:
            sheets.append(save_view(f"asset_{row['asset_id']:04d}_review", [(path.split("/")[-1], rendered,
                                                                           {"asset_id": row["asset_id"], "box": [0, 0, rendered.width, rendered.height]})]))
    for start in range(0, len(deck), 4):
        # Two columns at native304x240 keep each page below screen-preview limits.
        first = save_view(f"deck_maps_{start // 4}_a", deck[start:start + 2])
        second = save_view(f"deck_maps_{start // 4}_b", deck[start + 2:start + 4])
        sheets.extend([first, second])
    result = {"format": "dk4-full-resolution-gap-review-v230", "ROM_sha256": CURRENT_SHA,
              "historical_inventory_sha256": sha(inventory_path.read_bytes()),
              "historical_contact_bounds": [272, 342], "historical_assets": 921,
              "not_downsampled_by_historical_contact_geometry": 892,
              "previously_downsampled_assets": 29,
              "event_images": 243, "event_images_all_original_256x192": all(
                  (r["width"], r["height"]) == (256, 192) for r in inventory["assets"] if r["path"].startswith("/evstill/")),
              "records": records, "review_sheets": sheets,
              "source_size_geometry_does_not_itself_prove_editorial_review_or_native_composition": True,
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "full_resolution_inventory.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"historical_original_size": 892, "previously_reduced": len(records),
                      "new_source_size_review_sheets": len(sheets), "full_cell_review_already_exists": 4,
                      "all_selected_source_assets_exact": True, "ROM_modified": False}))


if __name__ == "__main__":
    main()
