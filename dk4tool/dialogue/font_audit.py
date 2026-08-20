from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

ASCII_FONT_OFFSET = 0x125A60
ASCII_FIRST_CODE = 0x21
ASCII_LAST_CODE = 0x7F
ASCII_GLYPH_WIDTH = 6
ASCII_GLYPH_HEIGHT = 11
ASCII_BYTES_PER_GLYPH = 11
SJIS_MAP_OFFSET = 0x125EC4
SJIS_GLYPH_COUNT = 3340
REFERENCE_ASCII_FONT_SHA256 = (
    "427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058"
)
REFERENCE_KANJI_FONT_SHA256 = (
    "41b9f2f2da08e7fc80715506614dd4d0c18365b78cd89ff5982f2f9e7de3b669"
)

_RENDERER_SIGNATURES = {
    0xD1674: bytes.fromhex("0C5085E2"),  # add r5, r5, #12 after Shift-JIS glyph
    0xD169C: bytes.fromhex("065085E2"),  # add r5, r5, #6 after ASCII glyph
    0xD1748: bytes.fromhex("0B0051E3"),  # 11 bitmap rows, direct-color path
    0xD1804: bytes.fromhex("0B005AE3"),  # 11 bitmap rows, paletted path
    0xD1828: bytes.fromhex("210050E3"),  # first embedded ASCII glyph is '!'
    0xD1830: bytes.fromhex("7F0050E3"),  # final embedded ASCII glyph is DEL
    0xD1840: bytes.fromhex("0B20A0E3"),  # 11 bytes per ASCII glyph
}


@dataclass(frozen=True)
class GameAsciiFont:
    glyphs: bytes

    @classmethod
    def from_arm9(cls, arm9: bytes) -> GameAsciiFont:
        glyph_count = ASCII_LAST_CODE - ASCII_FIRST_CODE + 1
        end = ASCII_FONT_OFFSET + glyph_count * ASCII_BYTES_PER_GLYPH
        if end > len(arm9):
            raise ValueError("ARM9 is too short to contain the DK4 ASCII font table")
        glyphs = arm9[ASCII_FONT_OFFSET:end]
        if not any(glyphs):
            raise ValueError("DK4 ASCII font table is blank at the expected ARM9 offset")
        return cls(glyphs)

    def decode(self, character: str) -> Image.Image:
        if len(character) != 1:
            raise ValueError("decode expects one character")
        code = ord(character)
        image = Image.new("1", (ASCII_GLYPH_WIDTH, ASCII_GLYPH_HEIGHT), 0)
        if code == 0x20:
            return image
        if not ASCII_FIRST_CODE <= code <= ASCII_LAST_CODE:
            raise ValueError(f"character is outside the DK4 ASCII table: {character!r}")
        start = (code - ASCII_FIRST_CODE) * ASCII_BYTES_PER_GLYPH
        rows = self.glyphs[start : start + ASCII_BYTES_PER_GLYPH]
        pixels = image.load()
        for y, value in enumerate(rows):
            for x in range(ASCII_GLYPH_WIDTH):
                pixels[x, y] = bool(value & (0x80 >> x))
        return image


