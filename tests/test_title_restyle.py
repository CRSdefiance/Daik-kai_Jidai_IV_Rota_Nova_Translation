"""Native-size wordmark coverage, source gold and complete payload regressions."""

import copy
import json
import zlib

import pytest

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import (
    apply_fls_indexed_region_batch,
    apply_pxl_indexed_region_batch,
)
from scripts.title_restyle_v186 import (
    ASSET_SHA,
    FLS_BATCH,
    FLS_BOXES,
    FLS_PATH,
    SPECS,
    batch_path,
    fls_regions,
    pxl_regions,
    sha,
    sources,
    targets,
    verify_art,
    wordmark,
)


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    return base, prior, targets()


def test_wordmark_has_soft_edges_full_bounded_lines_and_locked_asset():
    image, crop = wordmark()
    alpha = image.getchannel('A')
    box = alpha.getbbox()
    assert image.height == 42 and 170 < image.width < 200
    assert 0 <= box[0] < box[2] <= image.width
    assert 0 <= box[1] < box[3] <= image.height
    assert sum(0 < a < 255 for a in alpha.tobytes()) > 300
    assert crop == (155, 159, 1978, 593)
    assert ASSET_SHA == 'e357836b83dc8c527a16954d4fd5a007a102d59a33a5e7663903f9f950822d28'
    # Both visibly checked source lines include their leading and final letters.
    for y0, y1 in [(0, 21), (21, 42)]:
        assert alpha.crop((0, y0, image.width, y1)).getbbox() is not None


def test_all_source_headers_palettes_gold_and_unowned_pixels_exact(case):
    cases = verify_art(case[2])
    assert len(cases) == 4
    assert all(c['header_palette_unowned_gold_copyright_exact'] for c in cases[:3])


@pytest.mark.parametrize('spec', SPECS, ids=lambda s: s['name'])
def test_all_pxl_caption_blue_and_white_fringe_removed(case, spec):
    image = PxlImage.from_bytes(case[2][spec['path']])
    x0, y0, x1, y1 = spec['caption']
    pixels, proof = pxl_regions(spec)
    assert proof[1]['caption_policy'] == 'omit-redundant-phonetic-label'
    assert proof[0]['hard_alpha_threshold_used'] is False
    assert proof[0]['soft_coverage_pixels'] > 300
    if spec['name'] == 'logo':
        # Former caption lower outline must not leave floating white dots.
        assert all(image.palette[image.indices[y * 256 + x]][:3] == (0, 0, 0)
                   for y in (133, 134) for x in range(159, 201))
    else:
        base = case[0]
        donor = PxlImage.from_bytes(base.read_file(spec['background']))
        protected = set(proof[1]['protected_original_indices'])
        for y in range(y0, y1):
            for x in range(x0, x1):
                i = (y - y0) * (x1 - x0) + x - x0
                if i not in protected:
                    rgb = image.palette[pixels[1][i]][:3]
                    wanted = donor.palette[donor.indices[y * 256 + x]][:3]
                    assert sum(abs(a - b) for a, b in zip(rgb, wanted, strict=True)) < 100


@pytest.mark.parametrize('spec', SPECS, ids=lambda s: s['name'])
@pytest.mark.parametrize('end', ['first', 'last'])
def test_rehashed_leading_or_trailing_art_deletion_fails_complete_art_verifier(case, spec, end):
    image = PxlImage.from_bytes(case[2][spec['path']])
    word, _ = wordmark()
    x0, y0, x1, _ = spec['main']
    ox = (x1 - x0 - word.width) // 2
    start = 0 if end == 'first' else word.width - 20
    for y in range(21):
        for x in range(start, start + 20):
            image.indices[(y0 + y) * 256 + x0 + ox + x] = 0
    broken = dict(case[2])
    broken[spec['path']] = image.to_bytes()
    with pytest.raises(ValueError, match='full wordmark'):
        verify_art(broken)


@pytest.mark.parametrize('index,end', [(4, 'first'), (4, 'last')])
def test_fls_rehashed_letter_deletion_fails_complete_art_verifier(case, tmp_path, index, end):
    batch = copy.deepcopy(json.loads(FLS_BATCH.read_text(encoding='utf-8')))
    row = next(r for r in batch['records'] if r['asset_index'] == index)
    payload = bytearray(zlib.decompress(bytes.fromhex(row['indices_zlib_hex'])))
    word, _ = wordmark()
    w = FLS_BOXES[index][2] - FLS_BOXES[index][0]
    ox = (w - word.width) // 2
    start = 0 if end == 'first' else word.width - 20
    for y in range(21):
        for x in range(start, start + 20):
            payload[y * w + x + ox] = 0
    row['indices_zlib_hex'] = zlib.compress(payload).hex()
    row['indices_sha256'] = sha(payload)
    path = tmp_path / 'missing-letter.json'
    path.write_text(json.dumps(batch), encoding='utf-8')
    broken = dict(case[2])
    broken[FLS_PATH] = apply_fls_indexed_region_batch(path, case[0].read_file(FLS_PATH))[0]
    with pytest.raises(ValueError, match='Opening artwork'):
        verify_art(broken)


def test_fls_latin_title_and_original_record_geometry_retained(case):
    source = FlsArchive(case[0].read_file(FLS_PATH))
    result = FlsArchive(case[2][FLS_PATH])
    assert source.records == result.records
    assert source.texture(5).palette == result.texture(5).palette
    _, proof = fls_regions()
    assert proof[1]['meaning'] == 'Rota Nova'
    assert proof[1]['caption_policy'] == 'omit-redundant-phonetic-label'


def test_pxl_source_hash_guard_rejects_wrong_base(case, tmp_path):
    batch = copy.deepcopy(json.loads(batch_path(SPECS[0]).read_text(encoding='utf-8')))
    batch['source_file_sha256'] = '0' * 64
    path = tmp_path / 'wrong-source.json'
    path.write_text(json.dumps(batch), encoding='utf-8')
    with pytest.raises(ValueError, match='source SHA'):
        apply_pxl_indexed_region_batch(path, case[0].read_file(SPECS[0]['path']))
