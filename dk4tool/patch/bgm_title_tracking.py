"""Isolated research: use native tracking in the BGM draw-local text context."""
from __future__ import annotations

import hashlib
import struct

PATCH_OFFSET = 0x109280
SOURCE = bytes.fromhex('0610a0e3900101e0a10f81e0c000a0e1')
# mvn r2,#0; str r2,[sp,#0x1c]; add r1,r0,r0,lsl#2;
# asr r0,r1,#1. The following original rsb centers at x=64.
REPLACEMENT = struct.pack('<4I', 0xE3E02000, 0xE58D201C, 0xE0801100, 0xE1A000C1)
CODE_LOCKS = (
    (0x1091FC, 0x109310, '21b0e1c865b4d5e935177f36f6c6fcdca93f761bbd66ae7689462ee27db24846'),
    (0xD57C4, 0xD57FC, '088c78dc39b1ddde1851fcd756b713f87d51d7565baa5e480935d1aea078e825'),
    (0xD5A98, 0xD5AF4, '0e014b6669b5c1ea496ef829e1dd6fbb1b2053829753dac2d42ac1c103740a9b'),
)
FONT_OFFSET, FONT_SIZE = 0x125A60, 95 * 11
FONT_SHA = '427776b1266289206333d94cf27c292df0d15d6f26f7c52f3846fee641c32058'


def title_geometry(title: str, advance: int = 6) -> dict:
    raw = title.encode('ascii')
    if not raw or any(c < 32 or c >= 127 for c in raw):
        raise ValueError('A BGM title must contain only printable ASCII')
    if advance not in (5, 6):
        raise ValueError('Unmapped ASCII advance')
    width = len(raw) * advance
    left = 64 - width // 2
    return {'ascii_bytes': len(raw), 'width_pixels': width,
            'left': left, 'right': left + width,
            'fits_panel': left >= 0 and left + width <= 128}


def apply_probe(arm9: bytes) -> bytes:
    for lo, hi, expected in CODE_LOCKS:
        if hashlib.sha256(arm9[lo:hi]).hexdigest() != expected:
            raise ValueError(f'Mapped BGM/context code differs at {lo:#x}')
    font = arm9[FONT_OFFSET:FONT_OFFSET + FONT_SIZE]
    if hashlib.sha256(font).hexdigest() != FONT_SHA:
        raise ValueError('Mapped ASCII font differs')
    # Printable glyphs !..~ occupy at most the first five columns. DEL is
    # excluded, and manuscript ASCII validation forbids its use in titles.
    if any(row & 4 for row in font[:94 * 11]):
        raise ValueError('Five-pixel tracking would overlap a glyph')
    if arm9[PATCH_OFFSET:PATCH_OFFSET + len(SOURCE)] != SOURCE:
        raise ValueError('BGM title arithmetic differs')
    result = bytearray(arm9)
    result[PATCH_OFFSET:PATCH_OFFSET + len(SOURCE)] = REPLACEMENT
    return bytes(result)
