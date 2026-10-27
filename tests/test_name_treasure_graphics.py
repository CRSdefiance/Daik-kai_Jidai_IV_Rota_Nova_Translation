"""Native complete lettering, atlas merging and neighboring artwork regression."""

import json
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    apply_ilnk_pxl_sync_batch,
    apply_ilnk_pxl_sync_batches,
    apply_pxl_native_label_batch,
    order_graphics_sync_groups,
)
from scripts.materialize_name_treasure_graphics_v161 import (
    ARCHIVE,
    BASE,
    BUTTON_SYNC,
    NAME,
    NAME_BATCH,
    PRIOR,
    SYNC_BATCH,
    TREASURE,
    TREASURE_BATCH,
)
from scripts.probe_name_treasure_graphics_v161 import glyph_case, mask_for, sizing


@pytest.fixture(scope='module')
def case():
    base, prior = NdsImage.open(BASE), NdsImage.open(PRIOR)
    source = prior.read_file('/__arm9__.bin')
    images = {path: apply_pxl_native_label_batch(batch, base.read_file(path), source)[0]
              for path, batch in ((NAME, NAME_BATCH), (TREASURE, TREASURE_BATCH))}
    return base, prior, source, images


@pytest.mark.parametrize('index', range(6))
def test_complete_native_label_cells_and_first_character(case, index):
    _, _, source, _ = case
    batch = json.loads((NAME_BATCH if index < 5 else TREASURE_BATCH).read_text(encoding='utf-8'))
    row = batch['records'][index if index < 5 else 0]
    glyph_case(source, batch, row)
    mask, origin = mask_for(source, batch, row)
    mask.paste(0, (origin[0], origin[1], origin[0] + batch['advance'], origin[1] + 11))
    with pytest.raises(ValueError, match='first letter'):
        glyph_case(source, batch, row, expected_mask=mask)


def test_native_full_name_atlas_and_eight_bit_treasure_sizes(case):
    _, _, source, images = case
    for selector in range(12, 20):
        sizing(source, images[NAME], selector, 0x023131DC)
    sizing(source, images[TREASURE], 20, 0x02313A10, supplied_table=True)


def test_merge_preserves_button_prompt_and_all_other_archive_blocks(case):
    base, prior, _, images = case
    refs = {'/_pxl/slackimg20.pxl': prior.read_file('/_pxl/slackimg20.pxl'), NAME: images[NAME]}
    actual, ids = apply_ilnk_pxl_sync_batches([BUTTON_SYNC, SYNC_BATCH], base.read_file(ARCHIVE), refs)
    old, new = IlnkContainer.parse(prior.read_file(ARCHIVE)), IlnkContainer.parse(actual)
    assert len(old.blocks) == len(new.blocks)
    assert all(a == b for i, (a, b) in enumerate(zip(old.blocks, new.blocks)) if i != 12)
    assert ids == ['DK4_PRESS_A_BUTTON_EMBEDDED_GRAPHIC_V1', 'DK4_NAME_ENTRY_EMBEDDED_GRAPHICS_V1']


def test_single_sync_backwards_compatibility(case):
    base, prior, _, _ = case
    source = base.read_file(ARCHIVE)
    image = prior.read_file('/_pxl/slackimg20.pxl')
    assert apply_ilnk_pxl_sync_batches([BUTTON_SYNC], source, {'/_pxl/slackimg20.pxl': image}) == (
        apply_ilnk_pxl_sync_batch(BUTTON_SYNC, source, image))


def test_overlap_cannot_overwrite_an_earlier_atlas_translation(case):
    base, prior, _, _ = case
    with pytest.raises(ValueError, match='overlapping'):
        apply_ilnk_pxl_sync_batches([BUTTON_SYNC, BUTTON_SYNC], base.read_file(ARCHIVE),
                                   {'/_pxl/slackimg20.pxl': prior.read_file('/_pxl/slackimg20.pxl')})


def test_archive_sync_runs_after_later_registered_pxl_inputs():
    grouped = {ARCHIVE: [BUTTON_SYNC, SYNC_BATCH], NAME: [NAME_BATCH], TREASURE: [TREASURE_BATCH]}
    assert [path for path, _ in order_graphics_sync_groups(grouped)] == [NAME, TREASURE, ARCHIVE]


def test_header_palette_plaque_chrome_and_treasure_rows_preserved(case):
    base, _, _, images = case
    for path, target in images.items():
        a, b = PxlImage.from_bytes(base.read_file(path)), PxlImage.from_bytes(target)
        assert len(a.source) == len(b.source)
        assert a.source[:a.pixels_offset] == b.source[:b.pixels_offset]
        if path == NAME:
            assert all(a.indices[y * 44 + x] == b.indices[y * 44 + x]
                       for y in range(60) for x in range(44)
                       if y % 12 in (0, 10, 11) or x < 4 or x >= 40)
        else:
            assert all(a.indices[y * 256 + x] == b.indices[y * 256 + x]
                       for y in range(192) for x in range(256)
                       if y >= 15 or x < 84 or x >= 174)


def test_all_previous_batches_and_stages_preserved():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v160'], registry['profiles']['all-routes-unified-v161']
    assert b['batches'] == a['batches'] + [NAME_BATCH.as_posix(), TREASURE_BATCH.as_posix(), SYNC_BATCH.as_posix()]
    assert len(b['batches']) == 440
    assert all(value == b[key] for key, value in a.items() if key not in ('batches', 'note', 'description'))


def test_font_trim_cannot_drop_visible_pixels(case, tmp_path):
    base, _, source, _ = case
    batch = json.loads(NAME_BATCH.read_text(encoding='utf-8'))
    batch['trim_blank_top_rows'] = 3  # Row two has actual capital-letter pixels.
    bad = tmp_path / 'bad_trim.json'
    bad.write_text(json.dumps(batch), encoding='utf-8')
    with pytest.raises(ValueError, match='drop visible glyph'):
        apply_pxl_native_label_batch(bad, base.read_file(NAME), source)
