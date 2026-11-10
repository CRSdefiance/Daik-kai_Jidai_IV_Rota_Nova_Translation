"""Two owned bitmap glyphs; preserve the one-pixel painter and every layout byte."""

import json
from pathlib import Path

from dk4tool.dialogue.font_audit import ASCII_FONT_OFFSET, GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha


GLYPHS = {
    ',': ['......'] * 8 + ['##....', '.#....', '#.....'],
    '?': ['.##...', '#..#..', '...#..', '...#..', '..#...', '..#...',
          '......', '......', '..#...', '......', '......'],
}


def propose(source):
    target = bytearray(source)
    spans = []
    for char, rows in GLYPHS.items():
        if len(rows) != 11 or any(len(row) != 6 or set(row) - {'.', '#'} for row in rows):
            raise ValueError('Invalid 6x11 punctuation bitmap')
        at = ASCII_FONT_OFFSET + (ord(char) - 33) * 11
        bitmap = bytes(sum(0x80 >> x for x, value in enumerate(row) if value == '#') for row in rows)
        spans.append(dict(character=char, offset=at, before_hex=source[at:at + 11].hex(), after_hex=bitmap.hex()))
        target[at:at + 11] = bitmap
    owned = {i for span in spans for i in range(span['offset'], span['offset'] + 11)}
    if any(source[i] != target[i] for i in range(len(source)) if i not in owned):
        raise ValueError('Unexpected bytes outside the two glyphs')
    target = bytes(target)
    proof = dict(source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        source_font_sha256=sha(GameAsciiFont.from_arm9(source).glyphs),
        target_font_sha256=sha(GameAsciiFont.from_arm9(target).glyphs),
        glyph_spans=spans, changed_records=['ASCII_COMMA_FULL_TAIL', 'ASCII_QUESTION_CLEAR_HOOK_DOT'],
        all_other_glyphs_code_offsets_advances_and_line_spacing_unchanged=True)
    return target, proof


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-ascii-punctuation-20261027-v1':
        raise ValueError('Unsupported punctuation release')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError('Punctuation dependency changed: ' + name)
    if sha(source) != config['source_ARM9_sha256']:
        raise ValueError('Exact registered one-pixel predecessor required')
    target, proof = propose(source)
    if proof != config['proof'] or sha(target) != config['target_ARM9_sha256']:
        raise ValueError('Punctuation successor differs from registered proof')
    return target, proof
