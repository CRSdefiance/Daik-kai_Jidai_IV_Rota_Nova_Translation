"""Protect reviewed raw comic art after all integrated release stages.

This is a final preservation contract. It supplies no original comic viewer,
native viewport, GPU alpha, hidden-source recovery or visual acceptance proof.
"""

import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import BLOCK_SHA, FORMAT, FRAME_BYTES, apply_raw_bgr555_art

FILE = '/GRP/SLACKIMG.DK4'
MARK_FRAME, MARK_BOX = 6, (175, 96, 229, 136)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def region(block, frame, box):
    left, top, right, bottom = box
    return b''.join(block[frame * FRAME_BYTES + (y * 320 + left) * 2:
                          frame * FRAME_BYTES + (y * 320 + right) * 2]
                    for y in range(top, bottom))


def verify_final_raw_art(candidate, baseline, clean, batch_paths):
    """Read final candidate bytes; permit unrelated archive sync blocks."""
    batches = []
    for path in batch_paths:
        path = Path(path)
        batch = json.loads(path.read_text(encoding='utf-8'))
        if batch.get('format') == FORMAT:
            batches.append((path, batch))
    result = {'applicable': bool(batches), 'families': [],
              'source_restoration_and_actual_display_review_not_inferred': True}
    if not batches:
        return result
    if len(batches) != 1 or batches[0][1].get('file_path') != FILE:
        raise ValueError('Final raw-art contract requires one reviewed SLACK comic batch')
    path, batch = batches[0]
    source = baseline.read_file(FILE)
    expected_archive, ids = apply_raw_bgr555_art(path, source)
    original_archive = IlnkContainer.parse(source)
    original = original_archive.blocks[19]
    clean_original = IlnkContainer.parse(clean.read_file(FILE)).blocks[19]
    if original != clean_original or digest(original) != BLOCK_SHA:
        raise ValueError('Final raw-art source must retain the exact clean Japanese comic block')
    actual_archive = candidate.read_file(FILE)
    header_bytes = 8 + (len(original_archive.blocks) + 1) * 4
    if len(actual_archive) != len(source) or actual_archive[:header_bytes] != source[:header_bytes]:
        raise ValueError('Final raw-art archive allocation or block table changed')
    actual = IlnkContainer.parse(actual_archive).blocks[19]
    if len(actual) != 21 * FRAME_BYTES:
        raise ValueError('Final raw-art complete comic extent differs')
    if any((a ^ b) & 0x80 for a, b in zip(original[1::2], actual[1::2], strict=True)):
        raise ValueError('Final raw-art original high color bits changed')
    marks = region(actual, MARK_FRAME, MARK_BOX)
    if marks != region(original, MARK_FRAME, MARK_BOX):
        raise ValueError('Final raw-art user-preserved brown marks changed')
    expected = IlnkContainer.parse(expected_archive).blocks[19]
    owned = bytearray(len(original))
    rows, frames = [], set()
    for row in batch['records']:
        frame, box = int(row['image_index']), tuple(row['box'])
        left, top, right, bottom = box
        for y in range(top, bottom):
            lo = frame * FRAME_BYTES + (y * 320 + left) * 2
            hi = frame * FRAME_BYTES + (y * 320 + right) * 2
            owned[lo:hi] = b'\1' * (hi - lo)
        full = region(actual, frame, box)
        if full != region(expected, frame, box):
            raise ValueError('Final raw-art caption letters or reviewed restoration changed: ' + row['id'])
        frames.add(frame)
        rows.append({'id': row['id'], 'english': row['english'], 'frame': frame, 'box': list(box),
                     'complete_region_bytes': len(full), 'sha256': digest(full),
                     'complete_reviewed_glyph_and_restoration_plane_exact': True})
    if any(a != b and not flag for a, b, flag in zip(original, actual, owned, strict=True)):
        raise ValueError('Final raw-art unowned source artwork changed')
    if actual != expected:
        raise ValueError('Final raw-art whole block differs from its source-bound reconstruction')
    untouched = [n for n in range(21) if n not in frames]
    if any(actual[n * FRAME_BYTES:(n + 1) * FRAME_BYTES] != original[n * FRAME_BYTES:(n + 1) * FRAME_BYTES]
           for n in untouched):
        raise ValueError('Final raw-art untouched frame differs')
    result['families'].append({'file_path': FILE, 'batch': str(path), 'batch_sha256': digest(path.read_bytes()),
        'source_block_sha256': BLOCK_SHA, 'final_block_sha256': digest(actual), 'complete_block_bytes': len(actual),
        'record_ids': ids, 'complete_caption_regions': rows, 'untouched_frames': untouched,
        'all_unowned_source_bytes_and_original_high_bits_exact': True,
        'approved_brown_mark_bytes': len(marks), 'approved_brown_mark_sha256': digest(marks),
        'other_archive_blocks_left_to_their_registered_sync_contracts': True})
    return result
