"""Traced native Grand Race help layout and ASCII pair-buffer verification."""

from .codec import parse_markup, tokens_to_bytes
from .layout import format_markup
from .profiles import DialogueProfile

PROFILE = DialogueProfile(
    name='grand-race-help-research', window_width_px=252, max_lines=8,
    line_height_px=12, guard_linebreaks=True, pair_phase_safe_breaks=True,
    balanced_wrapping=True,
    metrics_source='Native startup 0x5CA8 sets 6/12; widget dimensions 0x3F1D8 and 0x3E4E0 set 252/108; body starts y=12.',
)


def model_native_ascii(raw):
    """Independent ASCII pair-buffer/cursor model of the accepted help context."""
    x, y = 0, 12
    pending = None
    draws = []
    for index, byte in enumerate(raw):
        if byte == 10:
            x, y = 0, y + 12
            continue
        if not 32 <= byte < 127:
            raise ValueError('Unexpected non-ASCII/control byte in native help body')
        if x >= 252 or y >= 108:
            raise ValueError('Native context would wrap or clip a body glyph')
        if pending is None:
            pending = (chr(byte), x, y)
        else:
            first, px, py = pending
            if px + 12 > 252 or py + 11 > 108:
                raise ValueError('Buffered ASCII pair crosses the native bounds')
            draws.extend(((first, px, py), (chr(byte), px + 6, py)))
            pending = None
        x += 6
        # Exact inherited D5544-D555C repair, applied after each ASCII byte.
        if index >= 1 and raw[index - 1:index + 1] == b'\n ' and x == 6:
            x = 0
    # Native D4D84 calls D4EC4 with space to flush a pending final glyph.
    if pending is not None:
        char, px, py = pending
        if px + 12 > 252 or py + 11 > 108:
            raise ValueError('Final ASCII pair flush exceeds bounds')
        draws.extend(((char, px, py), (' ', px + 6, py)))
    return draws


def format_page(english):
    if english != english.strip() or '\n' in english or '\r' in english or '  ' in english:
        raise ValueError('Author English as one paragraph without layout spaces')
    if any(not 32 <= ord(c) < 127 for c in english) or '{' in english or '}' in english:
        raise ValueError('Help manuscript must be printable ASCII prose')
    markup = format_markup(english, PROFILE)
    tokens = parse_markup(markup)
    raw = tokens_to_bytes(tokens, guard_linebreaks=True, pair_phase_safe_breaks=True)
    lines = [line.rstrip(b' ').decode('ascii') for line in raw.split(b'\n ')]
    if ' '.join(lines) != english:
        raise ValueError('Formatted page drops or alters manuscript words')
    if len(lines) > PROFILE.max_lines or any(not line for line in lines):
        raise ValueError('Page exceeds its eight body lines')
    draws = model_native_ascii(raw)
    for row, line in enumerate(lines):
        visible = [(char, x, y) for char, x, y in draws if y == 12 + row * 12 and char != ' ']
        expected = [(char, index * 6, 12 + row * 12) for index, char in enumerate(line) if char != ' ']
        if visible != expected:
            raise ValueError('Native pair model changes/drops a character or its position')
    return markup, raw, lines, draws
