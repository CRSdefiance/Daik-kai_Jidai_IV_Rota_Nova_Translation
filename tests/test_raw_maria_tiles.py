"""Complete styled English, source plate edges, portraits and red-bubble borders."""

import copy
import json
import struct
import zlib
from collections import deque

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import (
    FRAME_BYTES,
    apply_raw_bgr555_art,
    render_region_payload,
    sha,
)
from scripts.creature_comic_v183 import BATCH as OLD
from scripts.maria_tiles_v184 import BATCH, OUT, PATH, authored, preservation, region_bytes, sources


@pytest.fixture(scope='module')
def case():
    _, prior, source, block = sources()
    batch = json.loads((OUT / 'reviewed-format-draft.json').read_text(encoding='utf-8'))
    target, _ = apply_raw_bgr555_art(OUT / 'reviewed-format-draft.json', source)
    merged = IlnkContainer.parse(prior.read_file(PATH))
    merged.blocks[19] = IlnkContainer.parse(target).blocks[19]
    return source, block, batch, merged.to_bytes(), authored()[1]


def frame(raw, index):
    return raw[index * FRAME_BYTES:(index + 1) * FRAME_BYTES]


def test_all_previous_records_frames_and_atlases_remain_exact(case):
    _, _, batch, target, _ = case
    assert batch['records'][:13] == json.loads(OLD.read_text(encoding='utf-8'))['records']
    assert preservation(target)['unowned_bytes_exact']


@pytest.mark.parametrize('index', [0, 1, 2])
def test_full_logical_heading_or_paragraph_glyphs_and_readable_size(case, index):
    _, _, batch, _, proofs = case
    row, proof = batch['records'][13 + index], proofs[index]
    assert ''.join(g['character'] for g in proof['visible_characters']) == row['english'].replace(' ', '')
    if index == 1:
        assert proof['font_size'] == 9
        assert ' '.join(proof['automatic_lines']) == row['english']
        assert '\n' not in row['english'] and row.get('text_box') is None
    else:
        assert ''.join(p['text'] for p in proof['segments']) == 'MariaMode'
        assert min(p['font_size'] for p in proof['segments']) >= 19
    w, h = row['box'][2] - row['box'][0], row['box'][3] - row['box'][1]
    for glyph in proof['visible_characters']:
        x0, y0, x1, y1 = glyph['bbox']
        assert 0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h


@pytest.mark.parametrize('index', [0, 1, 2])
@pytest.mark.parametrize('end', [0, -1])
def test_rehashed_actual_first_last_glyph_deletion_rejected(case, tmp_path, index, end):
    source, _, batch, _, proofs = case
    bad = copy.deepcopy(batch);row = bad['records'][13 + index]
    payload = bytearray(zlib.decompress(bytes.fromhex(row['words_zlib_hex'])))
    width = row['box'][2] - row['box'][0]
    background = (4246 if index == 0 else 0) if end == 0 and index != 1 else 32767
    x0, y0, x1, y1 = proofs[index]['visible_characters'][end]['bbox']
    for y in range(y0, y1):
        for x in range(x0, x1):
            struct.pack_into('<H', payload, (y * width + x) * 2, background)
    row['words_zlib_hex'] = zlib.compress(payload).hex();row['words_sha256'] = sha(payload)
    path = tmp_path / 'missing.json';path.write_text(json.dumps(bad), encoding='utf-8')
    with pytest.raises(ValueError, match='complete English glyph raster'):
        apply_raw_bgr555_art(path, source)


def test_black_plate_and_visible_red_plate_outer_edges_are_exact(case):
    _, original, _, target, _ = case
    a = frame(original, 12);b = frame(IlnkContainer.parse(target).blocks[19], 12)
    points = {(x, y) for y in range(16, 64) for x in range(259, 310)
              if x in (259, 309) or y in (16, 63)}
    points |= {(x, y) for y in range(48, 95) for x in range(228, 272)
               if (x in (228, 271) or y in (48, 94)) and not (x >= 259 and y < 64)}
    assert all(a[(y * 320 + x) * 2:(y * 320 + x) * 2 + 2] == b[(y * 320 + x) * 2:(y * 320 + x) * 2 + 2] for x, y in points)


