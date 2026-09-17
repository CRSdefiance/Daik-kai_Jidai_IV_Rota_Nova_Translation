from __future__ import annotations

import argparse
import hashlib
import json
import zlib
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage


BASE_ROM = Path("out/raphael_natural_v2_pre_story_push_v10_accepted_rollback.nds")
BASE_SHA256 = "d8cb15aa23e2496510eba8feb18e4536a7da195522b7f5959298b0c1cc0fd1cf"
SOURCE_PXL_SHA256 = "5c975dbd84451f3dafb1f84516fae378e4d4e0f03572c531f9c8713fad2d6f26"
FONT_SHA256 = "427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058"

LABELS = (
    ("DK4_TOWNINFO_TYPE_NATIVE", (7, 19, 51, 36), "Type"),
    ("DK4_TOWNINFO_GROWTH_NATIVE", (135, 19, 175, 36), "Growth"),
    ("DK4_TOWNINFO_STATUS_NATIVE", (7, 39, 51, 56), "Status"),
    ("DK4_TOWNINFO_ARMS_NATIVE", (135, 39, 175, 56), "Arms"),
    ("DK4_TOWNINFO_SHARE_NATIVE", (39, 59, 89, 77), "Share"),
    ("DK4_TOWNINFO_SPECIALTY_NATIVE", (163, 59, 235, 77), "Specialty"),
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
    parser = argparse.ArgumentParser(description="Materialize native-font town-information plaques.")
    parser.add_argument("--rom", type=Path, default=BASE_ROM)
    parser.add_argument(
        "--out", type=Path, default=Path("translations/trading_towninfo_graphics_v2.json")
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    source_pxl = NdsImage.open(args.rom).read_file("/_pxl/towninfo.pxl")
    if sha256(source_pxl) != SOURCE_PXL_SHA256:
        raise SystemExit("wrong accepted towninfo atlas")

    # V1 is already baked into the accepted parent. Its English glyphs use
    # palette index 1, so reconstructing from that exact source removes only
    # the former text while retaining the plaque texture and shadows.
    background = PxlImage.from_bytes(source_pxl)
    rows: list[dict[str, object]] = []
    for record_id, box, text in LABELS:
        background.erase_palette_indices(box, {1})
        rows.append(
            {
                "id": record_id,
                "box": list(box),
                "background_indices_zlib_hex": zlib.compress(box_indices(background, box), 9).hex(),
                "text": text,
            }
        )

    batch = {
        "format": "dk4-pxl-native-label-batch-v1",
        "file_path": "/_pxl/towninfo.pxl",
        "source_file_sha256": SOURCE_PXL_SHA256,
        "font_file_path": "/__arm9__.bin",
        "font_sha256": FONT_SHA256,
        "target_locale": "en-US",
        "scope": "Crisp native-font port-information plaques on restored source textures",
        "glyph_width": 5,
        "advance": 5,
        "color_index": 1,
        "erase_palette_indices": [1],
        "records": rows,
    }
    args.out.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(rows)} native town-information plaques")


if __name__ == "__main__":
    main()
