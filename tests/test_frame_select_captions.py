"""Reject lost miniature letters, font changes and alterations to earlier art."""

import copy
import json
from pathlib import Path

import pytest

from dk4tool.graphics.compact_font import FONT_SHA256, GLYPHS, glyph, layout
from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.frame_select_captions_v169 import (
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
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    return base, prior, batch, target, embedded


@pytest.mark.parametrize('index', [15, 16, 17])
@pytest.mark.parametrize('which', [0, -1])
def test_complete_first_and_final_letter_loss_rejected(case, index, which):
    _, _, batch, target, _ = case
    report, mask = compact_pixels(target, batch)
    row = report['cases'][index - 15]
    x, y = row['all_letter_origins'][which]
    letter = row['text'][which]
    width = len(GLYPHS[letter][0])
    mask.paste(0, (x, y, x + width, y + 7))
    with pytest.raises(ValueError, match='first or final letter'):
        compact_pixels(target, batch, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for gy in range(y, y + 7):
        for gx in range(x, x + width):
            p.indices[gy * 256 + gx] = 0
    with pytest.raises(ValueError, match='Packed compact glyph'):
        compact_pixels(p.to_bytes(), batch)


def test_complete_custom_font_face_pinned_and_not_native_clipping():
    assert FONT_SHA256 == '1f34962fa7ff25491a84dc488219d6e18727654f51fdcfdefbb201b95a0e4b7d'
    for c in 'DoneRankCancel':
        g = glyph(c)
        assert g.height == 7
        assert len(GLYPHS[c]) == 7
        assert g.getbbox() is not None
    with pytest.raises(ValueError, match='Unsupported compact bitmap letter'):
        glyph('?')


def test_full_cells_gold_color_one_blank_row_and_spacing(case):
    _, _, batch, target, _ = case
    report, canvas = compact_pixels(target, batch)
    assert [r['full_cell_width'] for r in report['cases']] == [16, 16, 22]
    assert report['independent_packed_nibble_decode_exact']
    for row, proof in zip(batch['records'][15:], report['cases'], strict=True):
        left, top, right, bottom = row['box']
        mask, bounds, points = layout(row['text'], tuple(row['box']))
        assert bounds[1] >= top and bounds[3] <= bottom
        assert bounds[0] >= left and bounds[2] <= right
        assert points == [tuple(origin) for origin in proof['all_letter_origins']]
        assert not mask.crop((0, 7, right - left, 8)).getbbox()
        assert set(canvas.crop(tuple(row['box'])).tobytes()) == {0, 9}
        for c, (x, y) in zip(row['text'][:-1], points[:-1], strict=True):
            sep = x + len(GLYPHS[c][0])
            assert not canvas.crop((sep, y, sep + 1, y + 7)).getbbox()


@pytest.mark.parametrize('change', ['wrong_hash', 'unknown_face', 'missing_letter', 'short_cell', 'narrow_cell'])
def test_compact_face_and_complete_allocation_enforced(case, tmp_path, change):
    base, prior, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    row = wrong['records'][15]
    if change == 'wrong_hash':
        row['compact_font_sha256'] = '0' * 64
        error = 'compact font identity'
    elif change == 'unknown_face':
        row['font_face'] = 'squeezed'
        error = 'unsupported bitmap font face'
    elif change == 'missing_letter':
        row['text'] = 'Done?'
        error = 'Unsupported compact bitmap letter'
    else:
        row['box'] = [240, 40, 256, 46] if change == 'short_cell' else [240, 40, 255, 48]
        # Background size must follow the altered cell so fitting is reached.
        row.pop('background_indices_zlib_hex')
        error = 'Complete compact label does not fit'
    path = tmp_path / 'wrong.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match=error):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))


def test_fifteen_prior_records_and_both_atlas_copies_exact(case):
    _, prior, batch, target, embedded = case
    assert batch['records'][:15] == json.loads(OLD_BATCH.read_text(encoding='utf-8'))['records']
    assert preservation(target, embedded)['all_fifteen_prior_labels_and_unowned_pixels_exact']
    a, b = [PxlImage.from_bytes(raw) for raw in (prior.read_file(RESOURCE), target)]
    # The original input-field ornament and deferred cargo/ship captions stay exact.
    for y in range(32, 48):
        assert a.indices[y * 256 + 181:y * 256 + 240] == b.indices[y * 256 + 181:y * 256 + 240]


@pytest.mark.parametrize('index', [15, 16, 17])
def test_actual_generic_crop_constructor_respects_supplied_full_cells(case, index):
    _, prior, batch, _, _ = case
    row = batch['records'][index]
    proof = scoped_crop(prior.read_file('/__arm9__.bin'), row)
    assert proof['actual_generic_constructor_and_ABI_guards_pass']
    assert proof['native_crop_descriptor_dimensions'] == [row['box'][2] - row['box'][0], 8]


def test_all_profile_stages_and_explicit_expansion():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v168'], registry['profiles']['all-routes-unified-v169']
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    assert b['batches'] == [replacements.get(p, p) for p in a['batches']]
    assert len(b['batches']) == 452
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))


def test_original_completion_grade_and_cancel_meanings():
    context = source_context()
    assert [x['japanese'] for x in context['entries']] == ['終了', '等級', 'キャンセル']
    assert [x['english'] for x in context['entries']] == ['Done', 'Rank', 'Cancel']
    assert 'input-field ornament' in context['deferred']
