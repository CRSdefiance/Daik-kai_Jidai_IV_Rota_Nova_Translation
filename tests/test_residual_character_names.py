import json
from pathlib import Path

import pytest

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.residual_character_name_release import NAMES, apply_release, transform
from dk4tool.rom.nds import NdsImage


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v149_candidate.nds').read_file('/__arm9__.bin')


def test_source_owner_boundaries_and_preservation(source):
    saved, report = apply_release(source, 'translations/residual_character_names_release_v1.json')
    assert saved == Path('work/analysis/residual_character_names_arm9.bin').read_bytes()
    restored = bytearray(saved)
    for _, at, _, _ in NAMES:
        restored[at:at + 12] = source[at:at + 12]
    assert restored == source
    assert report['runtime_verified'] is False


def test_changed_source_rejected(source):
    with pytest.raises(ValueError, match='exact complete V149'):
        transform(bytes([source[0] ^ 1]) + source[1:])


@pytest.mark.parametrize('change', ['missing_row', 'pixel_mismatch', 'dropped_leading_glyph_review'])
def test_incomplete_native_format_evidence_rejected(source, tmp_path, change):
    config = json.loads(Path('translations/residual_character_names_release_v1.json').read_text(encoding='utf-8'))
    native = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    if change == 'missing_row':
        native['paired']['cases'].pop()
    elif change == 'pixel_mismatch':
        native['paired']['rasters'][0]['independent_pixels_match'] = False
    else:
        native['native_ink_visual_review']['complete_leading_and_final_glyphs'] = False
    review = tmp_path / 'review.json'
    review.write_text(json.dumps(native), encoding='utf-8')
    old = config['native_review']
    config['native_review'] = str(review)
    config['dependencies'].pop(old)
    config['dependencies'][str(review)] = sha(review.read_bytes())
    path = tmp_path / 'release.json'
    path.write_text(json.dumps(config), encoding='utf-8')
    with pytest.raises(ValueError, match='native layout evidence'):
        apply_release(source, path)
