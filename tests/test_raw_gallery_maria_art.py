"""Rotated complete lettering, black footer erasure and original creator marks."""

import copy
import json
import struct
import zlib

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import FRAME_BYTES, apply_raw_bgr555_art, sha
from scripts.closing_gallery_v179 import BATCH as OLD
from scripts.maria_gallery_v180 import (
    BATCH,
    CREATOR_REGIONS,
    OUT,
    PATH,
    authored,
    preservation,
    region_bytes,
    sources,
)


def write(path, batch):
    path.write_text(json.dumps(batch), encoding="utf-8")
    return path


@pytest.fixture(scope="module")
def case():
    _, prior, source, block = sources()
    draft = OUT / "reviewed-format-draft.json"
    batch = json.loads(draft.read_text(encoding="utf-8"))
    target, _ = apply_raw_bgr555_art(draft, source)
    merged = IlnkContainer.parse(prior.read_file(PATH))
    merged.blocks[19] = IlnkContainer.parse(target).blocks[19]
    return source, block, batch, merged.to_bytes()


def test_full_source_art_creator_regions_and_previous_closing_remain_exact(case):
    _, original, batch, target = case
    evidence = preservation(target)
    assert all(row["byte_exact"] for row in evidence["creator_regions"])
    assert batch["records"][:2] == json.loads(OLD.read_text(encoding="utf-8"))["records"]
    frame = original[13 * FRAME_BYTES:14 * FRAME_BYTES]
    output = IlnkContainer.parse(target).blocks[19][13 * FRAME_BYTES:14 * FRAME_BYTES]
    for box in CREATOR_REGIONS:
        assert region_bytes(frame, box) == region_bytes(output, box)


def test_clockwise_title_glyphs_fit_and_black_footer_does_not_flood_protection(case):
    _, _, batch, _ = case
    _, evidence = authored()
    for row, proof in zip(batch["records"][2:], evidence, strict=True):
        assert ''.join(g["character"] for g in proof["visible_characters"]) == row["english"].replace(' ', '')
        width, height = row["box"][2] - row["box"][0], row["box"][3] - row["box"][1]
        for glyph in proof["visible_characters"]:
            x0, y0, x1, y1 = glyph["bbox"]
            assert 0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height
    assert evidence[0]["rotation"] == -90
    assert evidence[1]["rotation"] == 0
    assert evidence[1]["protected_colored_indices"] < 280 * 26 // 4
    # The original pause at the right was part of the sentence, not attribution.
    footer = zlib.decompress(bytes.fromhex(batch["records"][3]["words_zlib_hex"]))
    for x, y in ((262, 230), (269, 231), (276, 231)):
        assert struct.unpack_from('<H', footer, ((y - 214) * 280 + x) * 2)[0] == 0


@pytest.mark.parametrize("row_index", [2, 3])
@pytest.mark.parametrize("end", [0, -1])
def test_missing_rotated_or_footer_first_last_glyph_rehashed_still_rejected(case, tmp_path, row_index, end):
    source, _, batch, _ = case
    mutated = copy.deepcopy(batch)
    _, evidence = authored()
    row = mutated["records"][row_index]
    width = row["box"][2] - row["box"][0]
    x0, y0, x1, y1 = evidence[row_index - 2]["visible_characters"][end]["bbox"]
    payload = bytearray(zlib.decompress(bytes.fromhex(row["words_zlib_hex"])))
    for y in range(y0, y1):
        for x in range(x0, x1):
            struct.pack_into('<H', payload, (y * width + x) * 2, row["background"])
    row["words_zlib_hex"] = zlib.compress(payload).hex()
    row["words_sha256"] = sha(payload)
    with pytest.raises(ValueError, match="complete English glyph raster"):
        apply_raw_bgr555_art(write(tmp_path / 'missing.json', mutated), source)


@pytest.mark.parametrize("key,value,message", [
    ('rotation', 90, 'rotation differs'),
    ('ink_word', 32768, 'ink color differs'),
    ('background_rule', 'unknown', 'ownership rule differs'),
])
def test_new_authoring_controls_reject_invalid_values(case, tmp_path, key, value, message):
    source, _, batch, _ = case
    mutated = copy.deepcopy(batch)
    mutated["records"][2][key] = value
    with pytest.raises(ValueError, match=message):
        apply_raw_bgr555_art(write(tmp_path / 'invalid.json', mutated), source)


@pytest.mark.parametrize("x,y", [(282, 220), (20, 20)])
def test_creator_or_unowned_picture_corruption_fails_preservation(case, x, y):
    _, _, _, target = case
    archive = IlnkContainer.parse(target)
    block = bytearray(archive.blocks[19])
    block[13 * FRAME_BYTES + (y * 320 + x) * 2] ^= 1
    archive.blocks[19] = bytes(block)
    with pytest.raises(ValueError, match='Unowned picture/creator pixels'):
        preservation(archive.to_bytes())


def test_profile_supersedes_exactly_one_cumulative_batch_and_preserves_stages():
    from scripts.build_integrated_release import load_release_stack
    profiles = load_release_stack()['profiles']
    before, after = [profiles[p] for p in ('all-routes-unified-v179', 'all-routes-unified-v180')]
    assert after['batches'] == [BATCH.as_posix() if p == OLD.as_posix() else p for p in before['batches']]
    assert len(after['batches']) == 463
    assert all(after[k] == v for k, v in before.items() if k not in ('batches', 'description', 'note'))
