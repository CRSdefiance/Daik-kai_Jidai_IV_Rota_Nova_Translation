"""Native ink spacing, truthful font proof and complete prior inheritance."""

import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.frame_preset_buttons_v167 import (
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
from scripts.probe_button_prompt_native import HEADER, STACK, call, machine


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    target, embedded = targets()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    return base, prior.read_file('/__arm9__.bin'), batch, target, embedded


@pytest.mark.parametrize('index', [10, 11])
def test_preset_words_reject_missing_leading_letters(case, index):
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
    with pytest.raises(ValueError, match='Packed preset glyph'):
        real_format_glyphs(source, p.to_bytes(), batch)


def test_complete_native_ink_and_word_space(case):
    _, source, batch, target, _ = case
    proof = real_format_glyphs(source, target, batch)
    assert proof['label_widths'][-2:] == [40, 41]
    assert len(proof['isolated_proportional_glyphs']) == 11
    assert ''.join(x['character'] for x in proof['isolated_proportional_glyphs']) == 'Fill Evenly'
    mask, points, _ = layout_masks(source, batch)
    x, y = points[11][4]
    assert not mask.crop((x, y, x + 3, y + 11)).getbbox()


def test_final_letter_is_retained(case):
    _, source, batch, target, _ = case
    _, points, _ = layout_masks(source, batch)
    x, y = points[11][-1]
    p = PxlImage.from_bytes(target)
    for gy in range(y, y + 11):
        for gx in range(x, x + 5):
            p.indices[gy * 256 + gx] = 1
    with pytest.raises(ValueError, match='Packed preset glyph'):
        real_format_glyphs(source, p.to_bytes(), batch)


def test_original_native_cell_clearing_is_not_claimed_as_proportional_draw(case):
    _, source, batch, target, _ = case
    expected, points, _ = layout_masks(source, batch)
    p = PxlImage.from_bytes(target)
    p.indices[:] = bytes(len(p.indices))
    uc = machine(source)
    uc.mem_write(HEADER, p.to_bytes())
    for char, (x, y) in zip(batch['records'][11]['text'], points[11], strict=True):
        uc.mem_write(STACK, struct.pack('<2I', ord(char), 15))
        call(uc, 0xD16B4, (0, HEADER, x, y))
    actual = PxlImage.from_bytes(bytes(uc.mem_read(HEADER, len(p.source))))
    x0, y0, x1, y1 = batch['records'][11]['box']
    missing = [(x, y) for y in range(y0, y1) for x in range(x0, x1)
               if expected.getpixel((x, y)) and actual.indices[y * 256 + x] == 0]
    assert len(missing) == 23
    # Final baked pixels retain all of this ink; the scoped proof executes
    # each complete native cell in isolation before composing its ink offline.
    packed = PxlImage.from_bytes(target)
    assert all(packed.indices[y * 256 + x] == 15 for x, y in missing)


def test_prior_ten_labels_and_artwork_exact(case):
    _, _, batch, target, embedded = case
    assert preservation(target, embedded)['all_ten_prior_labels_and_unowned_pixels_exact']
    old = json.loads(OLD_BATCH.read_text(encoding='utf-8'))
    assert batch['records'][:10] == old['records']


def test_spacing_policy_rejects_unknown_mode_and_overflow(case, tmp_path):
    base, source, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    path = tmp_path / 'wrong-spacing.json'
    wrong['records'][11]['glyph_spacing'] = 'squeeze'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='invalid native glyph spacing'):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), source)
    wrong['records'][11]['glyph_spacing'] = 'fixed'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='label does not fit'):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), source)


def test_spacing_does_not_allow_cropped_source_glyphs(case, tmp_path):
    base, source, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    wrong['glyph_width'] = 3
    path = tmp_path / 'cropped.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='cropped glyph'):
        apply_pxl_native_label_batch(path, base.read_file(RESOURCE), source)


def test_complete_profile_stages_and_explicit_supersession():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v166'], registry['profiles']['all-routes-unified-v167']
    replacements = {OLD_BATCH.as_posix(): BATCH.as_posix(), OLD_SYNC.as_posix(): SYNC.as_posix()}
    assert b['batches'] == [replacements.get(p, p) for p in a['batches']]
    assert len(b['batches']) == 452
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))


def test_original_help_resolves_flagship_and_even_refill():
    proof = source_context()
    assert '［旗艦重視］旗艦へ優先的に配置。' in proof['entries'][0]['japanese']
    assert '水・食料を均等に最大量まで補給' in proof['entries'][1]['japanese']
