"""Expanded crew labels retain V165 and reject dropped leading characters."""

import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_ilnk_pxl_sync_batch, apply_pxl_native_label_batch
from scripts.frame_buttons_v165 import masks, real_format_glyphs
from scripts.frame_crew_buttons_v166 import (
    ARCHIVE,
    BATCH,
    OLD_BATCH,
    OLD_SYNC,
    RESOURCE,
    SYNC,
    preservation,
    sources,
    targets,
)


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    target, embedded = targets()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    return base, prior.read_file('/__arm9__.bin'), batch, target, embedded


@pytest.mark.parametrize('index', range(6, 10))
def test_four_new_words_reject_missing_first_character(case, index):
    _, source, batch, target, _ = case
    mask, origins = masks(source, batch)
    x, y = origins[index]
    mask.paste(0, (x, y, x + 5, y + 11))
    with pytest.raises(ValueError, match='first letter'):
        real_format_glyphs(source, target, batch, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for gy in range(y, y + 11):
        for gx in range(x, x + 5):
            p.indices[gy * 256 + gx] = 1
    with pytest.raises(ValueError, match='Packed button glyph'):
        real_format_glyphs(source, p.to_bytes(), batch)


def test_all_ten_actual_format_glyphs_and_set_crew_space(case):
    _, source, batch, target, _ = case
    assert real_format_glyphs(source, target, batch)['all_glyph_cells_ABI_header_and_guards_pass']
    assert len(batch['records']) == 10
    mask, origins = masks(source, batch)
    x, y = origins[6]
    assert batch['records'][6]['text'] == 'Set Crew'
    assert not mask.crop((x + 15, y, x + 20, y + 11)).getbbox()
    assert mask.crop((x, y, x + 15, y + 11)).getbbox()
    assert mask.crop((x + 20, y, x + 40, y + 11)).getbbox()


def test_prior_labels_chrome_and_embedded_storage_exact(case):
    _, _, _, target, embedded = case
    assert preservation(target, embedded)['all_six_prior_labels_and_unowned_pixels_exact']


def test_prior_letter_damage_is_rejected(case):
    _, _, _, target, embedded = case
    p = PxlImage.from_bytes(target)
    p.indices[125 * 256 + 8] ^= 1  # The earlier Equip lettering rectangle.
    with pytest.raises(ValueError, match='Prior labels'):
        preservation(p.to_bytes(), embedded)


def test_explicit_profile_supersession_preserves_all_other_batches_and_stages(case):
    _, _, batch, _, _ = case
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v165'], registry['profiles']['all-routes-unified-v166']
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    assert b['batches'] == [replacements.get(p, p) for p in a['batches']]
    assert len(b['batches']) == 452
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))
    old = json.loads(OLD_BATCH.read_text(encoding='utf-8'))
    assert batch['records'][:6] == old['records']


def test_canonical_source_and_reference_locks(case):
    base, source, _, target, _ = case
    raw = bytearray(base.read_file(RESOURCE))
    raw[-1] ^= 1
    with pytest.raises(ValueError, match='PXL source SHA-256'):
        apply_pxl_native_label_batch(BATCH, bytes(raw), source)
    archive = bytearray(base.read_file(ARCHIVE))
    archive[-1] ^= 1
    with pytest.raises(ValueError, match='ILNK source SHA-256'):
        apply_ilnk_pxl_sync_batch(SYNC, bytes(archive), target)


def test_new_white_pixels_fit_each_original_lettering_rectangle(case):
    _, source, batch, _, _ = case
    mask, _ = masks(source, batch)
    for row in batch['records'][6:]:
        x0, y0, x1, y1 = row['box']
        assert len(row['text']) * batch['advance'] <= x1 - x0
        cell = mask.crop((x0, y0, x1, y1))
        assert cell.getbbox()
        assert cell.getbbox()[3] <= y1 - y0
