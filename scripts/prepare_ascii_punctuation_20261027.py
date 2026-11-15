"""Register an isolated successor and retain a pixel-exact punctuation audit."""

import copy
import json
import string
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_punctuation_20261027 import GLYPHS, propose
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/font_punctuation_20261027')
CONFIG = Path('translations/ascii_punctuation_20261027_v1.json')
PROFILE = 'font-v2-punctuation-one-pixel-20261027'
PARENT = Path('out/font_v2_draw_down_one_20261027_test.nds')
ROM = Path('out/font_v2_punctuation_one_pixel_20261027_test.nds')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def preview(source, target):
    old, new = GameAsciiFont.from_arm9(source), GameAsciiFont.from_arm9(target)
    label = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 21)
    def text(font, value, scale):
        image = Image.new('RGB', (len(value) * 6, 12), '#e8d8ac')
        for i, ch in enumerate(value):
            if ch == ' ':
                continue
            g = font.decode(ch)
            for y in range(11):
                for x in range(6):
                    if g.getpixel((x, y)):
                        image.putpixel((i * 6 + x, y + 1), (16, 24, 16))
        return image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    sheet = Image.new('RGB', (1100, 400), '#17252b')
    draw = ImageDraw.Draw(sheet)
    draw.text((20, 12), 'Actual 6 x 11 font pixels / both use the same +1 drawing offset', fill='white', font=label)
    for index, (font, name) in enumerate([(old, 'Before'), (new, 'After')]):
        y = 55 + index * 170
        draw.text((20, y), name + '    comma        question mark', fill='white', font=label)
        sheet.paste(text(font, ',  ?', 7), (20, y + 34))
        sheet.paste(text(font, 'Admiral, would you address the crew?', 3), (290, y + 40))
        sheet.paste(text(font, 'Aye, aye!  Everything correct?', 3), (290, y + 93))
    sheet.save(ROOT / 'punctuation_before_after.png')
    sheet = Image.new('RGB', (880, 590), '#17252b')
    draw = ImageDraw.Draw(sheet)
    draw.text((20, 12), 'Punctuation audit: only comma and question mark changed', fill='white', font=label)
    for i, ch in enumerate(string.punctuation):
        x, y = 20 + i % 8 * 107, 65 + i // 8 * 126
        draw.text((x, y), f'U+{ord(ch):04X}' + (' *' if ch in GLYPHS else ''), fill='white', font=label)
        sheet.paste(text(new, ch, 6), (x + 13, y + 31))
    sheet.save(ROOT / 'punctuation_audit.png')
    rows = []
    for ch in string.punctuation:
        glyph = new.decode(ch)
        rows.append(dict(character=ch, codepoint=ord(ch), changed=ch in GLYPHS,
            rows=[''.join('#' if glyph.getpixel((x, y)) else '.' for x in range(6)) for y in range(11)]))
    save(ROOT / 'punctuation_audit.json', dict(glyphs=rows, unchanged_findings={
        ';': 'Tail ends at baseline row8; review a below-baseline tail next.',
        '"': 'Top ink row joins both quotation marks; consider separating the strokes.',
        '~': 'Flat top bar; check whether the legacy Japanese overline mapping is intentional before drawing a wave.',
        '. and !': 'Period is a vertical two-pixel dot; exclamation dot is horizontal two-pixel. Consider consistent dot weight.',
        '\\': 'Legacy Japanese yen-shaped glyph. Currency/encoding semantics must be checked before replacement.'},
        completed_brackets_parentheses_braces_dollar_and_underscore_preserved=True))


if __name__ == '__main__':
    ROOT.mkdir(parents=True, exist_ok=False)
    assert sha(PARENT.read_bytes()) == 'fed25c1b5c360d32164e6530ca8106d1abaf87167531c66ce2dda01328341a6f'
    source = NdsImage.open(PARENT).read_file('/__arm9__.bin')
    target, proof = propose(source)
    (ROOT / 'proposed_ARM9.bin').write_bytes(target)
    module = 'dk4tool/patch/ascii_punctuation_20261027.py'
    config = dict(format='dk4-ascii-punctuation-20261027-v1', status='experimental',
        predecessor_rom=str(PARENT), predecessor_rom_sha256=sha(PARENT.read_bytes()),
        source_ARM9_sha256=sha(source), target_ARM9_sha256=sha(target),
        proof=proof, dependencies={module: sha(Path(module).read_bytes())})
    assert not CONFIG.exists()
    save(CONFIG, config)
    registry = Path('translations/release_stack.json')
    original = registry.read_bytes()
    (ROOT / 'release_stack_before_registration.json').write_bytes(original)
    stack = json.loads(original)
    assert PROFILE not in stack['profiles']
    profile = copy.deepcopy(stack['profiles']['font-v2-draw-down-one-20261027'])
    profile['description'] = 'Experimental comma and question-mark bitmaps; complete prior font stack; Y+1 and line spacing unchanged.'
    profile['ascii_punctuation_20261027'] = str(CONFIG)
    stack['profiles'][PROFILE] = profile
    assert registry.read_bytes() == original
    save(registry, stack)
    (ROOT / 'release_stack_snapshot.json').write_bytes(registry.read_bytes())
    preview(source, target)
    print(json.dumps(dict(profile=PROFILE, proof=proof), indent=2))
