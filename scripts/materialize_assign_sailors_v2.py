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
SOURCE_PXL_SHA256 = "a3441a625a853bf05f70d57599f8565535aba0f119147e40ed38fd55c2dc29ef"
ARM9_SHA256 = "249860ab1d29ecfa8e149fd04b5cbff3c3414fb192f81459cfaf469d6c83fa52"
FONT_SHA256 = "427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058"

# The outer box restores the complete original plaque, including its folded
# left edge. The inner box is the safe text band and deliberately stops before
# the live numeric value drawn by the game.
LABELS = (
    ("DK4_ASSIGN_FLEET_CREW_V2", (5, 14, 88, 36), (8, 15, 85, 35), "Fleet Crew"),
    ("DK4_ASSIGN_UNASSIGNED_V2", (132, 14, 216, 36), (135, 15, 213, 35), "Unassigned"),
    ("DK4_ASSIGN_RANGE_V2", (5, 37, 88, 60), (8, 38, 85, 58), "Range"),
    ("DK4_ASSIGN_MARINES_V2", (5, 100, 68, 120), (8, 101, 65, 119), "Marines"),
    ("DK4_ASSIGN_CANNON_V2", (84, 100, 124, 120), (86, 101, 122, 119), "Cannon"),
    ("DK4_ASSIGN_LATEEN_V2", (5, 120, 68, 142), (8, 122, 65, 140), "Lateen"),
    ("DK4_ASSIGN_SQUARE_V2", (132, 120, 196, 142), (135, 122, 193, 140), "Square"),
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
    parser = argparse.ArgumentParser(
        description="Materialize the refined Assign Sailors labels and range formatter."
    )
    parser.add_argument("--rom", type=Path, default=BASE_ROM)
    parser.add_argument(
        "--pxl-out",
        type=Path,
        default=Path("translations/assign_sailors_graphics_v2.json"),
    )
    parser.add_argument(
        "--arm9-out",
        type=Path,
        default=Path("translations/assign_sailors_arm9_v2.json"),
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    base = NdsImage.open(args.rom)
    source_pxl = base.read_file("/_pxl/dividecrewinfo.pxl")
    arm9 = base.read_file("/__arm9__.bin")
    if sha256(source_pxl) != SOURCE_PXL_SHA256:
        raise SystemExit("wrong accepted Assign Sailors atlas")
    if sha256(arm9) != ARM9_SHA256:
        raise SystemExit("wrong accepted ARM9 component")

    # The accepted V1 atlas has the original plaque frames and text-free
    # interiors, but its caption boxes and terminology need refinement. Use it
    # as the reconstruction parent so no antialiased Japanese shadow pixels are
    # reintroduced from the pristine atlas.
    rows: list[dict[str, object]] = []
    for record_id, box, draw_box, text in LABELS:
        left, top, right, bottom = box
        background = PxlImage.from_bytes(source_pxl)
        background.erase_palette_indices(draw_box, {1})
        rows.append(
            {
                "id": record_id,
                "box": [left, top, right, bottom],
                "draw_box": list(draw_box),
                "background_indices_zlib_hex": zlib.compress(box_indices(background, box), 9).hex(),
                "text": text,
            }
        )

    pxl_batch = {
        "format": "dk4-pxl-native-label-batch-v1",
        "file_path": "/_pxl/dividecrewinfo.pxl",
        "source_file_sha256": SOURCE_PXL_SHA256,
        "font_file_path": "/__arm9__.bin",
        "font_sha256": FONT_SHA256,
        "target_locale": "en-US",
        "scope": "Refined source-art Assign Sailors plaques with aligned native captions",
        "glyph_width": 5,
        "advance": 5,
        "color_index": 1,
        "erase_palette_indices": [1],
        "records": rows,
    }
    args.pxl_out.write_text(
        json.dumps(pxl_batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    offset = 0x133FF4
    expected = arm9[offset : offset + 8]
    if expected.rstrip(b"\0") != b"~%d d":
        raise SystemExit(f"unexpected accepted range formatter: {expected!r}")
    arm9_batch = {
        "format": "dk4-arm9-fixed-text-batch-v1",
        "file_path": "/__arm9__.bin",
        "source_file_sha256": ARM9_SHA256,
        "target_locale": "en-US",
        "scope": "Unambiguous Assign Sailors voyage-range value",
        "records": [
            {
                "id": "DK4_ASSIGN_RANGE_FORMAT_V2",
                "offset": offset,
                "source_hex": expected.hex().upper(),
                "english": "%d days",
                "encoding": "ascii",
                "context": "Assign Sailors range value; replaces the tilde that looked like a stray dash",
            }
        ],
    }
    args.arm9_out.write_text(
        json.dumps(arm9_batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.pxl_out}: {len(rows)} refined plaques")
    print(f"wrote {args.arm9_out}: readable voyage-range formatter")


if __name__ == "__main__":
    main()
