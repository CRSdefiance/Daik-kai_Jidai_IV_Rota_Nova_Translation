"""Whole English glyphs and independent source-art regressions for the reveal."""

import copy
import json
import struct
import zlib

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import FRAME_BYTES, apply_raw_bgr555_art, sha
from scripts.maria_tiles_v184 import BATCH as OLD
from scripts.reveal_comic_v185 import OUT, PATH, authored, preservation, sources


@pytest.fixture(scope='module')
def case():
    _, prior, source, block = sources()
    draft = OUT / 'reviewed-format-draft.json'
    batch = json.loads(draft.read_text(encoding='utf-8'))
    target, _ = apply_raw_bgr555_art(draft, source)
    merged = IlnkContainer.parse(prior.read_file(PATH))
    merged.blocks[19] = IlnkContainer.parse(target).blocks[19]
    return source, block, batch, merged.to_bytes(), authored()[1]


def pixel(block, frame, x, y):
    return struct.unpack_from('<H', block, frame * FRAME_BYTES + (y * 320 + x) * 2)[0]


def test_prior_sixteen_records_and_other_frames_atlases_are_exact(case):
    _, _, batch, target, _ = case
    assert batch['records'][:16] == json.loads(OLD.read_text(encoding='utf-8'))['records']
    assert preservation(target)['unowned_bytes_exact']


@pytest.mark.parametrize('frame,text,size', [(6, 'Huh?!', 9), (7, 'TA-DA!', 28)])
def test_complete_clear_english(case, frame, text, size):
    proof = next(c for c in case[4] if c['image_index'] == frame)
    assert ''.join(g['character'] for g in proof['visible_characters']) == text
    assert proof['font_size'] == size
    assert proof['automatic_lines'] == [text]
    if frame == 7:
        assert proof['full_ink_box'][3] <= 24  # All English above source horns.
    else:
        assert proof['full_ink_box'][2] < 88  # Photo begins at x88.


@pytest.mark.parametrize('frame', [6, 7])
@pytest.mark.parametrize('end', [0, -1])
def test_fresh_hash_cannot_hide_deleted_first_or_final_letter(case, tmp_path, frame, end):
    source, block, original, _, proofs = case
    batch = copy.deepcopy(original)
    row = next(r for r in batch['records'] if r['image_index'] == frame)
    proof = next(c for c in proofs if c['image_index'] == frame)
    bbox = proof['visible_characters'][end]['bbox']
    payload = bytearray(zlib.decompress(bytes.fromhex(row['words_zlib_hex'])))
    x0, y0, x1, _ = row['box']
    for y in range(bbox[1], bbox[3]):
        for x in range(bbox[0], bbox[2]):
            struct.pack_into('<H', payload, ((y - y0) * (x1 - x0) + x - x0) * 2,
                             pixel(block, frame, x, y))
    row['words_sha256'] = sha(payload)
    row['words_zlib_hex'] = zlib.compress(payload).hex()
    path = tmp_path / 'deleted-letter.json'
    path.write_text(json.dumps(batch), encoding='utf-8')
    with pytest.raises(ValueError, match='complete English glyph raster'):
        apply_raw_bgr555_art(path, source)


def test_question_bubble_crew_photo_and_ambiguous_water_marks_exact(case):
    source = case[1]
    target = IlnkContainer.parse(case[3]).blocks[19]
    # Independently pinned source areas, not the renderer's mask.
    for box in [(41, 40, 111, 99), (104, 99, 234, 171), (88, 125, 234, 171),
                (178, 103, 226, 136), (88, 75, 90, 171)]:
        x0, y0, x1, y1 = box
        for y in range(y0, y1):
            for x in range(x0, x1):
                assert pixel(source, 6, x, y) == pixel(target, 6, x, y)


def test_creature_core_horns_spike_and_people_exact(case):
    source = case[1]
    target = IlnkContainer.parse(case[3]).blocks[19]
    for box in [(119, 34, 129, 62), (178, 35, 185, 62), (152, 56, 159, 94),
                (119, 75, 185, 114), (0, 114, 320, 240)]:
        x0, y0, x1, y1 = box
        for y in range(y0, y1):
            for x in range(x0, x1):
                assert pixel(source, 7, x, y) == pixel(target, 7, x, y)


def test_remaining_source_green_letters_removed_outside_foreground(case):
    target = IlnkContainer.parse(case[3]).blocks[19]
    # Large former letter bodies separated from the foreground.
    for box in [(23, 23, 70, 58), (30, 65, 73, 101), (225, 17, 270, 60),
                (280, 30, 310, 60), (245, 76, 284, 98)]:
        x0, y0, x1, y1 = box
        for y in range(y0, y1):
            for x in range(x0, x1):
                w = pixel(target, 7, x, y)
                r, g, b = (w >> shift & 31 for shift in (0, 5, 10))
                assert not (g >= r + 2 and r >= b + 2)


def test_no_high_bits_or_unproved_native_claims(case):
    source = case[1]
    target = IlnkContainer.parse(case[3]).blocks[19]
    assert all((a ^ b) & 32768 == 0 for (a,), (b,) in zip(
        struct.iter_unpack('<H', source), struct.iter_unpack('<H', target), strict=True))
    assert all(not p['actual_native_display_verified'] and not p['original_hidden_scenery_recovered'] for p in case[4])


@pytest.mark.parametrize('field,value', [('english', 'TA-DA'), ('size', 27), ('box', [0, 0, 320, 115])])
def test_source_specific_contract_rejects_format_changes(case, tmp_path, field, value):
    batch = copy.deepcopy(case[2])
    row = next(r for r in batch['records'] if r['image_index'] == 7)
    row[field] = value
    path = tmp_path / 'invalid-contract.json'
    path.write_text(json.dumps(batch), encoding='utf-8')
    with pytest.raises(ValueError):
        apply_raw_bgr555_art(path, case[0])
