"""Complete caption shapes/packing, full image bounds and prior release preservation."""

import json
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.fleet_row_graphics_v162 import packed_proof
from scripts.probe_name_treasure_graphics_v161 import glyph_case, mask_for
from scripts.village_graphics_v163 import BATCHES, PATHS, image_geometry, sources


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    source = prior.read_file('/__arm9__.bin')
    batches = {i: json.loads(p.read_text(encoding='utf-8')) for i, p in BATCHES.items()}
    targets = {i: apply_pxl_native_label_batch(BATCHES[i], base.read_file(path), source)[0]
               for i, path in PATHS.items()}
    return base, source, batches, targets


@pytest.mark.parametrize('index', list(PATHS))
def test_native_full_caption_and_missing_first_character_rejection(case, index):
    _, source, batches, targets = case
    batch, target = batches[index], targets[index]
    row = batch['records'][0]
    scratch = dict(batch, color_index=15)
    glyph_case(source, scratch, row)
    packed_proof(source, batch, row, target)
    mask, origin = mask_for(source, scratch, row)
    assert mask.getbbox()[0] >= 0 and mask.getbbox()[2] <= 256
    mask.paste(0, (origin[0], origin[1], origin[0] + 6, origin[1] + 11))
    with pytest.raises(ValueError, match='first letter'):
        glyph_case(source, scratch, row, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for y in range(origin[1] - 2, origin[1] + 9):
        for x in range(origin[0], origin[0] + 6):
            p.indices[y * 256 + x] = 255
    with pytest.raises(ValueError, match='first character'):
        packed_proof(source, batch, row, p.to_bytes())


@pytest.mark.parametrize('index', list(PATHS))
def test_native_full_image_size_under_explicit_loaded_resource_contract(case, index):
    _, source, _, targets = case
    assert image_geometry(source, targets[index])['dimensions'] == [256, 192]


def test_original_headers_palettes_extents_and_complete_white_canvas(case):
    base, _, batches, targets = case
    for i, raw in targets.items():
        a, b = PxlImage.from_bytes(base.read_file(PATHS[i])), PxlImage.from_bytes(raw)
        assert len(raw) == len(a.source)
        assert raw[:b.pixels_offset] == a.source[:a.pixels_offset]
        assert (b.width, b.height, b.bits_per_pixel) == (256, 192, 8)
        assert set(b.indices) == {255, batches[i]['color_index']}
        assert a.palette[batches[i]['color_index']] == b.palette[batches[i]['color_index']]


def test_exact_inherited_profile_and_terminal_stages():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v162'], registry['profiles']['all-routes-unified-v163']
    assert b['batches'] == a['batches'] + [p.as_posix() for p in BATCHES.values()]
    assert len(b['batches']) == 449
    assert all(value == b[key] for key, value in a.items() if key not in ('batches', 'note', 'description'))


def test_wrong_source_is_rejected(case):
    base, source, _, _ = case
    changed = bytearray(base.read_file(PATHS[168]))
    changed[-1] ^= 1
    with pytest.raises(ValueError, match='source SHA-256'):
        apply_pxl_native_label_batch(BATCHES[168], bytes(changed), source)
