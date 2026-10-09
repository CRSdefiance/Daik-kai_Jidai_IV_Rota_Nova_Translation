"""Prepare complete source-cell reviews for the real item and trade PXL atlases."""

import json
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/common_atlas_consumers_v210/source_reviews")


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open("out/all_routes_combined_v205_candidate.nds")
    source = NdsImage.open("work/clean.nds")
    rows = []
    for path, size, count in (("/_pxl/item.pxl", 32, 218), ("/_pxl/itemtrade.pxl", 24, 124),
                              ("/_pxl/item16.pxl", 16, 218), ("/_pxl/itemtrade16.pxl", 16, 124)):
        data = rom.read_file(path)
        assert data == source.read_file(path)
        image = PxlImage.from_bytes(data)
        assert (image.width, image.height) == (size, count * size)
        complete = image.render().convert("RGB")
        stem = Path(path).stem
        cells = []
        for index in range(count):
            cell = complete.crop((0, index * size, size, (index + 1) * size))
            file = ROOT / f"{stem}_{index:03d}.png"
            cell.save(file)
            with Image.open(file) as saved:
                assert saved.tobytes() == cell.tobytes()
            cells.append({"index": index, "PNG": file.as_posix(), "PNG_sha256": sha(file.read_bytes()),
                          "indices_sha256": sha(image.indices[index * size * size:(index + 1) * size * size]),
                          "complete_extent": [size, size], "visual_review": "pending"})
        sheets = []
        for first in range(0, count, 80):
            batch = cells[first:first + 80]
            slot = size * 3 + 8
            pitch = size * 3 + 26
            sheet = Image.new("RGB", (10 * slot, ((len(batch) + 9) // 10) * pitch), (220, 220, 220))
            draw = ImageDraw.Draw(sheet)
            for index, row in enumerate(batch):
                x, y = index % 10 * slot, index // 10 * pitch
                draw.text((x + 2, y + 2), str(row["index"]), fill=(0, 0, 0))
                with Image.open(row["PNG"]) as cell:
                    sheet.paste(cell.resize((size * 3, size * 3), Image.Resampling.NEAREST), (x + 2, y + 20))
            file = ROOT / f"{stem}_review_{first // 80}.png"
            sheet.save(file)
            sheets.append({"PNG": file.as_posix(), "PNG_sha256": sha(file.read_bytes()),
                           "first": first, "last": first + len(batch) - 1, "visual_review": "pending"})
        rows.append({"path": path, "source_sha256": sha(data), "complete_cells": cells,
                     "review_sheets": sheets, "all_source_indices_and_palette_preserved": True,
                     "alpha_not_inferred_from_RGB_review": True})
    result = {"format": "dk4-native-atlas-source-review-v1", "atlases": rows,
              "complete_cells": sum(len(row["complete_cells"]) for row in rows),
              "native_source_color_views_only_not_GPU_or_alpha_proof": True}
    (ROOT / "inventory.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_cells": result["complete_cells"], "sheets": sum(len(r["review_sheets"]) for r in rows)}))


if __name__ == "__main__":
    main()
