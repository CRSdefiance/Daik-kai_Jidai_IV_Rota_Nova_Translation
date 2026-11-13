"""Fit the shared empty-player status within every original Grand Race card."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

SOURCE = "85d1b032ebdb16a4337f43de46b4bca4207b7ded8d763ef71eb1960791db0fe7"
BASE, ORIGINAL, OFFSET, POINTER = 0x02000000, 0x16BA34, 0x16B927, 0xFADDC
BEFORE, AFTER = b"Waiting for a player\0", b"Awaiting player\0"
JAPANESE = "-- 参加待ち --"


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError("Race waiting status requires the complete exact V599 ARM9")
    assert source[OFFSET:OFFSET + len(BEFORE)] == BEFORE
    assert struct.unpack_from("<I", source, POINTER)[0] == BASE + OFFSET
    clean_rom = NdsImage.open("work/clean.nds")
    clean = clean_rom.read_file("/__arm9__.bin")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/__arm9__.bin")
    original = JAPANESE.encode("cp932") + b"\0"
    assert clean[ORIGINAL:ORIGINAL + len(original)] == canonical[ORIGINAL:ORIGINAL + len(original)] == original
    # The fallback constructor and whole original painter, including all four
    # original card coordinates, remain source-identical. Only the display text
    # in the preceding source-owned UI pool is shortened.
    for lo, hi in ((0xFABB0, 0xFADD8), (0xD1604, 0xD16B4), (0x12EFB8, 0x12EFB8 + 96)):
        assert source[lo:hi] == clean[lo:hi]
    units = [(s.ramAddress, bytes(s.data)) for s in MainCodeFile(source, BASE).sections]
    units += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, f: clean_rom.rom.files[f]).values()]
    references = [(address + at, struct.unpack_from("<I", data, at)[0]) for address, data in units
                  for at in range(len(data) - 3)
                  if BASE + OFFSET <= struct.unpack_from("<I", data, at)[0] < BASE + OFFSET + len(BEFORE)]
    assert references == [(BASE + POINTER, BASE + OFFSET)], "Another pointer aliases the owned status span"
    result = bytearray(source)
    result[OFFSET:OFFSET + len(BEFORE)] = AFTER.ljust(len(BEFORE), b"\0")
    result = bytes(result)
    assert len(result) == len(source)
    assert result[:OFFSET] == source[:OFFSET] and result[OFFSET + len(BEFORE):] == source[OFFSET + len(BEFORE):]
    return result, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(result),
        "changed_records": ["GRAND_RACE_EMPTY_PLAYER_CARD_STATUS"], "source_Japanese": JAPANESE,
        "canonical_source_offset": ORIGINAL, "canonical_source_hex": original.hex(),
        "display_pool_span": [OFFSET, OFFSET + len(BEFORE)], "sole_original_pointer_field": POINTER,
        "before": BEFORE[:-1].decode("ascii"), "after": AFTER[:-1].decode("ascii"),
        "display_width_pixels_before": 120, "display_width_pixels_after": 90,
        "original_four_card_coordinates_painter_and_fallback_unchanged": True,
        "all_other_ROM_bytes_and_all_pointers_unchanged": True,
        "no_code_section_pool_growth_or_runtime_hooks": True, "status": "experimental", "full_goal_complete": False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    assert config["format"] == "dk4-race-waiting-label-v1"
    assert config["source_arm9_sha256"] == sha(source)
    result, report = transform(source)
    assert sha(result) == config["target_arm9_sha256"]
    assert config["English"] == AFTER[:-1].decode("ascii")
    return result, report
