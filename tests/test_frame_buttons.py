"""Complete shared action words, source locks and exact paired atlas storage."""

import copy
import json
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.build_integrated_release import apply_ilnk_pxl_sync_batch, apply_pxl_native_label_batch
from scripts.frame_buttons_v165 import (
    ARCHIVE,
    BATCH,
    LABELS,
    SYNC,
    masks,
    preservation,
    real_format_glyphs,
    sources,
    targets,
)


@pytest.fixture(scope='module')
def case():
    base, prior, _ = sources()
    target, embedded = targets()
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    return base, prior.read_file('/__arm9__.bin'), batch, target, embedded


@pytest.mark.parametrize('index', range(6))
def test_complete_word_and_first_character_rejection(case, index):
    _, source, batch, target, _ = case
    mask, origins = masks(source, batch)
    x, y = origins[index]
    mask.paste(0, (x, y, x + 5, y + 11))
    with pytest.raises(ValueError, match='first letter'):
        real_format_glyphs(source, target, batch, expected_mask=mask)
    p = PxlImage.from_bytes(target)
    for gy in range(y, y + 11):
        for gx in range(x, x + 5):
            p.indices[gy * 256 + gx] = 1
    with pytest.raises(ValueError, match='Packed button glyph'):
        real_format_glyphs(source, p.to_bytes(), batch)


def test_complete_actual_source_format_native_raster(case):
    _, source, batch, target, _ = case
    assert real_format_glyphs(source, target, batch)['dimensions'] == [256, 256]
    mask, _ = masks(source, batch)
    for row in batch['records']:
        x0, y0, x1, y1 = row['box']
        cell = mask.crop((x0, y0, x1, y1))
        assert cell.getbbox()
    assert [row['text'] for row in batch['records']] == [x[1] for x in LABELS]


def test_frame_chrome_and_embedded_palette_header_left_half_exact(case):
    _, _, _, target, embedded = case
    assert preservation(target, embedded)['embedded_right_half_exact_translated_frame_indices']


def test_embedded_border_damage_rejected(case):
    _, _, _, target, embedded = case
    container = IlnkContainer.parse(embedded)
    block = bytearray(container.blocks[5])
    block[20] ^= 1  # Outside the owned right-half lettering.
    container.blocks[5] = bytes(block)
    with pytest.raises(ValueError, match='Unowned embedded'):
        preservation(target, container.to_bytes())


def test_frame_border_damage_rejected(case):
    _, _, _, target, embedded = case
    p = PxlImage.from_bytes(target)
    p.indices[120 * 256 + 1] ^= 1
    with pytest.raises(ValueError, match='Unowned frame'):
        preservation(p.to_bytes(), embedded)


def test_source_locks_for_loose_and_embedded(case):
    base, source, _, target, _ = case
    raw = bytearray(base.read_file('/_pxl/__frame.pxl'))
    raw[-1] ^= 1
    with pytest.raises(ValueError, match='PXL source SHA-256'):
        apply_pxl_native_label_batch(BATCH, bytes(raw), source)
    archive = bytearray(base.read_file(ARCHIVE))
    archive[-1] ^= 1
    with pytest.raises(ValueError, match='ILNK source SHA-256'):
        apply_ilnk_pxl_sync_batch(SYNC, bytes(archive), target)


def test_sync_reference_and_destination_guards(case, tmp_path):
    base, _, _, target, _ = case
    wrong = bytearray(target)
    wrong[-1] ^= 1
    with pytest.raises(ValueError, match='reference PXL SHA-256'):
        apply_ilnk_pxl_sync_batch(SYNC, base.read_file(ARCHIVE), bytes(wrong))
    batch = json.loads(SYNC.read_text(encoding='utf-8'))
    batch['target_x'] = 258  # Exceeds original 512-pixel atlas width.
    path = tmp_path / 'wrong-sync.json'
    path.write_text(json.dumps(batch), encoding='utf-8')
    with pytest.raises(ValueError, match='does not fit'):
        apply_ilnk_pxl_sync_batch(path, base.read_file(ARCHIVE), target)


def test_no_visible_glyph_trim_or_width_truncation(case, tmp_path):
    base, source, batch, _, _ = case
    wrong = copy.deepcopy(batch)
    wrong['trim_blank_top_rows'] = 3
    path = tmp_path / 'wrong-font.json'
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='drop visible glyph'):
        apply_pxl_native_label_batch(path, base.read_file('/_pxl/__frame.pxl'), source)
    wrong = copy.deepcopy(batch)
    wrong['glyph_width'] = 4
    path.write_text(json.dumps(wrong), encoding='utf-8')
    with pytest.raises(ValueError, match='cropped glyph'):
        apply_pxl_native_label_batch(path, base.read_file('/_pxl/__frame.pxl'), source)


def test_exact_v164_batches_and_terminal_stages():
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a, b = registry['profiles']['all-routes-unified-v164'], registry['profiles']['all-routes-unified-v165']
    assert b['batches'] == a['batches'] + [BATCH.as_posix(), SYNC.as_posix()]
    assert len(b['batches']) == 452
    assert all(value == b[key] for key, value in a.items() if key not in ('batches', 'note', 'description'))


def test_paired_source_storage_stays_locked(case):
    base, _, _, _, _ = case
    sync = json.loads(SYNC.read_text(encoding='utf-8'))
    assert sync['source_file_sha256'] == sha(base.read_file(ARCHIVE))
    assert sync['source_block_sha256'] == sha(IlnkContainer.parse(base.read_file(ARCHIVE)).blocks[5])
