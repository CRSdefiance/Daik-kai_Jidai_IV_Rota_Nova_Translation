"""Clarify the enthusiastic Mood label in its existing eight-byte slot."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = "ea0d189f495cf8f6ba06fa9313ada05eef810bdfc8339378fec9e030aca9449c"
OFFSET = 0x1482F4
POINTER_FIELD = 0x1483B0


def transform(source, clean):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V272 ARM9 required")
    if clean[OFFSET:OFFSET + 8] != "ハイ".encode("cp932") + bytes(4):
        raise ValueError("Original elevated Mood caption differs")
    if source[OFFSET:OFFSET + 8] != b"High\0\0\0\0":
        raise ValueError("Current elevated Mood caption differs")
    if struct.unpack_from("<I", source, POINTER_FIELD)[0] != 0x02000000 + OFFSET:
        raise ValueError("Native Mood table pointer differs")
    target = bytearray(source)
    target[OFFSET:OFFSET + 8] = b"Excited\0"
    saved = bytes(target)
    assert saved[:OFFSET] == source[:OFFSET]
    assert saved[OFFSET + 8:] == source[OFFSET + 8:]
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
                   "source_Japanese": "ハイ", "previous_English": "High", "English": "Excited",
                   "offset": OFFSET, "source_pointer_field": POINTER_FIELD,
                   "eight_byte_slot_all_native_code_other_strings_and_tables_unchanged": True,
                   "changed_records": ["DK4_SAILOR_MOOD_EXCITED_CAPTION"]}


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-sailor-mood-caption-release-v1":
        raise ValueError("Unknown sailor Mood caption release")
    saved, plan = transform(source, clean)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Sailor Mood caption target differs")
    return saved, plan
