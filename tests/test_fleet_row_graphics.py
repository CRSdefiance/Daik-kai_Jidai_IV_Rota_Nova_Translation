"""Complete fleet lettering and exact surrounding art/inherited release guards."""

import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.fleet_row_graphics_v162 import (
    BATCH,
    LABELS,
    packed_proof,
    sources,
)
from scripts.probe_name_treasure_graphics_v161 import glyph_case, mask_for


@pytest.fixture(scope='module')
def case():
    base, prior, p = sources()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    source = prior.read_file('/__arm9__.bin')
    target, _ = apply_pxl_native_label_batch(BATCH, p.source, source)
    return base, source, batch, p, target


@pytest.mark.parametrize('index', range(5))
def test_complete_native_raster_and_negative_missing_first_character(case, index):
    _, source, batch, _, target = case
    row = batch['records'][index]
    scratch = dict(batch, color_index=15)
    glyph_case(source, scratch, row)
    mask, origin = mask_for(source, scratch, row)
    mask.paste(0, (origin[0], origin[1], origin[0] + 6, origin[1] + 11))
    with pytest.raises(ValueError, match='first letter'):
        glyph_case(source, scratch, row, expected_mask=mask)
    packed_proof(source, batch, row, target)
    p = PxlImage.from_bytes(target)
    for y in range(origin[1] - 2, origin[1] + 9):
        for x in range(origin[0], origin[0] + 6):
            p.indices[y * 256 + x] = 36
    with pytest.raises(ValueError, match='first character'):
        packed_proof(source, batch, row, p.to_bytes())


def test_exact_palette_header_borders_and_unowned_art(case):
    _, _, batch, a, target = case
    b = PxlImage.from_bytes(target)
    assert len(a.source) == len(target)
    assert a.source[:a.pixels_offset] == target[:b.pixels_offset]
    boxes = [row['box'] for row in batch['records']]
    assert all(a.indices[y * 256 + x] == b.indices[y * 256 + x]
               for y in range(192) for x in range(256)
               if not any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in boxes))
    assert [row['text'] for row in batch['records']] == [x[1] for x in LABELS]
    assert all(row['text'].startswith('Ship ') for row in batch['records'][1:])


def test_full_letters_fit_original_left_fleet_area(case):
    _, source, batch, _, _ = case
    for row in batch['records']:
        mask, _ = mask_for(source, batch, row)
        left, top, right, bottom = mask.getbbox()
        assert 3 <= left < right <= 52
        assert row['box'][1] <= top - 2 < bottom - 2 <= row['box'][3]


def test_wrong_source_cannot_be_repacked(case):
    _, source, _, p, _ = case
    changed = bytearray(p.source)
    changed[-1] ^= 1
    with pytest.raises(ValueError, match='source SHA-256'):
        apply_pxl_native_label_batch(BATCH, bytes(changed), source)


def test_exact_prior_stack_and_terminal_stages():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v161'], registry['profiles']['all-routes-unified-v162']
    assert b['batches'] == a['batches'] + [BATCH.as_posix()]
    assert len(b['batches']) == 441
    assert all(value == b[key] for key, value in a.items() if key not in ('batches', 'note', 'description'))
