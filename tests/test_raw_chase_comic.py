"""Whole chase phrases, source outlines, actual missing-letter and scenery mutations."""

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
from dk4tool.graphics.raw_chase_restore import restore_chase_call
from scripts.chase_comic_v182 import BATCH, OLD, OUT, PATH, authored, preservation, sources
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
    _, proofs = authored()
    return source, block, batch, merged.to_bytes(), proofs


def test_full_previous_art_atlas_and_bubble_corner_source_exact(case):
    _, block, batch, target, _ = case
    assert preservation(target)['unowned_bytes_exact']
    assert batch['records'][:7] == json.loads(OLD.read_text(encoding='utf-8'))['records']
    new = IlnkContainer.parse(target).blocks[19]
    prior = IlnkContainer.parse(sources()[1].read_file(PATH)).blocks[19]
    for f in (4, 10, 13, 16, 18, 19):
        assert new[f * FRAME_BYTES:(f + 1) * FRAME_BYTES] == prior[f * FRAME_BYTES:(f + 1) * FRAME_BYTES]
    box = [35, 86, 47, 91]
    assert region_bytes(block[5 * FRAME_BYTES:6 * FRAME_BYTES], box) == region_bytes(new[5 * FRAME_BYTES:6 * FRAME_BYTES], box)


@pytest.mark.parametrize('index', range(4))
def test_complete_natural_phrases_and_individual_glyphs_fit(case, index):
    _, _, batch, _, proof = case
    row, evidence = batch['records'][7 + index], proof[index]
    if index < 2:
        assert evidence['font_size'] >= 9
    assert ''.join(g['character'] for g in evidence['visible_characters']) == row['english'].replace(' ', '')
    w, h = row['box'][2] - row['box'][0], row['box'][3] - row['box'][1]
    for g in evidence['visible_characters']:
        x0, y0, x1, y1 = g['bbox']
        assert 0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h
    if index == 2:
        assert row['box'][1] + evidence['full_ink_box'][3] < 51
        assert row['ink_word'] == 4173


@pytest.mark.parametrize('index', range(4))
@pytest.mark.parametrize('end', [0, -1])
def test_actual_first_last_letter_deletion_with_rehashed_payload_rejected(case, tmp_path, index, end):
    source, block, batch, _, proofs = case
    bad = copy.deepcopy(batch)
    row = bad['records'][7 + index]
    x0, y0, x1, y1 = proofs[index]['visible_characters'][end]['bbox']
    width = row['box'][2] - row['box'][0]
    payload = bytearray(zlib.decompress(bytes.fromhex(row['words_zlib_hex'])))
    if index >= 2:
        frame = block[5 * FRAME_BYTES:6 * FRAME_BYTES]
        restored, _ = restore_chase_call(row, region_bytes(frame, row['box']), block, FRAME_BYTES)
    else:
        restored = [32767] * (len(payload) // 2)
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = y * width + x
            struct.pack_into('<H', payload, i * 2, restored[i])
    row['words_zlib_hex'] = zlib.compress(payload).hex()
    row['words_sha256'] = sha(payload)
    with pytest.raises(ValueError, match='complete English glyph raster'):
        apply_raw_bgr555_art(write(tmp_path / 'missing.json', bad), source)


def test_source_outline_words_remain_exact_and_soil_does_not_seed_red_call(case):
    _, block, batch, target, proofs = case
    original = block[5 * FRAME_BYTES:6 * FRAME_BYTES]
    actual = IlnkContainer.parse(target).blocks[19][5 * FRAME_BYTES:6 * FRAME_BYTES]
    row = batch['records'][9]
    width = row['box'][2] - row['box'][0]
    for i in proofs[2]['restoration']['protected_outline_indices']:
        offset = ((row['box'][1] + i // width) * 320 + row['box'][0] + i % width) * 2
        assert original[offset:offset + 2] == actual[offset:offset + 2]
    soil = (103 * 320 + 80) * 2
    assert original[soil:soil + 2] == actual[soil:soil + 2]
    assert proofs[2]['restoration']['covered_outline_recovery_is_exact'] is False
    assert proofs[2]['restoration']['concealed_original_recovered'] is False


@pytest.mark.parametrize('change,message', [
    ('outline', 'bubble outline'), ('inkbox', 'ink box escapes'),
    ('frame', 'reviewed source call'), ('block', 'exact original block'),
])
def test_new_outline_source_and_layout_guards(case, change, message):
    _, block, batch, _, _ = case
    row = copy.deepcopy(batch['records'][9])
    frame = block[5 * FRAME_BYTES:6 * FRAME_BYTES]
    source = region_bytes(frame, row['box'])
    if change == 'outline': row['text_box'] = [0, 33, 35, 105]
    elif change == 'inkbox': row['source_ink_box'][0] = 72
    elif change == 'frame': row['image_index'] = 6
    elif change == 'block': block = block[:-2]
    with pytest.raises(ValueError, match=message):
        render_region_payload(row, source, batch, block)


def test_rehashed_scenery_or_visible_outline_mutation_rejected(case, tmp_path):
    source, _, batch, _, _ = case
    bad = copy.deepcopy(batch)
    row = bad['records'][9]
    payload = bytearray(zlib.decompress(bytes.fromhex(row['words_zlib_hex'])))
    payload[-10] ^= 1
    row['words_zlib_hex'] = zlib.compress(payload).hex()
    row['words_sha256'] = sha(payload)
    with pytest.raises(ValueError, match='complete English glyph raster'):
        apply_raw_bgr555_art(write(tmp_path / 'background.json', bad), source)


def test_all_original_color_flags_and_allocation_exact(case):
    source, block, _, target, _ = case
    actual = IlnkContainer.parse(target).blocks[19]
    assert len(source) == len(target) and source[:96] == target[:96]
    assert all(not (a ^ b) & 0x8000 for (a,), (b,) in zip(struct.iter_unpack('<H', block), struct.iter_unpack('<H', actual), strict=True))


def test_profile_one_cumulative_batch_replacement_and_all_stages_inherited():
    from scripts.build_integrated_release import load_release_stack
    profiles = load_release_stack()['profiles']
    a, b = [profiles[p] for p in ('all-routes-unified-v181', 'all-routes-unified-v182')]
    assert b['batches'] == [BATCH.as_posix() if p == OLD.as_posix() else p for p in a['batches']]
    assert len(b['batches']) == 463
    assert all(b[k] == v for k, v in a.items() if k not in ('batches', 'description', 'note'))
