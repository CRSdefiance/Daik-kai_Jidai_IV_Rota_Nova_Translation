"""Whole lettering and independently sampled original bubble/portrait preservation."""

import copy
import json
import struct
import zlib
from collections import deque

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import FRAME_BYTES, apply_raw_bgr555_art, sha
from scripts.chase_comic_v182 import BATCH as OLD
from scripts.creature_comic_v183 import BATCH, OUT, PATH, authored, preservation, sources


@pytest.fixture(scope='module')
def case():
    _, prior, source, block = sources()
    batch = json.loads((OUT / 'reviewed-format-draft.json').read_text(encoding='utf-8'))
    target, _ = apply_raw_bgr555_art(OUT / 'reviewed-format-draft.json', source)
    merged = IlnkContainer.parse(prior.read_file(PATH))
    merged.blocks[19] = IlnkContainer.parse(target).blocks[19]
    return source, block, batch, merged.to_bytes(), authored()[1]


def test_all_previous_records_frames_atlases_and_unowned_art_exact(case):
    _, _, batch, target, _ = case
    assert batch['records'][:11] == json.loads(OLD.read_text(encoding='utf-8'))['records']
    proof = preservation(target)
    assert proof['unowned_bytes_exact']
    assert proof['changed_frame_indices'] == [8]


@pytest.mark.parametrize('index', [0, 1])
def test_full_question_reply_letters_fit_at_readable_size(case, index):
    _, _, batch, _, proofs = case
    row, proof = batch['records'][11 + index], proofs[index]
    assert proof['font_size'] == 11
    assert ''.join(g['character'] for g in proof['visible_characters']) == row['english'].replace(' ', '')
    width, height = row['box'][2] - row['box'][0], row['box'][3] - row['box'][1]
    for glyph in proof['visible_characters']:
        x0, y0, x1, y1 = glyph['bbox']
        assert 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height


@pytest.mark.parametrize('index', [0, 1])
@pytest.mark.parametrize('end', [0, -1])
def test_rehashed_first_or_last_glyph_deletion_rejected(case, tmp_path, index, end):
    source, _, batch, _, proofs = case
    bad = copy.deepcopy(batch)
    row = bad['records'][11 + index]
    width = row['box'][2] - row['box'][0]
    payload = bytearray(zlib.decompress(bytes.fromhex(row['words_zlib_hex'])))
    x0, y0, x1, y1 = proofs[index]['visible_characters'][end]['bbox']
    for y in range(y0, y1):
        for x in range(x0, x1):
            struct.pack_into('<H', payload, (y * width + x) * 2, 32767)
    row['words_zlib_hex'] = zlib.compress(payload).hex()
    row['words_sha256'] = sha(payload)
    path = tmp_path / 'missing.json'
    path.write_text(json.dumps(bad), encoding='utf-8')
    with pytest.raises(ValueError, match='complete English glyph raster'):
        apply_raw_bgr555_art(path, source)


def test_whole_original_bubble_contours_and_tail_pixels_exact(case):
    # Trace neutral edge components crossing the text-plane boundary, independently
    # of the author's protected-corner rectangles or renderer evidence.
    _, block, _, target, _ = case
    original = block[8 * FRAME_BYTES:9 * FRAME_BYTES]
    actual = IlnkContainer.parse(target).blocks[19][8 * FRAME_BYTES:9 * FRAME_BYTES]
    pixels = [v for v, in struct.iter_unpack('<H', original)]
    for plane, region in [([239, 29, 284, 89], [221, 18, 301, 112]),
                          ([43, 144, 73, 209], [19, 134, 96, 217])]:
        px0, py0, px1, py1 = plane
        rx0, ry0, rx1, ry1 = region
        edge = set()
        for y in range(ry0, ry1):
            for x in range(rx0, rx1):
                i = y * 320 + x
                channels = [(pixels[i] >> (5 * c)) & 31 for c in range(3)]
                if max(channels) < 31 and max(channels) - min(channels) <= 2:
                    edge.add(i)
        pending = deque(i for i in edge if not (px0 <= i % 320 < px1 and py0 <= i // 320 < py1))
        traced = set(pending)
        while pending:
            i = pending.popleft()
            x, y = i % 320, i // 320
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if not rx0 <= x + dx < rx1 or not ry0 <= y + dy < ry1:
                        continue
                    j = (y + dy) * 320 + x + dx
                    if j in edge and j not in traced:
                        traced.add(j)
                        pending.append(j)
        assert len(traced) > 100
        assert all(original[i * 2:i * 2 + 2] == actual[i * 2:i * 2 + 2] for i in traced)


@pytest.mark.parametrize('x,y', [(55, 146), (57, 207)])
def test_reply_top_bottom_ghost_glyph_regression(case, x, y):
    _, _, _, target, _ = case
    actual = IlnkContainer.parse(target).blocks[19]
    assert struct.unpack_from('<H', actual, 8 * FRAME_BYTES + (y * 320 + x) * 2)[0] == 32767


def test_source_high_bits_archive_extent_and_wordplay_note(case):
    source, block, batch, target, _ = case
    actual = IlnkContainer.parse(target).blocks[19]
    assert source[:96] == target[:96] and len(source) == len(target)
    assert all(not (a ^ b) & 0x8000 for (a,), (b,) in zip(struct.iter_unpack('<H', block), struct.iter_unpack('<H', actual), strict=True))
    assert 'not an official game creature name' in batch['records'][12]['localization_note']


def test_registered_stack_replaces_only_one_raw_batch_and_keeps_stages():
    from scripts.build_integrated_release import load_release_stack
    profiles = load_release_stack()['profiles']
    a, b = [profiles[p] for p in ('all-routes-unified-v182', 'all-routes-unified-v183')]
    assert b['batches'] == [BATCH.as_posix() if p == OLD.as_posix() else p for p in a['batches']]
    assert len(b['batches']) == 463
    assert all(b[k] == value for k, value in a.items() if k not in ('batches', 'description', 'note'))
