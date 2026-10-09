"""Recover complete common raw raster interpretations with exact source identities."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.rom.nds import NdsImage

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE = Path("out/all_routes_combined_v190_candidate.nds")
ROOT = Path("work/qa/common_raw_v194")
REPORT = Path("work/analysis/common_raw_v194.json")
SPECS = ((0, 512, 8, 56, 64, 178), (2, 512, 8, 24, 24, 100), (3, 32, 4, 304, 200, 8), (7, 512, 8, 32, 32, 188))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(CANDIDATE.read_bytes()) == "9ccff57aec0326722b89b85877fb5be23e63dc466022b1f7c2e0a984ccdd9424"
    source = IlnkContainer.parse(NdsImage.open(BASE).read_file("/GRP/CMMNIMG.DK4"))
    saved = IlnkContainer.parse(NdsImage.open(CANDIDATE).read_file("/GRP/CMMNIMG.DK4"))
    ROOT.mkdir(parents=True, exist_ok=True)
    blocks = []
    for block_index, palette_bytes, depth, width, height, count in SPECS:
        raw = source.blocks[block_index]
        assert raw == saved.blocks[block_index]
        palette = raw[:palette_bytes]
        words = [value for value, in struct.iter_unpack("<H", palette)]
        assert all(value < 0x8000 for value in words)
        colors = [bgr555(value) for value in words]
        packed = raw[palette_bytes:]
        indices = packed if depth == 8 else bytes(part for value in packed for part in (value & 15, value >> 4))
        assert len(indices) == width * height * count
        repacked = indices if depth == 8 else bytes(indices[i] | indices[i + 1] << 4 for i in range(0, len(indices), 2))
        assert palette + repacked == raw
        image = Image.new("RGBA", (width, height * count))
        image.putdata([colors[value] for value in indices])
        image_path = ROOT / f"block{block_index}_full.png"
        image.save(image_path)
        assert Image.open(image_path).tobytes() == image.tobytes()
        cells = []
        for index in range(count):
            start = index * width * height
            cell = image.crop((0, index * height, width, (index + 1) * height))
            cell_path = ROOT / f"block{block_index}_cell_{index:03d}.png"
            cell.save(cell_path)
            cells.append({"index": index, "index_offset": start, "index_bytes": width * height, "indices_sha256": sha(indices[start : start + width * height]), "preview": str(cell_path), "preview_sha256": sha(cell_path.read_bytes()), "visual_review": "pending"})
        # Bound each review sheet so every pixel is available at native scale or
        # an integer enlargement; do not downsample a large portrait catalogue.
        sheets = []
        batch = 40 if block_index != 3 else 8
        for begin in range(0, count, batch):
            scale = 2 if block_index == 0 else 3 if block_index in (2, 7) else 1
            columns = 10 if block_index != 3 else 4
            cw, ch = width * scale + 8, height * scale + 28
            slots = min(batch, count - begin)
            sheet = Image.new("RGB", (columns * cw, ((slots + columns - 1) // columns) * ch), "#333333")
            draw = ImageDraw.Draw(sheet)
            for slot, cell in enumerate(cells[begin : begin + batch]):
                x, y = slot % columns * cw, slot // columns * ch
                draw.text((x + 4, y + 3), str(cell["index"]), fill="white")
                preview = Image.open(cell["preview"]).convert("RGB").resize((width * scale, height * scale), Image.Resampling.NEAREST)
                sheet.paste(preview, (x + 4, y + 24))
            path = ROOT / f"block{block_index}_review_{begin // batch}.png"
            sheet.save(path)
            sheets.append({"path": str(path), "sha256": sha(path.read_bytes()), "first_cell": begin, "last_cell": begin + slots - 1, "visual_review": "pending"})
        blocks.append({"path": "/GRP/CMMNIMG.DK4", "block_index": block_index, "source_block_sha256": sha(raw), "source_bytes": len(raw), "palette_bytes_interpretation": palette_bytes, "palette_sha256": sha(palette), "depth_interpretation": depth, "cell_dimensions_interpretation": [width, height], "cell_count_interpretation": count, "whole_block_roundtrip_exact": True, "candidate_block_unchanged": True, "full_preview": str(image_path), "full_preview_sha256": sha(image_path.read_bytes()), "cells": cells, "review_sheets": sheets, "native_geometry_palette_alpha_usage_proved": False})
    result = {"status": "complete-bounded-raw-raster-interpretations-review-pending", "candidate_sha256": sha(CANDIDATE.read_bytes()), "blocks": blocks, "complete_cells": sum(row["cell_count_interpretation"] for row in blocks), "row_correlation_evidence": "work/analysis/common_raw_row_lags_v194.json", "native_loose_equivalence_claimed": False, "historical_unclassified_counts_unchanged": True, "rom_changed": False, "limits": ["Palette-prefix and cell geometries are coherent byte-exact interpretations, not declared native headers.", "Native loose item resources have additional icons and different palettes/indices; no exact loose-payload or live-portrait equality was established.", "Visual/source review does not prove native bank/alpha, resource use or full graphics clearance."]}
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {result['complete_cells']} complete cells on bounded, full-resolution review sheets.")


if __name__ == "__main__":
    main()
