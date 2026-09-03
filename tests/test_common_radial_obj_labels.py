from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_obj_label_batch

BASE = Path("out/raphael_natural_v2_pre_extras_common_v6_accepted_rollback.nds")
BATCH = Path("translations/common_radial_obj_labels_v3.json")
EXPECTED_SHA256 = "39f92594251194f27252e70d08d48610649947809294fb390c976df91f3bff99"


def _decode_bank(data: bytes, bank: int) -> list[list[int]]:
    pixels = [[0] * 64 for _ in range(32)]
    for tile_y in range(4):
        for tile_x in range(8):
            tile_index = bank * 32 + tile_y * 8 + tile_x
            tile = data[tile_index * 32 : tile_index * 32 + 32]
            for y in range(8):
                for pair, value in enumerate(tile[y * 4 : y * 4 + 4]):
                    x = tile_x * 8 + pair * 2
                    pixels[tile_y * 8 + y][x] = value & 0x0F
                    pixels[tile_y * 8 + y][x + 1] = value >> 4
    return pixels


def test_common_radial_labels_preserve_art_and_use_the_native_font() -> None:
    image = NdsImage.open(BASE)
    source = image.read_file("/GRP/DSOBJ.DK4")
    arm9 = image.read_file("/__arm9__.bin")
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    assert hashlib.sha256(source).hexdigest() == batch["source_file_sha256"]

    rebuilt, ids = apply_obj_label_batch(BATCH, source, arm9)
    assert len(rebuilt) == len(source)
    assert len(ids) == 6
    assert hashlib.sha256(rebuilt).hexdigest() == EXPECTED_SHA256
    assert rebuilt[0x1800:] == source[0x1800:]

    font = GameAsciiFont.from_arm9(arm9)
    for bank, record in enumerate(batch["records"]):
        assert rebuilt[bank * 0x400 + 0x300 : bank * 0x400 + 0x400] == source[
            bank * 0x400 + 0x300 : bank * 0x400 + 0x400
        ]
        before = _decode_bank(source, bank)
        after = _decode_bank(rebuilt, bank)
        text = record["text"]
        text_x = (64 - len(text) * 5) // 2
        english_pixels: set[tuple[int, int]] = set()
        for character_index, character in enumerate(text):
            glyph = font.decode(character).load()
            for y in range(11):
                for x in range(5):
                    if glyph[x, y]:
                        point = (text_x + character_index * 5 + x, 6 + y)
                        english_pixels.add(point)
                        assert after[point[1]][point[0]] == 15

        for y in range(32):
            for x in range(64):
                if not (3 <= x < 61 and 5 <= y < 18):
                    assert after[y][x] == before[y][x]
                if (
                    3 <= x < 61
                    and 5 <= y < 18
                    and before[y][x] == 15
                    and (x, y) not in english_pixels
                ):
                    assert after[y][x] != 15
