"""Disjoint atlas regions cannot revert prior captions or damage unowned storage."""
import copy
import json
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_ilnk_pxl_sync_batch, apply_ilnk_pxl_sync_batches
from scripts.marker_cmmnimg_v172 import (
    ARCHIVE,
    FRAME,
    FRAME_SYNC,
    MARKER,
    PROFILE,
    SYNC,
    preservation,
    sources,
    targets,
)


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    refs = {FRAME: prior.read_file(FRAME), MARKER: base.read_file(MARKER)}
    target, ids = targets()
    return base.read_file(ARCHIVE), refs, target, ids


def test_both_regions_complete_and_other_storage_exact(case):
    _, _, target, ids = case
    assert preservation(target)['changed_pixel_count'] == 4312
    assert ids == ['DK4_FRAME_ACTION_CMMNIMG_SYNC_V1', 'DK4_MARKER_CMMNIMG_SYNC_V1']


def test_order_independent_disjoint_regions(case):
    source, refs, target, _ = case
    actual, ids = apply_ilnk_pxl_sync_batches([SYNC, FRAME_SYNC], source, refs)
    assert actual == target
    assert ids == ['DK4_MARKER_CMMNIMG_SYNC_V1', 'DK4_FRAME_ACTION_CMMNIMG_SYNC_V1']


@pytest.mark.parametrize('batch', [SYNC, FRAME_SYNC])
def test_single_region_backward_compatibility(case, batch):
    source, refs, _, _ = case
    header = json.loads(batch.read_text(encoding='utf-8'))
    assert apply_ilnk_pxl_sync_batches([batch], source, refs) == apply_ilnk_pxl_sync_batch(
        batch, source, refs[header['source_image_path']])


@pytest.mark.parametrize('x', [0, 2, 254])
def test_partial_or_full_overlap_rejected(case, tmp_path, x):
    source, refs, _, _ = case
    header = json.loads(FRAME_SYNC.read_text(encoding='utf-8'))
    header['target_x'] = x
    path = tmp_path / 'overlap.json'
    path.write_text(json.dumps(header), encoding='utf-8')
    with pytest.raises(ValueError, match='overlapping'):
        apply_ilnk_pxl_sync_batches([SYNC, path], source, refs)


def test_inconsistent_same_block_geometry_rejected(case, tmp_path):
    source, refs, _, _ = case
    header = json.loads(FRAME_SYNC.read_text(encoding='utf-8'))
    header.update(target_width=256, target_height=512, target_x=0, target_y=256)
    path = tmp_path / 'geometry.json'
    path.write_text(json.dumps(header), encoding='utf-8')
    with pytest.raises(ValueError, match='inconsistent'):
        apply_ilnk_pxl_sync_batches([SYNC, path], source, refs)


@pytest.mark.parametrize('offset, message', [(20, 'marker pixel'), (148, 'right-half'), (0, 'header')])
def test_lost_letter_prior_frame_or_header_rejected(case, offset, message):
    _, _, target, _ = case
    a = IlnkContainer.parse(target)
    block = bytearray(a.blocks[5])
    block[offset] ^= 1
    a.blocks[5] = bytes(block)
    with pytest.raises(ValueError, match=message):
        preservation(a.to_bytes())


def test_source_and_reference_lock_rejected(case):
    source, refs, _, _ = case
    wrong_source = bytearray(source)
    wrong_source[-1] ^= 1
    with pytest.raises(ValueError, match='source SHA-256'):
        apply_ilnk_pxl_sync_batches([SYNC], bytes(wrong_source), refs)
    wrong_refs = copy.deepcopy(refs)
    wrong = bytearray(refs[MARKER])
    wrong[-1] ^= 1
    wrong_refs[MARKER] = bytes(wrong)
    with pytest.raises(ValueError, match='reference PXL SHA-256'):
        apply_ilnk_pxl_sync_batches([SYNC], source, wrong_refs)


@pytest.mark.parametrize('edge', ['first', 'last'])
def test_accepted_caption_edge_ink_cannot_be_lost(case, edge):
    _, refs, target, _ = case
    marker = PxlImage.from_bytes(refs[MARKER])
    ink = [(x, y) for x in range(68, 106) for y in range(4, 13)
           if marker.indices[y * 256 + x] == 15]
    x, y = ink[0] if edge == 'first' else ink[-1]
    a = IlnkContainer.parse(target)
    block = bytearray(a.blocks[5])
    offset = 20 + y * 256 + x // 2
    block[offset] ^= 1 << (4 if x & 1 else 0)
    a.blocks[5] = bytes(block)
    with pytest.raises(ValueError, match='first or final letter'):
        preservation(a.to_bytes())


def test_duplicate_record_id_rejected(case, tmp_path):
    source, refs, _, _ = case
    header = json.loads(SYNC.read_text(encoding='utf-8'))
    header['id'] = json.loads(FRAME_SYNC.read_text(encoding='utf-8'))['id']
    path = tmp_path / 'duplicate.json'
    path.write_text(json.dumps(header), encoding='utf-8')
    with pytest.raises(ValueError, match='duplicate'):
        apply_ilnk_pxl_sync_batches([FRAME_SYNC, path], source, refs)


def test_all_v171_batches_and_terminal_stages_exact():
    s = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = s['profiles']['all-routes-unified-v171'], s['profiles'][PROFILE]
    assert b['batches'] == a['batches'] + [SYNC.as_posix()]
    assert len(b['batches']) == 453
    assert all(value == b[key] for key, value in a.items() if key not in ('batches', 'note', 'description'))
