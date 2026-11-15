"""Retain separate reproducible verification/replay producers for the five-glyph test."""

from pathlib import Path


if __name__ == '__main__':
    pairs = [
        ('verify_ascii_punctuation_native_20261027.py', 'verify_ascii_punctuation_all_native_20261027.py'),
        ('verify_ascii_punctuation_release_20261027.py', 'verify_ascii_punctuation_all_release_20261027.py'),
        ('verify_ascii_punctuation_dialogue_20261027.py', 'verify_ascii_punctuation_all_dialogue_20261027.py'),
        ('review_ascii_punctuation_captures_20261027.py', 'review_ascii_punctuation_all_captures_20261027.py'),
        ('run_ascii_punctuation_20261027.py', 'run_ascii_punctuation_all_20261027.py'),
        ('run_ascii_punctuation_hodram_20261027.py', 'run_ascii_punctuation_all_hodram_20261027.py'),
    ]
    for before, after in pairs:
        source = (Path('scripts') / before).read_text(encoding='utf-8')
        source = source.replace('ascii_punctuation_20261027', 'ascii_punctuation_all_20261027')
        source = source.replace('font_punctuation_20261027', 'font_punctuation_all_20261027')
        source = source.replace('font_v2_punctuation_one_pixel_20261027_test.nds',
                                'font_v2_all_punctuation_one_pixel_20261027_test.nds')
        if 'native' in before:
            source = source.replace("labels = ['g,', 'j?', 'p,', 'q?', 'y,', '[gyp?]']",
                                    'labels = ' + repr(['g;', 'j"', 'p.', 'q!', 'y~', '[gyp,?]']))
            sample = '"Wait; sail on."{LB}Aye! Ready? ~ 10 days ~{LB}Quickly, bring my spyglass!{LB}Can you judge this cargo, Rafael?'
            source = '\n'.join('    sample = ' + repr(sample) if line.startswith('    sample = ') else line for line in source.splitlines()) + '\n'
            source = source.replace('    pixels, events, kanji = raster(arm, raw)',
                '    pixels, events, kanji = raster(arm, raw)\n'
                '    _, prior_events, prior_kanji = raster(source, raw)\n'
                '    assert events == prior_events and kanji == prior_kanji\n'
                "    assert set(';\".!~') <= {chr(e['code']) for e in events if e['kind'] == 'ascii'}\n"
                "    save(ROOT / 'cursor_verification.json', dict(same_bytes=raw.hex(),\n"
                '        before_events=prior_events, after_events=events, all_glyph_positions_identical=True,\n'
                '        quotation_marks_and_every_following_character_keep_original_advance=True))')
        elif 'release' in before:
            source = source.replace('two glyphs', 'five approved glyphs').replace('two-glyph', 'five-glyph')
            source = source.replace('only_comma_and_question_bitmaps_changed', 'only_approved_five_bitmaps_changed')
        elif 'dialogue' in before:
            source = source.replace("[(4000, 'Aye!'), (6000, 'Aye, aye!')]",
                "[(3000, 'Warn them.'), (4000, 'Aye!'), (6000, 'Aye, aye!')]")
            source = source.replace("sum(sum(bool(p) for p in font.decode(c).getdata()) for c in 'Everything correct?' if c != ' ')",
                "sum(bool(font.decode(c).getpixel((x, y))) for c in 'Everything correct?' for y in range(11) for x in range(6))")
        output = Path('scripts') / after
        assert not output.exists()
        output.write_text(source, encoding='utf-8')
    print('Frozen separate native, cursor, release, dialogue and cold-boot producers.')
