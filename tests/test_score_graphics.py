"""Complete score labels in source four-bit format and preservation/crop guards."""

import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.probe_name_treasure_graphics_v161 import glyph_case, mask_for, sizing
from scripts.score_graphics_v164 import (
    BATCH,
    OWNER,
    RESOURCE,
    crop,
    real_format_glyphs,
    selector,
    sources,
)


@pytest.fixture(scope='module')
def case():
    base, prior, p = sources()
    source = prior.read_file('/__arm9__.bin')
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    target, _ = apply_pxl_native_label_batch(BATCH, p.source, source)
    return base, source, batch, p, target


@pytest.mark.parametrize('index', range(2))
def test_complete_native_glyphs_and_missing_first_character_rejection(case, index):
    _, source, batch, _, target = case
    row = batch['records'][index]
    glyph_case(source, batch, row)
    mask, origin = mask_for(source, batch, row)
    mask.paste(0, (origin[0], origin[1], origin[0] + 5, origin[1] + 11))
    with pytest.raises(ValueError, match='first letter'):
        glyph_case(source, batch, row, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for y in range(origin[1] - 2, origin[1] + 9):
        for x in range(origin[0], origin[0] + 5):
            p.indices[y * 208 + x] = 0
    with pytest.raises(ValueError, match='Packed score glyph'):
        real_format_glyphs(source, p.to_bytes(), batch)


def test_complete_native_raster_in_actual_four_bit_source_geometry(case):
    _, source, batch, _, target = case
    assert real_format_glyphs(source, target, batch)['dimensions'] == [208, 72]


def test_actual_selector_branch_with_explicit_type_virtual_input(case):
    _, source, _, _, _ = case
    assert selector(source)['source_owner'] == OWNER


def test_scoped_native_full_image_size(case):
    _, source, _, _, target = case
    assert sizing(source, target, 20, OWNER, supplied_table=True)['dimensions'] == [208, 72]


@pytest.mark.parametrize('index', range(2))
def test_native_crop_fields_under_original_glyph_cell_contract(case, index):
    _, source, batch, _, target = case
    row = batch['records'][index]
    assert crop(source, target, row)['native_crop_dimensions'] == [24, 24]
    wrong = dict(row, box=[row['box'][0] + 1, 0, row['box'][2], 24])
    with pytest.raises(ValueError, match='Native crop'):
        crop(source, target, wrong)


def test_exact_digits_perfect_art_palette_header_and_extents(case):
    _, source, batch, a, target = case
    b = PxlImage.from_bytes(target)
    assert len(target) == len(a.source)
    assert target[:b.pixels_offset] == a.source[:a.pixels_offset]
    assert all(a.indices[y * 208 + x] == b.indices[y * 208 + x]
               for y in range(72) for x in range(208) if x < 160 or y >= 24)
    for row in batch['records']:
        mask, _ = mask_for(source, batch, row)
        x0, y0, x1, y1 = row['box']
        bounds = mask.getbbox()
        assert x0 <= bounds[0] < bounds[2] <= x1
        assert y0 <= bounds[1] - 2 < bounds[3] - 2 <= y1
        assert {b.indices[y * 208 + x] for y in range(y0, y1) for x in range(x0, x1)} == {0, 15}


def test_exact_previous_profile_and_terminal_stages():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v163'], registry['profiles']['all-routes-unified-v164']
    assert b['batches'] == a['batches'] + [BATCH.as_posix()]
    assert len(b['batches']) == 450
    assert all(value == b[key] for key, value in a.items() if key not in ('batches', 'note', 'description'))


def test_modified_source_cannot_be_repacked(case):
    base, source, _, _, _ = case
    changed = bytearray(base.read_file(RESOURCE))
    changed[-1] ^= 1
    with pytest.raises(ValueError, match='source SHA-256'):
        apply_pxl_native_label_batch(BATCH, bytes(changed), source)
