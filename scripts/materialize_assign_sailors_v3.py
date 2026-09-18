from __future__ import annotations

import argparse
import hashlib
import json
import zlib
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage


BASE_ROM = Path("out/raphael_natural_v2_accepted_base.nds")
BASE_SHA256 = "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
FILE_PATH = "/_pxl/dividecrewinfo.pxl"
SOURCE_SHA256 = "cf98ac3ce2eec82f39f28300b810c023713d3f8b3ba7803725c0e7448f07f17d"
ARM9_SHA256 = "9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5"
FONT_SHA256 = "427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058"


# Short, parallel captions leave a consistent margin between the plaque text
# and the live numbers beside it. The text bands also share exact baselines by
# row, avoiding the one-pixel vertical drift in the earlier reconstruction.
LABELS = (
    ("DK4_ASSIGN_ASSIGNED_V3", (5, 14, 88, 36), (8, 15, 85, 35), "Assigned"),
    ("DK4_ASSIGN_RESERVE_V3", (132, 14, 216, 36), (135, 15, 213, 35), "Reserve"),
    ("DK4_ASSIGN_RANGE_V3", (5, 37, 88, 60), (8, 38, 85, 58), "Range"),
    ("DK4_ASSIGN_MARINES_V3", (5, 100, 68, 120), (8, 101, 65, 119), "Marines"),
    ("DK4_ASSIGN_GUNS_V3", (84, 100, 124, 120), (86, 101, 122, 119), "Guns"),
    ("DK4_ASSIGN_LATEEN_V3", (5, 120, 68, 142), (8, 122, 65, 140), "Lateen"),
    ("DK4_ASSIGN_SQUARE_V3", (132, 120, 196, 142), (135, 122, 193, 140), "Square"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def box_indices(image: PxlImage, box: tuple[int, int, int, int]) -> bytes:
    left, top, right, bottom = box
    return b"".join(
        bytes(image.indices[y * image.width + left : y * image.width + right])
        for y in range(top, bottom)
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, default=BASE_ROM)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("translations/assign_sailors_graphics_v3.json"),
    )
    args = parser.parse_args()
    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    rom = NdsImage.open(args.rom)
    source = rom.read_file(FILE_PATH)
    arm9 = rom.read_file("/__arm9__.bin")
    if sha256(source) != SOURCE_SHA256 or sha256(arm9) != ARM9_SHA256:
        raise SystemExit("accepted Assign Sailors source component mismatch")

    rows: list[dict[str, object]] = []
    for record_id, box, draw_box, text in LABELS:
        background = PxlImage.from_bytes(source)
        background.erase_palette_indices(draw_box, {1})
        rows.append(
            {
                "id": record_id,
                "box": list(box),
                "draw_box": list(draw_box),
                "background_indices_zlib_hex": zlib.compress(
                    box_indices(background, box), 9
                ).hex(),
                "text": text,
            }
        )
    batch = {
        "format": "dk4-pxl-native-label-batch-v1",
        "file_path": FILE_PATH,
        "source_file_sha256": SOURCE_SHA256,
        "font_file_path": "/__arm9__.bin",
        "font_sha256": FONT_SHA256,
        "target_locale": "en-US",
        "scope": "Compact, consistently aligned native-font Assign Sailors plaques",
        "glyph_width": 5,
        "advance": 5,
        "color_index": 1,
        "erase_palette_indices": [1],
        "records": rows,
    }
    args.out.write_text(
        json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.out}: {len(rows)} aligned captions")


if __name__ == "__main__":
    main()
