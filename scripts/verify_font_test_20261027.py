"""Verify exact cumulative ancestry, font ownership, and original native glyph painting."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.codec import parse_markup, tokens_to_bytes
from dk4tool.dialogue.font_audit import ASCII_FONT_OFFSET, GameAsciiFont
from dk4tool.patch.experimental_ascii_font_v2 import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_name_catalog_glyphs_v278 import expected_pixels, raster

ROOT = Path('work/font_test_20261027')
ROM = Path('out/font_descenders_symbols_v2_20261027_test.nds')
CONFIG = Path('translations/experimental_ascii_font_20261027_v2.json')


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def native_checks():
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    parent = NdsImage.open(cfg['predecessor_rom']).read_file('/__arm9__.bin')
    arm, proof = apply_release(parent, CONFIG)
    cases = []
    # Prepend literal text so each printable symbol is exercised as text rather
    # than as a possible leading native presentation selector.
    for code in range(33, 127):
        raw = b'Test ' + bytes([code])
        pixels, events, kanji = raster(arm, raw)
        assert pixels == expected_pixels(arm, kanji, events), code
        assert [e['code'] for e in events if e['code'] != 32] == [ord(c) for c in 'Test'] + [code], code
        cases.append(dict(code=code, complete_independent_native_pixels=True))
    sample = ("I hear it's an enormous spear{LB}capable of driving evil away.{LB}"
              "Quickly, bring my spyglass!{LB}Can you judge this cargo, Rafael?")
    raws = [tokens_to_bytes(parse_markup(sample), guard_linebreaks=True, pair_phase_safe_breaks=True),
            b'[gyp] (Ready) {Yes} $100 _']
    sheet = Image.new('RGB', (864, 340), '#17252b')
    draw = ImageDraw.Draw(sheet)
    for row, raw in enumerate(raws):
        for column, data in enumerate([parent, arm]):
            pixels, events, kanji = raster(data, raw)
            assert pixels == expected_pixels(data, kanji, events)
            assert [e['code'] for e in events if e['code'] != 32] == [b for b in raw if b not in (32, 10)]
            if row == 0:
                assert sorted({e['y'] for e in events if e['code'] != 32}) == [0, 16, 32, 48]
            picture = Image.new('RGB', (216, 64))
            picture.putdata([(8, 16, 8) if p else (239, 232, 201) for p in pixels])
            sheet.paste(picture.resize((432, 128), Image.Resampling.NEAREST), (column * 432, row * 170 + 28))
            draw.text((column * 432 + 8, row * 170 + 8), 'V4749 ORIGINAL' if column == 0 else 'FONT TEST v2', fill='white')
    sheet.save(ROOT / 'native_font_before_after.png')
    # A bad predecessor must fail, rather than silently editing a new baseline.
    invalid = bytearray(parent)
    invalid[ASCII_FONT_OFFSET] ^= 4
    try:
        apply_release(bytes(invalid), CONFIG)
    except ValueError:
        pass
    else:
        raise AssertionError('Altered predecessor accepted')
    save(ROOT / 'native_font_verification.json', dict(font_proof=proof, printable_glyphs=cases,
        four_row_and_symbol_planes_match_independent_pixels=True,
        semantic_glyph_order_and_16_pixel_line_spacing_preserved=True,
        altered_predecessor_rejected=True,
        scope='Original native painter on controlled bitmap contexts; actual progressive scenes tested separately.'))
    print('94 printable ASCII glyphs and complete four-row/symbol native planes pass.', flush=True)


def release_checks():
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    parent_path = Path(config['predecessor_rom'])
    assert sha(parent_path.read_bytes()) == config['predecessor_rom_sha256']
    manifest = json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    prior = json.loads(parent_path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['profile'] == 'font-descenders-symbols-v2-20261027'
    snapshot = ROOT / 'release_stack_snapshot.json'
    assert manifest['release_stack_sha256'] == sha(snapshot.read_bytes())
    stack = json.loads(snapshot.read_text(encoding='utf-8'))
    live = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    for key in ['canonical_baseline', 'accepted_layers', 'latest_promoted_build']:
        assert live[key] == stack[key], key
    assert live['profiles'][manifest['profile']] == stack['profiles'][manifest['profile']]
    assert manifest['batches'] == prior['batches'] + [str(CONFIG)]
    assert manifest['required_batches'] == prior['required_batches']
    assert all(l['baked_into_baseline'] for l in stack['accepted_layers'])
    assert manifest['changed_paths'] == prior['changed_paths']
    parent, candidate = NdsImage.open(parent_path), NdsImage.open(ROM)
    def files(image):
        return {**{p: b for _, p, b in image.iter_files()}, **dict(image.iter_components())}
    before, after = files(parent), files(candidate)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    assert changed == ['/__arm9__.bin'], changed
    expected, proof = apply_release(before['/__arm9__.bin'], CONFIG)
    assert after['/__arm9__.bin'] == expected
    assert GameAsciiFont.from_arm9(expected).glyphs == Path(config['font_asset']).read_bytes()
    assert before['/GRP/KANJI.FNT'] == after['/GRP/KANJI.FNT']
    for text in [b'Continue', b'New Game', b'Options', b'Grand Race', b'Extras', b'Gallery']:
        assert text in expected, text
    command = [sys.executable, 'scripts/verify_release_baseline.py', stack['canonical_baseline']['path'], str(ROM)]
    for p in manifest['changed_paths']:
        command += ['--allow-path', p]
    with (ROOT / 'baseline_verification.log').open('w', encoding='utf-8') as log:
        subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT)
    save(ROOT / 'release_verification.json', dict(candidate=str(ROM), candidate_sha256=sha(ROM.read_bytes()),
        predecessor=str(parent_path), predecessor_sha256=config['predecessor_rom_sha256'],
        changed_from_predecessor=changed, font_proof=proof,
        all_nonfont_ARM9_bytes_and_all_other_files_identical=True,
        baseline=stack['canonical_baseline'], promoted_main_preserved=stack['latest_promoted_build'],
        all_accepted_layers_preserved=len(stack['accepted_layers']), total_batches=len(manifest['batches']),
        exact_frozen_registry_and_manifest_verified=True, baseline_verifier_passed=True,
        user_gameplay_acceptance_pending=True))
    print('Cumulative release preserved; only the 1045-byte font span is edited. SHA256', sha(ROM.read_bytes()), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--native-only', action='store_true')
    args = parser.parse_args()
    native_checks()
    if not args.native_only:
        release_checks()
