"""Actual clipped/rehashed caption mutations and source-mask restoration limits."""

import copy
import json
import struct
import zlib

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import (
    FRAME_BYTES,
    apply_raw_bgr555_art,
    render_region_payload,
    sha,
)
from dk4tool.graphics.raw_caption_restore import restore_caption
from scripts.comic_captions_v181 import (
    BATCH,
    OLD,
    OUT,
    PATH,
    authored,
    preservation,
    sources,
)
from scripts.maria_gallery_v180 import region_bytes


def write(path, batch):
    path.write_text(json.dumps(batch), encoding='utf-8')
    return path


@pytest.fixture(scope='module')
def case():
    _, prior, source, block = sources()
    draft = OUT / 'reviewed-format-draft.json'
    batch = json.loads(draft.read_text(encoding='utf-8'))
    target, _ = apply_raw_bgr555_art(draft, source)
    merged = IlnkContainer.parse(prior.read_file(PATH))
    merged.blocks[19] = IlnkContainer.parse(target).blocks[19]
    return source, block, batch, merged.to_bytes()


def test_source_scenery_outside_old_ink_and_new_glyphs_is_word_exact(case):
    _, block, batch, target = case
    assert preservation(target)['unowned_bytes_exact']
    assert batch['records'][:4] == json.loads(OLD.read_text(encoding='utf-8'))['records']
    new_block = IlnkContainer.parse(target).blocks[19]
    for row in batch['records'][4:]:
        frame = block[row['image_index'] * FRAME_BYTES:(row['image_index'] + 1) * FRAME_BYTES]
        source_region = region_bytes(frame, row['box'])
        restored, proof = restore_caption(row, source_region, block, FRAME_BYTES)
        actual = region_bytes(new_block[row['image_index'] * FRAME_BYTES:(row['image_index'] + 1) * FRAME_BYTES], row['box'])
        _, raster = render_region_payload(row, source_region, batch, block)
        width = row['box'][2] - row['box'][0]
        x0, y0, x1, y1 = raster['full_ink_box']
        allowed = set(proof['source_glyph_mask_indices'])
        allowed.update(y * width + x for y in range(y0, y1) for x in range(x0, x1))
        before = [v for v, in struct.iter_unpack('<H', source_region)]
        after = [v for v, in struct.iter_unpack('<H', actual)]
        assert all(a == b for i, (a, b) in enumerate(zip(before, after, strict=True)) if i not in allowed)
        assert len(restored) == len(before)
        assert all(not (a ^ b) & 0x8000 for a, b in zip(before, after, strict=True))
        assert proof['estimated_scenery_is_recovered_original'] is False


@pytest.mark.parametrize('index', [0, 1, 2])
def test_full_phrases_are_below_or_above_photos_not_on_borders(case, index):
    _, _, batch, _ = case
    _, proofs = authored()
    row, proof = batch['records'][index + 4], proofs[index]
    assert ''.join(g['character'] for g in proof['visible_characters']) == row['english'].replace(' ', '')
    py0, py1 = proof['restoration']['photo_box'][1::2]
    for glyph in proof['visible_characters']:
        y0, y1 = row['box'][1] + glyph['bbox'][1], row['box'][1] + glyph['bbox'][3]
        assert y1 <= py0 or y0 >= py1


@pytest.mark.parametrize('index', [0, 1, 2])
@pytest.mark.parametrize('end', [0, -1])
def test_missing_caption_credit_first_or_last_letter_with_new_checksum_fails(case, tmp_path, index, end):
    source, block, batch, _ = case
    bad = copy.deepcopy(batch)
    row = bad['records'][index + 4]
    _, proofs = authored()
    x0, y0, x1, y1 = proofs[index]['visible_characters'][end]['bbox']
    width = row['box'][2] - row['box'][0]
    frame = block[row['image_index'] * FRAME_BYTES:(row['image_index'] + 1) * FRAME_BYTES]
    restored, _ = restore_caption(row, region_bytes(frame, row['box']), block, FRAME_BYTES)
    payload = bytearray(zlib.decompress(bytes.fromhex(row['words_zlib_hex'])))
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = y * width + x
            struct.pack_into('<H', payload, i * 2, restored[i])
    row['words_zlib_hex'] = zlib.compress(payload).hex()
    row['words_sha256'] = sha(payload)
    with pytest.raises(ValueError, match='complete English glyph raster'):
        apply_raw_bgr555_art(write(tmp_path / 'missing.json', bad), source)


