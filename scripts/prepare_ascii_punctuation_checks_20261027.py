"""Freeze predecessor replay/check producers for this two-glyph successor."""

from pathlib import Path

OLD = 'font_offset_one_20261027'
NEW = 'font_punctuation_20261027'
OLD_ROM = 'font_v2_draw_down_one_20261027_test.nds'
NEW_ROM = 'font_v2_punctuation_one_pixel_20261027_test.nds'


def clone(source, target):
    path = Path('scripts') / source
    output = Path('scripts') / target
    assert not output.exists()
    return output, path.read_text().replace(OLD, NEW).replace(OLD_ROM, NEW_ROM)


if __name__ == '__main__':
    path, source = clone('verify_font_offset_one_native_20261027.py', 'verify_ascii_punctuation_native_20261027.py')
    source = source.replace('import struct\n', 'import struct\nimport string\n')
    source = source.replace('from dk4tool.patch.ascii_draw_offset_one_20261027 import apply_release',
                            'from dk4tool.patch.ascii_punctuation_20261027 import apply_release')
    source = source.replace('translations/ascii_draw_offset_one_20261027_v1.json',
                            'translations/ascii_punctuation_20261027_v1.json')
    source = source.replace("for char in 'gjpqy[]_':", "for char in 'gjpqy' + string.punctuation:")
    source = source.replace("labels = ['g', 'j', 'p', 'q', 'y', '[gyp]']",
                            "labels = ['g,', 'j?', 'p,', 'q?', 'y,', '[gyp?]']")
    path.write_text(source, encoding='utf-8')
    for before, after in [
        ('run_font_offset_one_20261027.py', 'run_ascii_punctuation_20261027.py'),
        ('review_font_offset_one_captures_20261027.py', 'review_ascii_punctuation_captures_20261027.py'),
        ('verify_font_offset_one_dialogue_20261027.py', 'verify_ascii_punctuation_dialogue_20261027.py')]:
        path, source = clone(before, after)
        if before.startswith('verify_font_offset_one_dialogue'):
            source = source.replace('assert count == 213',
                "assert count == sum(sum(bool(p) for p in font.decode(c).getdata()) for c in 'Everything correct?' if c != ' ')")
            source = source.replace("    terminal = read(ROOT / 'newgame_terminal.json')", """    replies = []
    for frame, text in [(4000, 'Aye!'), (6000, 'Aye, aye!')]:
        reply_image = Image.open(frames[frame]['path']).convert('RGB')
        match = dark_text(font, text, reply_image, (10, 290, 245, 350))
        x, y, right, bottom = match['bounds']
        assert not [(px, py) for py in range(bottom, y + 15) for px in range(x, right)
                    if reply_image.getpixel((px, py)) == tuple(match['color'])]
        replies.append(dict(frame=frame, match=match, all_ink_and_blank_pixels_complete=True,
                            empty_rows_below_complete=True))
    terminal = read(ROOT / 'newgame_terminal.json')""")
            source = source.replace('confirmation_full_mask=bounds,', 'confirmation_full_mask=bounds, complete_live_replies=replies,')
        path.write_text(source, encoding='utf-8')
