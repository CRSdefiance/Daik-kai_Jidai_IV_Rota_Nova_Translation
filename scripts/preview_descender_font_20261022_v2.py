"""Pixel-exact font design mockup; writes preview assets, never a ROM."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.dialogue.codec import parse_markup, tokens_to_bytes
from dk4tool.dialogue.font_audit import ASCII_FONT_OFFSET, GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels, raster

OUT = Path('work/font_descender_mockup_20261022_v2')
ROM = Path('out/screenshot_text_repairs_20261022_centered_candidate.nds')
TAILS = {
    'g': ['......'] * 3 + ['.###..', '#..#..', '#..#..', '#..#..', '.###..', '...#..', '#..#..', '.##...'],
    'j': ['..#...', '..#...', '......', '..#...', '..#...', '..#...', '..#...', '..#...', '..#...', '#.#...', '.#....'],
    'p': ['......'] * 3 + ['###...', '#..#..', '#..#..', '#..#..', '###...', '#.....', '#.....', '#.....'],
    'q': ['......'] * 3 + ['.###..', '#..#..', '#..#..', '#..#..', '.###..', '...#..', '...#..', '...#..'],
    'y': ['......'] * 3 + ['#..#..', '#..#..', '#..#..', '.#.#..', '..#...', '..#...', '.#....', '#.....'],
}
PUNCTUATION = {
    '[': ['...##.'] + ['...#..'] * 9 + ['...##.'],
    ']': ['##....'] + ['.#....'] * 9 + ['##....'],
    '(': ['....#.', '...#..', '...#..', '..#...', '..#...', '..#...', '..#...', '..#...', '...#..', '...#..', '....#.'],
    ')': ['#.....', '.#....', '.#....', '..#...', '..#...', '..#...', '..#...', '..#...', '.#....', '.#....', '#.....'],
    '{': ['...##.', '...#..', '...#..', '...#..', '...#..', '..#...', '...#..', '...#..', '...#..', '...#..', '...##.'],
    '}': ['##....', '.#....', '.#....', '.#....', '.#....', '..#...', '.#....', '.#....', '.#....', '.#....', '##....'],
    '$': ['..#...', '.###..', '#.#.#.', '#.#.#.', '.##...', '..##..', '..#.#.', '#.#.#.', '#.#.#.', '.###..', '..#...'],
    '_': ['......'] * 10 + ['#####.'],
}
REDRAWS = {**TAILS, **PUNCTUATION}
PAPER, INK = '#efe8c9', '#081008'
BACKGROUND, MUTED, ACCENT = '#17252b', '#b4c5c9', '#81d8c3'


def ui_font(size, bold=False):
    name = 'segoeuib.ttf' if bold else 'segoeui.ttf'
    return ImageFont.truetype(str(Path('C:/Windows/Fonts') / name), size)


def draw_label(draw, xy, text, size=18, fill='white', bold=False):
    draw.text(xy, text, font=ui_font(size, bold), fill=fill)


def render_line(font, text, scale=3):
    result = Image.new('RGB', (max(1, len(text) * 6), 16), PAPER)
    for index, character in enumerate(text):
        result.paste(INK, (index * 6, 0), font.decode(character))
    return result.resize((result.width * scale, result.height * scale), Image.Resampling.NEAREST)


def edited_font(original):
    data = bytearray(original.glyphs)
    shifts = {}
    for code in range(33, 127):
        character = chr(code)
        old = original.decode(character)
        box = old.getbbox()
        shift = min(2, box[1]) if box else 0
        shifts[character] = shift
        new = Image.new('1', (6, 11))
        for y in range(11 - shift):
            for x in range(6):
                new.putpixel((x, y), old.getpixel((x, y + shift)))
        # Taller punctuation moves by one row so no original ink is cropped.
        assert sum(bool(new.getpixel((x, y))) for y in range(11) for x in range(6)) == sum(
            bool(old.getpixel((x, y))) for y in range(11) for x in range(6))
        if character in REDRAWS:
            rows = REDRAWS[character]
            assert len(rows) == 11 and all(len(row) == 6 for row in rows)
            new = Image.new('1', (6, 11))
            for y, row in enumerate(rows):
                for x, value in enumerate(row):
                    new.putpixel((x, y), value == '#')
        offset = (code - 33) * 11
        data[offset:offset + 11] = bytes(sum(0x80 >> x for x in range(6) if new.getpixel((x, y)))
                                         for y in range(11))
    return GameAsciiFont(bytes(data)), shifts


def overview(original, proposed, before_native, after_native):
    sheet = Image.new('RGB', (1440, 1240), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    draw_label(draw, (44, 24), 'FONT MOCKUP / LETTERS + SYMBOLS', 32, bold=True)
    draw_label(draw, (44, 69), 'Actual game pixels • font design mockup v2 • no ROM changes', 18, MUTED)
    columns = [(44, 'ORIGINAL', original, before_native), (742, 'PROPOSED', proposed, after_native)]
    for x, title, font, native in columns:
        draw.rounded_rectangle((x, 112, x + 654, 1188), radius=14, fill='#23363c')
        draw_label(draw, (x + 24, 129), title, 23, ACCENT if title == 'PROPOSED' else 'white', True)
        subtitle = 'Original baseline and stored letterforms' if title == 'ORIGINAL' else 'Raised baseline; descenders and symbols completed'
        draw_label(draw, (x + 24, 166), subtitle, 17, MUTED)
        draw_label(draw, (x + 24, 214), 'ALPHABET  /  3× pixels', 15, MUTED, True)
        lines = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz', '0123456789  !?.,:;\'"-', '()[]{} /\\ +-= @#$%&*']
        y = 247
        for text in lines:
            panel = Image.new('RGB', (606, 54), PAPER)
            panel.paste(render_line(font, text), (12, 6))
            sheet.paste(panel, (x + 24, y))
            y += 62
        draw_label(draw, (x + 24, 523), 'DESCENDERS IN WORDS  /  4× pixels', 15, MUTED, True)
        for y, text in [(558, 'g j p q y'), (630, 'away  flying  judging')]:
            panel = Image.new('RGB', (606, 64), PAPER)
            panel.paste(render_line(font, text, 4), (12, 0))
            sheet.paste(panel, (x + 24, y))
        draw_label(draw, (x + 24, 732), 'SAMPLE DIALOGUE  /  2× native renderer pixels', 15, MUTED, True)
        panel = Image.new('RGB', (606, 176), PAPER)
        panel.paste(native.resize((432, 128), Image.Resampling.NEAREST), (22, 22))
        sheet.paste(panel, (x + 24, 769))
        draw_label(draw, (x + 24, 976), 'READING SAMPLE  /  2× pixels', 15, MUTED, True)
        panel = Image.new('RGB', (606, 134), PAPER)
        for row, text in enumerate(['Quickly, bring my spyglass!', 'Can you judge this cargo, Rafael?', 'Faticia: Yes. Enjoy your voyage!']):
            panel.paste(render_line(font, text, 2), (14, 14 + row * 34))
        sheet.paste(panel, (x + 24, 1012))
    draw_label(draw, (44, 1201), 'Same 6×11 cell, 6 px advance and 16 px line spacing. Enlarged with nearest-neighbor scaling.', 17, MUTED)
    sheet.save(OUT / 'font_before_after.png')


def pixel_grid(original, proposed):
    scale, margin = 14, 40
    sheet = Image.new('RGB', (1440, 448), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    draw_label(draw, (40, 18), 'THE FIVE REDRAWN DESCENDERS', 27, bold=True)
    draw_label(draw, (40, 60), 'Red line: baseline. Teal pixels: the proposed tail below that baseline. One square = one game pixel.', 17, MUTED)
    for column, character in enumerate('gjpqy'):
        left = margin + column * 280
        draw_label(draw, (left, 99), character, 29, ACCENT, True)
        for index, (label, font, baseline) in enumerate([('Original', original, 10), ('Proposed', proposed, 8)]):
            x, y = left + index * 122, 173
            draw_label(draw, (x, 145), label, 15, MUTED)
            glyph = font.decode(character)
            for yy in range(11):
                for xx in range(6):
                    color = '#f0ead8'
                    if glyph.getpixel((xx, yy)):
                        color = '#127765' if index == 1 and yy > baseline else INK
                    draw.rectangle((x + xx * scale, y + yy * scale,
                                    x + (xx + 1) * scale - 1, y + (yy + 1) * scale - 1),
                                   fill=color, outline='#aab3ad')
            line_y = y + (baseline + 1) * scale
            draw.line((x - 5, line_y, x + 6 * scale + 4, line_y), fill='#e96d69', width=2)
        draw_label(draw, (left, 348), '6 px wide × 11 px high', 15, MUTED)
    draw_label(draw, (40, 403), 'Design proposal: letterforms can be refined independently before any in-game font replacement.', 18, MUTED)
    sheet.save(OUT / 'descender_pixel_grid.png')


def symbol_sheet(original, proposed):
    sheet = Image.new('RGB', (1440, 920), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    draw_label(draw, (40, 20), 'COMPLETE SYMBOLS / MOCKUP v2', 30, bold=True)
    draw_label(draw, (40, 66), 'Original source pixels on the left of each pair; completed symbols on the right.', 18, MUTED)
    for number, character in enumerate(PUNCTUATION):
        left, top = 40 + number % 4 * 350, 108 + number // 4 * 282
        draw_label(draw, (left, top), character, 26, ACCENT, True)
        for index, (label, font) in enumerate([('Original', original), ('Proposed', proposed)]):
            x, y, scale = left + index * 126, top + 66, 13
            draw_label(draw, (x, top + 36), label, 15, MUTED)
            glyph = font.decode(character)
            old_shifted = Image.new('1', (6, 11))
            source_glyph = original.decode(character)
            for yy in range(10):
                for xx in range(6):
                    old_shifted.putpixel((xx, yy), source_glyph.getpixel((xx, yy + 1)))
            for yy in range(11):
                for xx in range(6):
                    ink = bool(glyph.getpixel((xx, yy)))
                    added = index == 1 and ink and not old_shifted.getpixel((xx, yy))
                    color = '#127765' if added else INK if ink else '#efe8c9'
                    draw.rectangle((x + xx * scale, y + yy * scale,
                                    x + (xx + 1) * scale - 1, y + (yy + 1) * scale - 1),
                                   fill=color, outline='#aab3ad')
        draw_label(draw, (left, top + 220), '6 x 11 pixels; same character advance', 14, MUTED)
    draw_label(draw, (40, 676), 'SYMBOLS IN CONTEXT / 3x PIXELS', 16, MUTED, True)
    sample = '[gyp] (Ready) {Yes} $100 _'
    for x, label, font in [(40, 'ORIGINAL', original), (742, 'PROPOSED', proposed)]:
        draw_label(draw, (x, 714), label, 18, ACCENT if label == 'PROPOSED' else 'white', True)
        panel = Image.new('RGB', (654, 80), PAPER)
        panel.paste(render_line(font, sample, 3), (18, 16))
        sheet.paste(panel, (x, 750))
    draw_label(draw, (40, 861), 'Teal: restored bottom strokes. The original underscore is blank; this proposal makes it visible.', 17, MUTED)
    sheet.save(OUT / 'symbols_before_after.png')


def main():
    OUT.mkdir(exist_ok=True)
    image = NdsImage.open(ROM)
    arm = image.read_file('/__arm9__.bin')
    original = GameAsciiFont.from_arm9(arm)
    proposed, shifts = edited_font(original)
    proposed_arm = bytearray(arm)
    proposed_arm[ASCII_FONT_OFFSET:ASCII_FONT_OFFSET + len(proposed.glyphs)] = proposed.glyphs
    sample = "I hear it's an enormous spear{LB}capable of driving evil away.{LB}Quickly, bring my spyglass!{LB}Can you judge this cargo, Rafael?"
    raw = tokens_to_bytes(parse_markup(sample), guard_linebreaks=True, pair_phase_safe_breaks=True)
    native_images = []
    checks = []
    for name, data in [('original', arm), ('proposed', bytes(proposed_arm))]:
        pixels, events, kanji = raster(data, raw)
        assert pixels == expected_pixels(data, kanji, events)
        semantic = [ord(c) for c in raw.decode() if c not in ' \n']
        assert semantic == [e['code'] for e in events if e['code'] != 32]
        assert sorted({e['y'] for e in events if e['code'] != 32}) == [0, 16, 32, 48]
        picture = Image.new('RGB', (216, 64))
        picture.putdata([(8, 16, 8) if p else (239, 232, 201) for p in pixels])
        picture.save(OUT / f'{name}_native_sample.png')
        native_images.append(picture)
        checks.append({'font': name, 'complete_native_and_independent_pixels_match': True,
                       'complete_glyph_order_and_four_rows_intact': True})
    for name, data in [('original', arm), ('proposed', bytes(proposed_arm))]:
        pixels, events, kanji = raster(data, b'[gyp] (Ready) {Yes} $100 _')
        assert pixels == expected_pixels(data, kanji, events)
        assert [e['code'] for e in events if e['code'] != 32] == [ord(c) for c in '[gyp](Ready){Yes}$100_']
        checks.append({'font': name, 'complete_symbol_native_and_independent_pixels_match': True})
    for character in '[](){}$':
        glyph = proposed.decode(character)
        assert any(glyph.getpixel((x, 0)) for x in range(6))
        assert [glyph.getpixel((x, 0)) for x in range(6)] == [glyph.getpixel((x, 10)) for x in range(6)]
    assert proposed.decode('_').getbbox() == (0, 10, 5, 11)
    overview(original, proposed, *native_images)
    pixel_grid(original, proposed)
    symbol_sheet(original, proposed)
    (OUT / 'original_ascii_font.bin').write_bytes(original.glyphs)
    (OUT / 'proposed_ascii_font.bin').write_bytes(proposed.glyphs)
    report = {'scope': 'Font design mockup only; original native painter executed on temporary in-memory font bytes. No ROM written or release registered.',
              'cell': [6, 11], 'character_advance': 6, 'line_spacing': 16,
              'ordinary_glyph_shift': 2, 'tall_punctuation_shift': 1,
              'redrawn_glyph_rows': REDRAWS, 'non_redrawn_glyph_ink_retained': True,
              'per_character_shift': shifts, 'native_checks': checks,
              'source_ROM': str(ROM), 'source_ROM_sha256': hashlib.sha256(ROM.read_bytes()).hexdigest(),
              'original_font_sha256': hashlib.sha256(original.glyphs).hexdigest(),
              'proposed_font_sha256': hashlib.sha256(proposed.glyphs).hexdigest(),
              'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / 'mockup_specification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Created font_before_after.png and descender_pixel_grid.png; both native sample planes pass independent pixel checks. No ROM changed.')


if __name__ == '__main__':
    main()
