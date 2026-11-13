"""Clarify the native L/R sail-angle caption without changing its footprint."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = "acbc7b631431cdfed20e499b5ab3563a1ea5a4a37c83def1ab64e37676349b71"
OFFSET = 0x147928
POINTER_FIELD = 0x119138


def transform(source, clean):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V263 ARM9 required")
    if clean[OFFSET:OFFSET + 8] != "帆回転".encode("cp932") + b"\0\0":
        raise ValueError("Original sail-rotation caption differs")
    if source[OFFSET:OFFSET + 8] != b"Rotate\0\0":
        raise ValueError("Current L/R caption differs")
    if struct.unpack_from("<I", source, POINTER_FIELD)[0] != 0x02000000 + OFFSET:
        raise ValueError("Native caption table pointer differs")
    target = bytearray(source)
    # Six stored cells retain the existing footer measure and pair phase.
    # The last cell is blank; all five visible letters are complete.
    target[OFFSET:OFFSET + 8] = b"Sails \0\0"
    saved = bytes(target)
    assert saved[:OFFSET] == source[:OFFSET] and saved[OFFSET + 8:] == source[OFFSET + 8:]
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
                   "source_Japanese": "帆回転", "English": "Sails", "stored": "Sails ",
                   "offset": OFFSET, "source_pointer_field": POINTER_FIELD,
                   "six_cell_footprint_and_all_native_code_unchanged": True,
                   "changed_records": ["DK4_SEA_SAIL_ANGLE_CAPTION"]}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-sail-angle-caption-release-v1":
        raise ValueError("Unknown sail-angle caption release")
    saved, plan = transform(source, clean)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Sail-angle caption target differs")
    return saved, plan
