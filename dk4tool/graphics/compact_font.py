"""Complete seven-row bitmap letters for fixed miniature image captions.

This authored face is baked into graphics only. It never replaces the game's
runtime font, and none of its shapes are cropped versions of native glyphs.
Unsupported letters fail rather than silently disappearing.
"""

import hashlib
import json

from PIL import Image

GLYPHS = {
    'C': ('0111', '1000', '1000', '1000', '1000', '1000', '0111'),
    'D': ('1110', '1001', '1001', '1001', '1001', '1001', '1110'),
    'P': ('1110', '1001', '1001', '1110', '1000', '1000', '1000'),
    'R': ('1110', '1001', '1001', '1110', '1010', '1001', '1001'),
    'S': ('0111', '1000', '1000', '0110', '0001', '0001', '1110'),
    'a': ('000', '000', '110', '001', '111', '101', '111'),
    'c': ('000', '000', '011', '100', '100', '100', '011'),
    'e': ('000', '000', '010', '101', '111', '100', '011'),
    'g': ('000', '000', '011', '101', '011', '001', '110'),
    'h': ('100', '100', '110', '101', '101', '101', '101'),
    'i': ('1', '0', '1', '1', '1', '1', '1'),
    'k': ('100', '100', '101', '110', '110', '101', '101'),
    'l': ('1', '1', '1', '1', '1', '1', '1'),
    'n': ('000', '000', '110', '101', '101', '101', '101'),
    'o': ('000', '000', '010', '101', '101', '101', '010'),
    'p': ('000', '000', '110', '101', '110', '100', '100'),
    'r': ('000', '000', '110', '101', '100', '100', '100'),
}
FONT_FACE = 'compact-en-7px-v1'
FONT_SHA256 = hashlib.sha256(json.dumps(GLYPHS, sort_keys=True, separators=(',', ':')).encode('ascii')).hexdigest()
DATE_FONT_FACE = 'compact-en-7px-v2'
DATE_GLYPHS = {**GLYPHS, 'M': ('10001', '11011', '10101', '10101', '10001', '10001', '10001')}
DATE_FONT_SHA256 = hashlib.sha256(json.dumps(DATE_GLYPHS, sort_keys=True, separators=(',', ':')).encode('ascii')).hexdigest()
GENDER_FONT_FACE = 'compact-en-7px-v3'
GENDER_GLYPHS = {
    **DATE_GLYPHS,
    '♂': ('0000111', '0000001', '0111011', '1000100', '1000100', '1000100', '0111000'),
    '♀': ('01110', '10001', '10001', '01110', '00100', '01110', '00100'),
}
GENDER_FONT_SHA256 = hashlib.sha256(json.dumps(GENDER_GLYPHS, sort_keys=True, separators=(',', ':')).encode('ascii')).hexdigest()
FONT_IDENTITIES = {FONT_FACE: FONT_SHA256, DATE_FONT_FACE: DATE_FONT_SHA256,
                   GENDER_FONT_FACE: GENDER_FONT_SHA256}
FONT_TABLES = {FONT_FACE: GLYPHS, DATE_FONT_FACE: DATE_GLYPHS, GENDER_FONT_FACE: GENDER_GLYPHS}


def glyph(character: str, *, font_face: str = FONT_FACE) -> Image.Image:
    if font_face not in FONT_IDENTITIES:
        raise ValueError('Unsupported compact font face')
    table = FONT_TABLES[font_face]
    if character == ' ':
        return Image.new('1', (2, 7))
    if character not in table:
        raise ValueError(f'Unsupported compact bitmap letter: {character!r}')
    rows = table[character]
    if len(rows) != 7 or any(len(row) != len(rows[0]) or set(row) - {'0', '1'} for row in rows):
        raise ValueError('Invalid complete compact glyph')
    image = Image.new('1', (len(rows[0]), 7))
    for y, row in enumerate(rows):
        for x, value in enumerate(row):
            image.putpixel((x, y), 255 if value == '1' else 0)
    return image


def layout(text: str, box: tuple[int, int, int, int], *, word_space_width: int = 2, font_face: str = FONT_FACE):
    """Center full cells with one separating column; never rescale or clip."""
    left, top, right, bottom = box
    if word_space_width not in (1, 2, 3):
        raise ValueError('Compact word space must be one to three blank columns')
    glyphs = [Image.new('1', (word_space_width, 7)) if c == ' ' else glyph(c, font_face=font_face) for c in text]
    width = sum(g.width for g in glyphs) + len(glyphs) - 1
    if not glyphs or width > right - left or 7 > bottom - top:
        raise ValueError(f'Complete compact label does not fit: {text!r}')
    x, y = left + (right - left - width) // 2, top + (bottom - top - 7) // 2
    bounds = (x, y, x + width, y + 7)
    canvas = Image.new('1', (right - left, bottom - top))
    origins = []
    for g in glyphs:
        canvas.paste(g, (x - left, y - top))
        origins.append((x, y))
        x += g.width + 1
    return canvas, bounds, origins
