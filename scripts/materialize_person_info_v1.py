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
PXL_PATH = "/_pxl/personinfo.pxl"
ARM9_PATH = "/__arm9__.bin"
PXL_SHA256 = "daf784c5ca545082922f62e01439d243e9cce4133b2797bcb2671eb142ec8eee"
ARM9_SHA256 = "9a79c25d4a7cf03678a8b5444c3f685a9f675be879109817adb01643141768f5"
FONT_SHA256 = "427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058"


PLAQUES = (
    ("DK4_PERSON_HEALTH_PLAQUE", (3, 103, 49, 118), "Health"),
    ("DK4_PERSON_MOOD_PLAQUE", (3, 123, 49, 138), "Mood"),
    ("DK4_PERSON_LEVEL_PLAQUE", (3, 143, 49, 158), "Level"),
    ("DK4_PERSON_HP_PLAQUE", (3, 163, 49, 178), "HP"),
)


ARM9_TEXT = (
    ("DK4_PERSON_STATUS_HEALTHY", 0x14827C, 8, "Healthy", "Healthy body condition"),
    ("DK4_PERSON_STATUS_DYING", 0x148284, 8, "Dying", "Near-death body condition"),
    ("DK4_PERSON_STAT_STAMINA", 0x14828C, 8, "Stamina", "Physical stamina stat"),
    ("DK4_PERSON_STATUS_SICK", 0x148294, 8, "Sick", "Illness body condition"),
    ("DK4_PERSON_STAT_AGILITY", 0x14829C, 8, "Agility", "Agility stat"),
    ("DK4_PERSON_STATUS_INJURED", 0x1482A4, 8, "Injured", "Severe-injury body condition"),
    ("DK4_PERSON_STATUS_TIRED", 0x1482AC, 8, "Tired", "Fatigue condition"),
    ("DK4_PERSON_STATUS_GOOD", 0x1482B4, 8, "Good", "Positive mood condition"),
    ("DK4_PERSON_STATUS_DAZED", 0x1482BC, 8, "Dazed", "Confused condition"),
    ("DK4_PERSON_STAT_SPIRIT", 0x1482C4, 8, "Spirit", "Spirit stat"),
    ("DK4_PERSON_STATUS_DEAD", 0x1482CC, 8, "Dead", "Dead condition"),
    ("DK4_PERSON_STATUS_RELAXED", 0x148368, 12, "Relaxed", "Relaxed mood condition"),
    ("DK4_PERSON_ROLE_ADMIRAL", 0x148498, 8, "Admiral", "Company leader role"),
    ("DK4_PERSON_ADMIRAL_FORMAT", 0x1484A0, 8, "%s Adm.", "Compact admiral title formatter"),
    ("DK4_PERSON_INFO_TITLE", 0x14852C, 16, "Sailor Info", "Info > Sailors screen title"),
    ("DK4_PERSON_EQUIPPED_ITEMS", 0x148CC8, 16, "Equipped Items", "Equipment-list heading"),
    ("DK4_PERSON_EQUIPPED_WEAPON", 0x148CD8, 12, "Weapon", "Equipped weapon heading"),
    ("DK4_PERSON_EQUIPPED_ARMOR", 0x148CE4, 12, "Armor", "Equipped armor heading"),
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
        "--graphics-out",
        type=Path,
        default=Path("translations/person_info_graphics_v1.json"),
    )
    parser.add_argument(
        "--arm9-out", type=Path, default=Path("translations/person_info_arm9_v1.json")
    )
    args = parser.parse_args()

    if sha256(args.rom.read_bytes()) != BASE_SHA256:
        raise SystemExit("wrong canonical accepted baseline")
    rom = NdsImage.open(args.rom)
    pxl = rom.read_file(PXL_PATH)
    arm9 = rom.read_file(ARM9_PATH)
    if sha256(pxl) != PXL_SHA256 or sha256(arm9) != ARM9_SHA256:
        raise SystemExit("accepted person-info source component mismatch")

    rows: list[dict[str, object]] = []
    for record_id, box, text in PLAQUES:
        background = PxlImage.from_bytes(pxl)
        background.erase_palette_indices(box, {1})
        rows.append(
            {
                "id": record_id,
                "box": list(box),
                "draw_box": list(box),
                "background_indices_zlib_hex": zlib.compress(
                    box_indices(background, box), 9
                ).hex(),
                "text": text,
            }
        )
    graphics = {
        "format": "dk4-pxl-native-label-batch-v1",
        "file_path": PXL_PATH,
        "source_file_sha256": PXL_SHA256,
        "font_file_path": ARM9_PATH,
        "font_sha256": FONT_SHA256,
        "target_locale": "en-US",
        "scope": "Aligned native-font Info > Sailors status plaques",
        "glyph_width": 5,
        "advance": 5,
        "color_index": 1,
        "erase_palette_indices": [1],
        "records": rows,
    }
    args.graphics_out.write_text(
        json.dumps(graphics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    text_rows: list[dict[str, object]] = []
    for record_id, offset, size, english, context in ARM9_TEXT:
        expected = arm9[offset : offset + size]
        encoded = english.encode("ascii")
        if len(encoded) >= size:
            raise ValueError(f"{record_id}: no room for a terminator")
        text_rows.append(
            {
                "id": record_id,
                "offset": offset,
                "source_hex": expected.hex().upper(),
                "english": english,
                "encoding": "ascii",
                "context": context,
            }
        )
    arm9_batch = {
        "format": "dk4-arm9-fixed-text-batch-v1",
        "file_path": ARM9_PATH,
        "source_file_sha256": ARM9_SHA256,
        "target_locale": "en-US",
        "scope": "Complete Info > Sailors headings, conditions, roles, and stats",
        "fixed_text_policy": {"require_c_string_termination": True},
        "records": text_rows,
    }
    args.arm9_out.write_text(
        json.dumps(arm9_batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.graphics_out}: {len(rows)} aligned plaques")
    print(f"wrote {args.arm9_out}: {len(text_rows)} runtime labels")


if __name__ == "__main__":
    main()
