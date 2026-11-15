"""Complete heading ink, original palette colors and inherited release stack."""

import copy
import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.frame_upper_headings_v168 import (
    BATCH,
    OLD_BATCH,
    OLD_SYNC,
    RESOURCE,
    SYNC,
    layout_masks,
    preservation,
    real_format_glyphs,
    source_context,
    sources,
    targets,
)


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    target, embedded = targets()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    return base, prior.read_file('/__arm9__.bin'), batch, target, embedded


@pytest.mark.parametrize('index', [12, 13, 14])
def test_headings_reject_missing_first_letters(case, index):
    _, source, batch, target, _ = case
    mask, points, _ = layout_masks(source, batch)
    x, y = points[index][0]
    mask.paste(0, (x, y, x + 5, y + 11))
    with pytest.raises(ValueError, match='first letter'):
        real_format_glyphs(source, target, batch, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for gy in range(y, y + 11):
        for gx in range(x, x + 5):
            p.indices[gy * 256 + gx] = 1
    with pytest.raises(ValueError, match='Packed heading glyph'):
        real_format_glyphs(source, p.to_bytes(), batch)


def test_native_gold_white_complete_words_and_separator(case):
    _, source, batch, target, _ = case
    proof = real_format_glyphs(source, target, batch)
    mask, positions, widths = layout_masks(source, batch)
    assert widths[-3:-1] == [20, 35]
    assert widths[-1] <= 33
    assert [r['color_index'] for r in batch['records'][-3:]] == [9, 9, 15]
    assert ''.join(p['character'] for p in proof['isolated_proportional_glyphs']) == 'Fill EvenlyArrival'
    for row in batch['records'][-3:]:
        ink = set(mask.crop(tuple(row['box'])).tobytes())
        assert ink == {0, row['color_index']}
    x, y = positions[13][5]
    assert not mask.crop((x, y, x + 5, y + 11)).getbbox()


def test_original_month_grid_and_twelve_prior_labels_exact(case):
    base, _, batch, target, embedded = case
    assert preservation(target, embedded)['all_twelve_prior_labels_and_unowned_pixels_exact']
    old = json.loads(OLD_BATCH.read_text(encoding='utf-8'))
    assert batch['records'][:12] == old['records']
    a, b = [PxlImage.from_bytes(raw) for raw in (base.read_file(RESOURCE), target)]
    for y in range(32, 70):
        assert a.indices[y * 256 + 105:y * 256 + 181] == b.indices[y * 256 + 105:y * 256 + 181]


@pytest.mark.parametrize('field', ['color_index', 'erase_palette_indices'])
def test_record_palette_override_rejects_out_of_range(case, tmp_path, field):
    base, source, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    wrong['records'][12][field] = 16 if field == 'color_index' else [16]
    path = tmp_path / 'wrong-color.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='palette index is out of range'):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), source)


def test_nine_visible_rows_cannot_be_clipped_to_eight(case, tmp_path):
    base, source, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    wrong['records'][12]['box'] = [195, 1, 222, 9]
    path = tmp_path / 'too-short.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='label does not fit'):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), source)


def test_complete_profile_and_stages_inherited():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v167'], registry['profiles']['all-routes-unified-v168']
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    assert b['batches'] == [replacements.get(p, p) for p in a['batches']]
    assert len(b['batches']) == 452
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))


def test_source_context_retains_stock_arrival_month():
    context = source_context()
    assert [r['japanese'] for r in context['entries']] == ['種類', '相場%', '入荷月']
    assert context['entries'][2]['english'] == 'Arrival'
    assert '1-12 month grid' in context['month_context']
