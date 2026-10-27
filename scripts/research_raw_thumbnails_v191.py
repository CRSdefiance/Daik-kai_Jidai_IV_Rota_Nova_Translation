"""Source-pinned palette-prefix landmark thumbnails; geometry remains interpreted."""

import hashlib
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.rom.nds import NdsImage

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE = Path("out/all_routes_combined_v189_candidate.nds")
ROOT = Path("work/qa/raw_palette_prefix_v191")
REPORT = Path("work/analysis/raw_thumbnails_v191.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(CANDIDATE.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    base, candidate = NdsImage.open(BASE), NdsImage.open(CANDIDATE)
    raw = IlnkContainer.parse(base.read_file("/GRP/SLACKIMG.DK4")).blocks[18]
    saved = IlnkContainer.parse(candidate.read_file("/GRP/SLACKIMG.DK4")).blocks[18]
    assert raw == saved and len(raw) == 512 + 19 * 64 * 48
    palette = raw[:512]
    words = [value for value, in struct.iter_unpack("<H", palette)]
    assert len(words) == 256 and all(value < 0x8000 for value in words)
    colors = [bgr555(value) for value in words]
    ROOT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1320, 880), "#333333")
    draw = ImageDraw.Draw(sheet)
    rebuilt = bytearray(palette)
    rows = []
    for index in range(19):
        offset = 512 + index * 3072
        indices = raw[offset : offset + 3072]
        image = Image.new("RGBA", (64, 48))
        image.putdata([colors[value] for value in indices])
        path = ROOT / f"thumbnail_{index:02d}.png"
        image.save(path)
        assert Image.open(path).convert("RGBA").tobytes() == image.tobytes()
        x, y = index % 5 * 264, index // 5 * 220
        draw.text((x + 4, y + 4), f"Raw18 proposed thumbnail {index}", fill="white")
        sheet.paste(image.resize((256, 192), Image.Resampling.NEAREST).convert("RGB"), (x + 4, y + 24))
        rebuilt.extend(indices)
        rows.append({"index": index, "offset": offset, "bytes": len(indices), "indices_sha256": sha(indices), "preview": str(path), "preview_sha256": sha(path.read_bytes()), "visual_review": "pending", "native_geometry_palette_usage_proved": False})
    assert bytes(rebuilt) == raw
    sheet_path = ROOT / "thumbnail_review.png"
    sheet.save(sheet_path)
    result = {
        "status": "complete-prefix-palette-storage-interpretation",
        "path": "/GRP/SLACKIMG.DK4",
        "block_index": 18,
        "source_block_sha256": sha(raw),
        "source_palette_sha256": sha(palette),
        "candidate_sha256": sha(CANDIDATE.read_bytes()),
        "candidate_block_unchanged": True,
        "palette_bytes": 512,
        "hypothesis_dimensions_per_image": [64, 48],
        "hypothesis_image_count": 19,
        "whole_block_roundtrip_exact": True,
        "native_geometry_palette_alpha_use_proved": False,
        "records": rows,
        "review_sheet": str(sheet_path),
        "review_sheet_sha256": sha(sheet_path.read_bytes()),
        "historical_unclassified_counts_unchanged": True,
        "limits": ["Palette-prefix, 19-image partition and dimensions are observed coherent interpretations, not declared native metadata.", "Original small architectural details may remain indistinct; no exact landmark names, city assignments or tiny plaque readings are inferred."],
        "rom_changed": False,
    }
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Saved all 19 complete landmark thumbnail interpretations with exact palette/index/whole-block identities.")


if __name__ == "__main__":
    main()
