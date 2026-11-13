"""Complete two-word phrases, exact input chrome and inherited graphics."""

import copy
import json
from pathlib import Path

import pytest

from dk4tool.graphics.compact_font import GLYPHS
from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.frame_cargo_captions_v170 import (
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


@pytest.mark.parametrize('index', [18, 19])
@pytest.mark.parametrize('which', [0, 5, -1])
def test_first_letters_of_both_words_and_final_letter_loss_rejected(case, index, which):
    _, _, batch, target, _ = case
    report, mask = compact_pixels(target, batch)
    row = report['cases'][index - 15]
    x, y = row['all_letter_origins'][which]
    width = len(GLYPHS[row['text'][which]][0])
    mask.paste(0, (x, y, x + width, y + 7))
    with pytest.raises(ValueError, match='first or final letter'):
        compact_pixels(target, batch, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for gy in range(y, y + 7):
        for gx in range(x, x + width):
            p.indices[gy * 256 + gx] = 0
    with pytest.raises(ValueError, match='Packed compact glyph'):
        compact_pixels(p.to_bytes(), batch)


def test_three_blank_word_columns_and_clear_neighbor_boundary(case):
    _, _, batch, target, _ = case
    report, canvas = compact_pixels(target, batch)
    assert [r['full_cell_width'] for r in report['cases'][-2:]] == [37, 31]
    for row in report['cases'][-2:]:
        x, y = row['all_letter_origins'][4]
        # The explicit blank space and two inter-cell columns remain clear.
        assert not canvas.crop((x - 1, y, x + 2, y + 7)).getbbox()
    p = PxlImage.from_bytes(target)
    assert all(p.indices[y * 256 + 239] == 0 for y in range(40, 48))
    assert all(p.indices[y * 256 + x] == 0 for y in (39, 47)
               for x in range(208, 240 if y == 47 else 256))


def test_input_field_and_eighteen_prior_labels_exact(case):
    _, prior, batch, target, embedded = case
    assert batch['records'][:18] == json.loads(OLD_BATCH.read_text(encoding='utf-8'))['records']
    assert preservation(target, embedded)['all_eighteen_prior_labels_and_unowned_pixels_exact']
    a, b = [PxlImage.from_bytes(raw) for raw in (prior.read_file(RESOURCE), target)]
    for y in range(30, 48):
        assert a.indices[y * 256 + 181:y * 256 + 208] == b.indices[y * 256 + 181:y * 256 + 208]


@pytest.mark.parametrize('space', [0, 4])
def test_invalid_blank_word_width_rejected(case, tmp_path, space):
    base, prior, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    wrong['records'][18]['compact_word_space_width'] = space
    path = tmp_path / 'invalid-space.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='invalid compact word space'):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))


def test_overwide_trial_word_gap_cannot_pass_reviewed_packed_shape(case, tmp_path):
    base, prior, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    for row in wrong['records'][-2:]:
        row.pop('compact_word_space_width')
    path = tmp_path / 'trial-space.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    target, _ = apply_pxl_native_label_batch(path, base.read_file(RESOURCE), prior.read_file('/__arm9__.bin'))
    assert any(PxlImage.from_bytes(target).indices[y * 256 + 239] for y in range(40, 47))
    with pytest.raises(ValueError, match='Packed compact glyph'):
        compact_pixels(target, batch)


@pytest.mark.parametrize('index', [18, 19])
def test_supplied_native_crop_keeps_full_caption_cell(case, index):
    _, prior, batch, _, _ = case
    proof = scoped_crop(prior.read_file('/__arm9__.bin'), batch['records'][index])
    assert proof['actual_generic_constructor_and_ABI_guards_pass']
    assert proof['native_crop_descriptor_dimensions'] == [48 if index == 18 else 32, 8]


def test_full_profile_and_stages_inherited():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v169'], registry['profiles']['all-routes-unified-v170']
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    assert b['batches'] == [replacements.get(p, p) for p in a['batches']]
    assert len(b['batches']) == 452
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))


def test_exact_source_readings_and_palette_boundary():
    proof = source_context()
    assert [(r['japanese'], r['english']) for r in proof['entries']] == [('積み荷選択', 'Pick Cargo'), ('船選択', 'Pick Ship')]
    assert [r['original_cell_palette_indices'] for r in proof['entries']] == [[0, 6, 9], [0, 4, 5, 6, 9]]
    assert 'x<=207' in proof['border_boundary']
