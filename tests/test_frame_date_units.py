"""Date-unit initials fit original ink cells; earlier compact face is unchanged."""

import copy
import json
from pathlib import Path

import pytest

from dk4tool.graphics.compact_font import (
    DATE_FONT_FACE,
    DATE_FONT_SHA256,
    DATE_GLYPHS,
    FONT_SHA256,
    GLYPHS,
    glyph,
)
from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.frame_date_units_v171 import (
    BATCH,
    OLD_BATCH,
    OLD_SYNC,
    RESOURCE,
    SYNC,
    compact_pixels,
    preservation,
    scoped_crop,
    source_context,
    sources,
    targets,
)


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    target, embedded = targets()
    return base, prior, json.loads(BATCH.read_text(encoding='utf-8')), target, embedded


@pytest.mark.parametrize('index', [20, 21])
def test_complete_unit_glyph_loss_rejected(case, index):
    _, _, batch, target, _ = case
    proof, mask = compact_pixels(target, batch)
    unit = proof['cases'][index - 15]
    x, y = unit['all_letter_origins'][0]
    width = len(DATE_GLYPHS[unit['text']][0])
    mask.paste(0, (x, y, x + width, y + 7))
    with pytest.raises(ValueError, match='first or final letter'):
        compact_pixels(target, batch, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for gy in range(y, y + 7):
        for gx in range(x, x + width):
            p.indices[gy * 256 + gx] = 0
    with pytest.raises(ValueError, match='Packed compact glyph'):
        compact_pixels(p.to_bytes(), batch)


def test_versioned_face_keeps_every_prior_shape_and_identity():
    assert FONT_SHA256 == '1f34962fa7ff25491a84dc488219d6e18727654f51fdcfdefbb201b95a0e4b7d'
    assert DATE_FONT_SHA256 == 'cfe704c25f3ce6e8e8464201d8b3791a981941c47782bb1bbc5dbc0cf054d16f'
    assert {c: DATE_GLYPHS[c] for c in GLYPHS} == GLYPHS
    with pytest.raises(ValueError, match='Unsupported compact bitmap letter'):
        glyph('M')
    assert glyph('M', font_face=DATE_FONT_FACE).size == (5, 7)
    assert glyph('D', font_face=DATE_FONT_FACE).tobytes() == glyph('D').tobytes()


def test_twenty_prior_labels_and_separator_ornaments_exact(case):
    _, prior, batch, target, embedded = case
    assert batch['records'][:20] == json.loads(OLD_BATCH.read_text(encoding='utf-8'))['records']
    assert preservation(target, embedded)['all_twenty_prior_labels_and_unowned_pixels_exact']
    a, b = [PxlImage.from_bytes(raw) for raw in (prior.read_file(RESOURCE), target)]
    for y in range(112, 128):
        assert a.indices[y * 256 + 134:y * 256 + 146] == b.indices[y * 256 + 134:y * 256 + 146]
        assert a.indices[y * 256 + 98:y * 256 + 104] == b.indices[y * 256 + 98:y * 256 + 104]


@pytest.mark.parametrize('index', [20, 21])
def test_complete_unit_cells_and_supplied_native_crops(case, index):
    _, prior, batch, target, _ = case
    row = batch['records'][index]
    proof = scoped_crop(prior.read_file('/__arm9__.bin'), row)
    assert proof['native_crop_descriptor_dimensions'] == [6 if index == 20 else 5, 8]
    assert proof['actual_generic_constructor_and_ABI_guards_pass']
    report, mask = compact_pixels(target, batch)
    assert report['cases'][index - 15]['full_cell_width'] == (5 if index == 20 else 4)
    assert not mask.crop((row['box'][0], 123, row['box'][2], 124)).getbbox()


@pytest.mark.parametrize('hash_value', [FONT_SHA256, '0' * 64])
def test_date_face_requires_its_exact_identity(case, tmp_path, hash_value):
    base, prior, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    wrong['records'][20]['compact_font_sha256'] = hash_value
    path = tmp_path / 'wrong-face-hash.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='compact font identity'):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))


def test_wrong_unit_letter_cannot_pass_reviewed_shape(case, tmp_path):
    base, prior, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    wrong['records'][20]['text'] = 'D'
    path = tmp_path / 'wrong-unit.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    target, _ = apply_pxl_native_label_batch(path, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    with pytest.raises(ValueError, match='Packed compact glyph'):
        compact_pixels(target, batch)


def test_full_profile_and_terminal_stages_inherited():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v170'], registry['profiles']['all-routes-unified-v171']
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    assert b['batches'] == [replacements.get(p, p) for p in a['batches']]
    assert len(b['batches']) == 452
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))


def test_original_month_day_meaning_and_exact_ink_cells():
    proof = source_context()
    assert [(r['japanese'], r['english']) for r in proof['entries']] == [('月', 'M'), ('日', 'D')]
    assert [r['box'] for r in proof['entries']] == [[104, 116, 110, 124], [128, 116, 133, 124]]
    assert 'month and day' in proof['localization']