def test_old_two_pixel_antialias_fringe_is_restored_without_white_ghosts(case):
    _, block, batch, _ = case
    for row in batch['records'][4:]:
        f = row['image_index']
        restored, proof = restore_caption(row, region_bytes(block[f * FRAME_BYTES:(f + 1) * FRAME_BYTES], row['box']), block, FRAME_BYTES)
        assert proof['source_antialias_fringe_radius'] == 2
        assert len(proof['estimated_scenery_indices']) > 0
        # Source dim photo colors are below the caption's bright-white ink.
        assert all(min((restored[i] >> (c * 5)) & 31 for c in range(3)) < 16
                   for i in proof['estimated_scenery_indices'])


@pytest.mark.parametrize('change,message', [
    ('outside', 'text box escapes'), ('photo', 'overlap original photo'),
    ('background', 'reviewed gray-canvas'),
])
def test_layout_restoration_controls_reject_bad_declared_geometry(case, tmp_path, change, message):
    source, _, batch, _ = case
    bad = copy.deepcopy(batch)
    row = bad['records'][6]
    if change == 'outside': row['text_box'][2] = 118
    elif change == 'photo': row['text_box'] = [0, 0, 117, 10]
    elif change == 'background': row['background'] = 0
    with pytest.raises(ValueError, match=message):
        apply_raw_bgr555_art(write(tmp_path / 'bad.json', bad), source)


def test_original_full_block_required_for_restoration(case):
    _, block, batch, _ = case
    row = batch['records'][4]
    region = region_bytes(block[4 * FRAME_BYTES:5 * FRAME_BYTES], row['box'])
    with pytest.raises(ValueError, match='exact original block'):
        render_region_payload(row, region, batch, block[:-2])


def test_border_growth_is_bounded_by_original_ink_not_previous_added_pixels(case):
    _, block, batch, _ = case
    for row in batch['records'][4:]:
        f = row['image_index']
        _, proof = restore_caption(row, region_bytes(block[f * FRAME_BYTES:(f + 1) * FRAME_BYTES], row['box']), block, FRAME_BYTES)
        seed = set(proof['initial_glyph_fringe_mask_indices'])
        width = row['box'][2] - row['box'][0]
        for i in set(proof['source_glyph_mask_indices']) - seed:
            x, y = i % width, i // width
            assert any((y + dy) * width + x + dx in seed
                       for dx in range(-2, 3) for dy in range(-2, 3)
                       if 0 <= x + dx < width and 0 <= y + dy < row['box'][3] - row['box'][1])
        assert proof['source_border_reference_words'] == {'top': 1057, 'bottom': 1057, 'left': 7399, 'right': 7399}


def test_rehashed_hidden_scenery_mutation_is_rejected(case, tmp_path):
    source, _, batch, _ = case
    bad = copy.deepcopy(batch)
    row = bad['records'][4]
    payload = bytearray(zlib.decompress(bytes.fromhex(row['words_zlib_hex'])))
    payload[-12] ^= 1
    row['words_zlib_hex'] = zlib.compress(payload).hex()
    row['words_sha256'] = sha(payload)
    with pytest.raises(ValueError, match='complete English glyph raster'):
        apply_raw_bgr555_art(write(tmp_path / 'scenery.json', bad), source)


def test_complete_profile_preserves_every_stage_and_one_batch_replacement():
    from scripts.build_integrated_release import load_release_stack
    profiles = load_release_stack()['profiles']
    a, b = [profiles[p] for p in ('all-routes-unified-v180', 'all-routes-unified-v181')]
    assert b['batches'] == [BATCH.as_posix() if p == OLD.as_posix() else p for p in a['batches']]
    assert len(b['batches']) == 463
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))


def test_other_raw_frames_and_prior_creator_marks_cannot_change(case):
    _, _, _, target = case
    archive = IlnkContainer.parse(target)
    block = bytearray(archive.blocks[19])
    block[13 * FRAME_BYTES + (220 * 320 + 282) * 2] ^= 1
    archive.blocks[19] = bytes(block)
    with pytest.raises(ValueError, match='Unowned scenery/other raw frames'):
        preservation(archive.to_bytes())