def audit_standard_font(arm9: bytes, kanji_font: bytes) -> dict[str, object]:
    signature_checks = {
        f"arm9+0x{offset:X}": arm9[offset : offset + len(expected)] == expected
        for offset, expected in _RENDERER_SIGNATURES.items()
    }
    map_end = SJIS_MAP_OFFSET + SJIS_GLYPH_COUNT * 2
    if map_end > len(arm9):
        raise ValueError("ARM9 is too short to contain the DK4 Shift-JIS glyph map")
    mapping = struct.unpack_from(f"<{SJIS_GLYPH_COUNT}H", arm9, SJIS_MAP_OFFSET)
    expected_kanji_size = SJIS_GLYPH_COUNT * RawFontGeometry().bytes_per_cell
    ascii_end = ASCII_FONT_OFFSET + (
        ASCII_LAST_CODE - ASCII_FIRST_CODE + 1
    ) * ASCII_BYTES_PER_GLYPH
    ascii_font = arm9[ASCII_FONT_OFFSET:ascii_end]
    ascii_hash = hashlib.sha256(ascii_font).hexdigest()
    kanji_hash = hashlib.sha256(kanji_font).hexdigest()
    return {
        "format": "dk4-standard-font-audit-v1",
        "all_renderer_signatures_match": all(signature_checks.values()),
        "renderer_signatures": signature_checks,
        "ascii": {
            "arm9_offset": ASCII_FONT_OFFSET,
            "first_code": ASCII_FIRST_CODE,
            "last_code": ASCII_LAST_CODE,
            "glyph_count": ASCII_LAST_CODE - ASCII_FIRST_CODE + 1,
            "glyph_width_px": ASCII_GLYPH_WIDTH,
            "glyph_height_px": ASCII_GLYPH_HEIGHT,
            "advance_px": 6,
            "fixed_width": True,
            "sha256": ascii_hash,
            "matches_clean_reference": ascii_hash == REFERENCE_ASCII_FONT_SHA256,
        },
        "shift_jis": {
            "arm9_map_offset": SJIS_MAP_OFFSET,
            "glyph_count": len(mapping),
            "map_sorted": list(mapping) == sorted(mapping),
            "first_code": mapping[0],
            "last_code": mapping[-1],
            "glyph_width_px": 16,
            "glyph_height_px": RawFontGeometry().cell_height,
            "record_bytes": RawFontGeometry().bytes_per_cell,
            "advance_px": 12,
            "font_file_size": len(kanji_font),
            "expected_font_file_size": expected_kanji_size,
            "font_size_matches_map": len(kanji_font) == expected_kanji_size,
            "sha256": kanji_hash,
            "matches_clean_reference": kanji_hash == REFERENCE_KANJI_FONT_SHA256,
        },
        "layout": {
            "line_pitch_px": 16,
            "story_dialogue_content_width_px": 216,
            "story_dialogue_ascii_cells": 36,
            "shared_dialogue_content_width_px": 216,
            "shared_dialogue_ascii_cells": 36,
            "story_content_width_source": "cold-boot SC0 Raphael 38/39-cell boundary probe",
            "shared_content_width_source": "cold-boot Market Info 38-cell boundary probe",
        },
    }


@dataclass(frozen=True)
class RawFontGeometry:
    cell_width: int = 16
    cell_height: int = 11
    bytes_per_cell: int = 22
    bit_order: str = "msb"


RAW_FONT_GEOMETRY = RawFontGeometry()


def glyph_count(data: bytes, geometry: RawFontGeometry = RAW_FONT_GEOMETRY) -> int:
    return len(data) // geometry.bytes_per_cell


def decode_glyph(
    data: bytes,
    index: int,
    geometry: RawFontGeometry = RAW_FONT_GEOMETRY,
) -> Image.Image:
    start = index * geometry.bytes_per_cell
    end = start + geometry.bytes_per_cell
    if index < 0 or end > len(data):
        raise IndexError(f"glyph index {index} is outside the font")

    cell = data[start:end]
    image = Image.new("1", (geometry.cell_width, geometry.cell_height), 0)
    pixels = image.load()
    row_bytes = geometry.cell_width // 8
    for y in range(geometry.cell_height):
        for byte_x in range(row_bytes):
            value = cell[y * row_bytes + byte_x]
            for bit in range(8):
                shift = 7 - bit if geometry.bit_order == "msb" else bit
                pixels[byte_x * 8 + bit, y] = bool(value & (1 << shift))
    return image


def render_font_atlas(
    font_path: Path,
    output_path: Path,
    *,
    start: int = 0,
    count: int = 256,
    columns: int = 16,
    scale: int = 2,
    geometry: RawFontGeometry = RAW_FONT_GEOMETRY,
) -> None:
    data = font_path.read_bytes()
    available = glyph_count(data, geometry)
    if start < 0 or start >= available:
        raise ValueError(f"start must be between 0 and {available - 1}")
    count = min(count, available - start)
    rows = (count + columns - 1) // columns
    label_height = 10
    slot_width = geometry.cell_width * scale
    slot_height = geometry.cell_height * scale + label_height
    atlas = Image.new("RGB", (columns * slot_width, rows * slot_height), "white")
    draw = ImageDraw.Draw(atlas)

    for offset in range(count):
        index = start + offset
        x = (offset % columns) * slot_width
        y = (offset // columns) * slot_height
        glyph = decode_glyph(data, index, geometry).resize(
            (geometry.cell_width * scale, geometry.cell_height * scale),
            resample=Image.Resampling.NEAREST,
        )
        atlas.paste(glyph.convert("RGB"), (x, y))
        draw.text((x + 1, y + geometry.cell_height * scale), f"{index:04X}", fill="black")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output_path)