def test_tilted_pink_tile_edge_and_exterior_white_component_exact(case):
    _, original, _, target, _ = case
    a = frame(original, 12);b = frame(IlnkContainer.parse(target).blocks[19], 12)
    word = lambda raw, x, y: struct.unpack_from('<H', raw, (y * 320 + x) * 2)[0]
    white = {(x, y) for y in range(92, 147) for x in range(248, 310) if word(a, x, y) == 32767}
    q = deque(p for p in white if p[0] in (248, 309) or p[1] in (92, 146));exterior = set(q)
    while q:
        x, y = q.popleft()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            p = x + dx, y + dy
            if p in white and p not in exterior:exterior.add(p);q.append(p)
    assert len(exterior) > 1600
    assert all(word(a, x, y) == word(b, x, y) for x, y in exterior)
    edge = {(x + dx, y + dy) for x, y in exterior for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if 248 <= x + dx < 310 and 92 <= y + dy < 147 and word(a, x + dx, y + dy) != 32767}
    assert all(word(a, x, y) == word(b, x, y) for x, y in edge)


def test_whole_character_art_and_chibi_companions_byte_exact(case):
    _, original, _, target, _ = case
    new = IlnkContainer.parse(target).blocks[19]
    for f, box in [(11, [0, 0, 137, 240]), (12, [0, 0, 192, 240])]:
        assert region_bytes(frame(original, f), box) == region_bytes(frame(new, f), box)


def test_original_monochrome_speech_contour_words_remain_exact(case):
    _, original, _, target, _ = case
    a = frame(original, 11);b = frame(IlnkContainer.parse(target).blocks[19], 11);count = 0
    for y in range(18, 82):
        for x in range(130, 320):
            v = struct.unpack_from('<H', a, (y * 320 + x) * 2)[0]
            channels = [(v >> (5 * c)) & 31 for c in range(3)]
            if max(channels) < 31 and max(channels) - min(channels) <= 1:
                count += 1
                assert a[(y * 320 + x) * 2:(y * 320 + x) * 2 + 2] == b[(y * 320 + x) * 2:(y * 320 + x) * 2 + 2]
    assert count > 300


@pytest.mark.parametrize('change', ['box', 'font'])
def test_concrete_source_layout_and_font_guards(case, change):
    _, block, batch, _, _ = case
    row = copy.deepcopy(batch['records'][13]);bad = copy.deepcopy(batch)
    source = region_bytes(frame(block, 11), row['box'])
    if change == 'box':row['box'][0] = 136
    else:bad['font_sha256'] = '0' * 64
    with pytest.raises(ValueError, match='source heading|font identity'):
        render_region_payload(row, source, bad, block)


def test_all_original_flags_and_archive_geometry_exact(case):
    source, block, _, target, _ = case
    new = IlnkContainer.parse(target).blocks[19]
    assert len(source) == len(target) and source[:96] == target[:96]
    assert all(not (a ^ b) & 0x8000 for (a,), (b,) in zip(struct.iter_unpack('<H', block), struct.iter_unpack('<H', new), strict=True))


def test_profile_replaces_one_cumulative_batch_and_preserves_all_stages():
    from scripts.build_integrated_release import load_release_stack
    profiles = load_release_stack()['profiles'];a, b = [profiles[p] for p in ('all-routes-unified-v183', 'all-routes-unified-v184')]
    assert b['batches'] == [BATCH.as_posix() if p == OLD.as_posix() else p for p in a['batches']]
    assert len(b['batches']) == 463
    assert all(b[k] == value for k, value in a.items() if k not in ('batches', 'description', 'note'))
