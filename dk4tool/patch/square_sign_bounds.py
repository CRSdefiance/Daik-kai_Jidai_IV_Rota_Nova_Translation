"""Keep selectable Square rows as wide as their complete caption backing."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = "aad56e57a642445c46a7cd5b5b26130e1ecebec502ececcbe17be87bbdd10265"
OFFSET = 0x118DAC
ROOT = Path("work/analysis/square_sign_bounds_v254")


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V253 ARM9 required")
    if struct.unpack_from("<4I", source, OFFSET - 8) != (20, 0, 100, 0):
        raise ValueError("Original Square row rectangle differs")
    # The one native reference loads this rectangle for all Square sign rows.
    references = [o for o in range(0, len(source) - 3, 4)
                  if struct.unpack_from("<I", source, o)[0] == 0x02118DA4]
    if references != [0x5F1E8]:
        raise ValueError("Square rectangle is no longer caller-private")
    saved = bytearray(source)
    struct.pack_into("<I", saved, OFFSET, 116)
    saved = bytes(saved)
    assert saved[:OFFSET] == source[:OFFSET] and saved[OFFSET + 4:] == source[OFFSET + 4:]
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
                   "row_rectangle_before": [20, 0, 100, 0],
                   "row_rectangle_after": [20, 0, 116, 0],
                   "native_reference": references[0], "changed_word_offset": OFFSET,
                   "only_four_byte_row_right_coordinate_changed": True,
                   "window_border_and_original_choice_menu_placement_preserved": True}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-square-sign-bounds-release-v1":
        raise ValueError("Unknown Square sign bounds release")
    saved, plan = transform(source)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Square bounds target differs")
    plan["changed_records"] = ["DK4_SQUARE_COMPLETE_CAPTION_ROW_BOUNDS_V1"]
    return saved, plan
