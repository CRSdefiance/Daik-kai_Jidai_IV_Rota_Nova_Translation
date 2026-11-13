"""Pixel-exact design proposals only; never writes a font patch or ROM."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/punctuation_proposals_20261027')
ROM = Path('out/font_v2_punctuation_one_pixel_20261027_test.nds')
PROPOSALS = {
    ';': dict(name='Semicolon', note='Full comma tail;\nsingle upper dot.', sample='Wait; sail on.',
              rows=['......'] * 3 + ['.#....'] + ['......'] * 4 + ['##....', '.#....', '#.....']),
    '"': dict(name='Double quotes', note='Two separate\ncurved strokes.', sample='"Aye!" she said.',
              rows=['##.##.', '.#..#.', '#..#..'] + ['......'] * 8),
    '.': dict(name='Period', note='One baseline dot,\nmatching the new ?.', sample='Aye. Sail on.',
              rows=['......'] * 8 + ['#.....'] + ['......'] * 2),
    '!': dict(name='Exclamation', note='Shorter stem; same\ndot and gap as ?.', sample='Aye! Ready?',
              rows=['..#...'] * 6 + ['......', '......', '..#...', '......', '......']),
    '~': dict(name='Tilde (optional)', note='Wavy option; original\nmay be an overline.', sample='~ 10 days ~',
              rows=['......'] * 3 + ['.#..#.', '#.##..'] + ['......'] * 6),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def raster(font, text):
    image = Image.new('RGB', (len(text) * 6, 12), '#ecdfbd')
    for i, char in enumerate(text):
        glyph = font.decode(char)
        for y in range(11):
            for x in range(6):
                if glyph.getpixel((x, y)):
                    image.putpixel((i * 6 + x, y + 1), (20, 28, 20))
    return image


def grid(sheet, font, char, left, top):
    scale = 8
    draw = ImageDraw.Draw(sheet)
    glyph = raster(font, char)
    sheet.paste(glyph.resize((48, 96), Image.Resampling.NEAREST), (left, top))
    for x in range(7):
        draw.line((left + x * scale, top, left + x * scale, top + 96), fill='#c1b89e')
    for y in range(13):
        draw.line((left, top + y * scale, left + 48, top + y * scale), fill='#c1b89e')
    # Boundary below raw glyph baseline row8, including the shared +1 offset.
    draw.line((left - 5, top + 80, left + 53, top + 80), fill='#217aae', width=2)


if __name__ == '__main__':
    ROOT.mkdir(parents=True, exist_ok=True)
    data = ROM.read_bytes()
    assert sha(data) == '9c2494830c3a60655fb09ab5cc67842851cbdbe8609083084ec447b81b363258'
    old = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    proposed = bytearray(old.glyphs)
    audit = []
    for char, item in PROPOSALS.items():
        rows = item['rows']
        assert len(rows) == 11 and all(len(row) == 6 and not set(row) - {'.', '#'} for row in rows)
        start = (ord(char) - 33) * 11
        proposed[start:start + 11] = bytes(sum(0x80 >> x for x, value in enumerate(row) if value == '#') for row in rows)
        glyph = old.decode(char)
        audit.append(dict(character=char, **item, before_rows=[
            ''.join('#' if glyph.getpixel((x, y)) else '.' for x in range(6)) for y in range(11)]))
    new = GameAsciiFont(bytes(proposed))
    title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 30)
    heading = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
    normal = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    small = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
    sheet = Image.new('RGB', (1320, 1120), '#17252b')
    draw = ImageDraw.Draw(sheet)
    draw.text((26, 18), 'Other punctuation: current font and proposed revisions', font=title, fill='#ffffff')
    draw.text((26, 60), 'Exact game pixels enlarged. Same 6-pixel advance, +1 drawing offset and line spacing.', font=normal, fill='#cbd8dc')
    draw.text((240, 100), 'BEFORE / current test ROM', font=heading, fill='#cbd8dc')
    draw.text((800, 100), 'AFTER / proposal only', font=heading, fill='#9bdfc2')
    for i, (char, item) in enumerate(PROPOSALS.items()):
        top = 145 + i * 180
        draw.rounded_rectangle((16, top, 1303, top + 166), radius=8, fill='#22343b')
        draw.text((30, top + 16), item['name'], font=heading, fill='#ffffff')
        draw.multiline_text((30, top + 55), item['note'], font=normal, fill='#cbd8dc', spacing=5)
        for x, font in [(245, old), (805, new)]:
            grid(sheet, font, char, x, top + 26)
            sample = raster(font, item['sample'])
            sheet.paste(sample.resize((sample.width * 4, 48), Image.Resampling.NEAREST), (x + 87, top + 44))
            draw.text((x + 87, top + 108), '4x context; enlarged glyph at left', font=small, fill='#afc0c7')
    draw.text((26, 1060), 'Blue line = baseline guide. All proposals fit the existing font cell.', font=normal, fill='#a9c7de')
    draw.text((26, 1088), 'Preview only: these five revisions have not been applied to a ROM.', font=normal, fill='#cbd8dc')
    sheet.save(ROOT / 'other_punctuation_before_after.png')
    # A second sheet removes guides and grids to judge clean in-game shapes.
    clean = Image.new('RGB', (1320, 770), '#17252b')
    d = ImageDraw.Draw(clean)
    d.text((26, 18), 'Punctuation proposals in text', font=title, fill='white')
    d.text((240, 75), 'BEFORE', font=heading, fill='#cbd8dc')
    d.text((800, 75), 'PROPOSED', font=heading, fill='#9bdfc2')
    for i, (char, item) in enumerate(PROPOSALS.items()):
        top = 125 + i * 118
        d.text((26, top + 12), item['name'], font=heading, fill='white')
        for x, font in [(240, old), (800, new)]:
            sample = raster(font, item['sample'])
            clean.paste(sample.resize((sample.width * 5, 60), Image.Resampling.NEAREST), (x, top))
    d.text((26, 735), 'Same +1 drawing offset throughout. Preview only; no ROM changes.', font=normal, fill='#cbd8dc')
    clean.save(ROOT / 'other_punctuation_text_comparison.png')
    (ROOT / 'proposals.json').write_text(json.dumps(dict(source_ROM=str(ROM), source_ROM_sha256=sha(data),
        source_font_sha256=sha(old.glyphs), drawing_offset_y=1, glyph_width=6, glyph_height=11,
        ROM_modified=False, proposals=audit, tilde_conditional_on_legacy_mapping=True), indent=2) + '\n', encoding='utf-8')
    assert ROM.read_bytes() == data
    print('Saved exact before/after proposals; source ROM is unchanged.')
