from pathlib import Path

import pytest

from scripts.compile_scene_caption_single_dispatch import (
    OFFSET,
    compile_dispatch,
    compile_scoped_dispatch,
)
from scripts.execute_scene_caption_raster import execute
from scripts.probe_scene_caption_raster import expected_pixels


@pytest.fixture(scope='module')
def source():
    return Path('work/analysis/scene_caption_complete_tracking_v137/proposed_arm9.bin').read_bytes()


@pytest.mark.parametrize('mode', [4, 16])
def test_actual_pair_overlap_and_complete_single_dispatch(source, mode):
    before = execute(source, 'Maria', mode=mode)
    after = execute(compile_dispatch(source), 'Maria', mode=mode)
    assert [g['x'] for g in before['glyphs'][:5]] == [18, 24, 28, 34, 38]
    assert [g['x'] for g in after['glyphs']] == [18, 23, 28, 33, 38]
    assert [g['code'] for g in after['glyphs']] == list(b'Maria')
    assert after['pixels'] == expected_pixels(source, 'Maria', 18, 70, mode)
    assert before['pixels'] != after['pixels']


@pytest.mark.parametrize('mode', [4, 16])
def test_full_blank_character_and_last_character(source, mode):
    result = execute(compile_dispatch(source), 'A B!', mode=mode)
    assert [g['code'] for g in result['glyphs']] == list(b'A B!')
    assert result['pixels'] == expected_pixels(source, 'A B!', 18, 70, mode)
    assert result['final_x'] == 38


def test_dispatch_source_and_vtable_mutations_rejected(source):
    for offset in (OFFSET, OFFSET + 40, 0x160400):
        changed = bytearray(source)
        changed[offset] ^= 1
        with pytest.raises(ValueError):
            compile_dispatch(changed)


@pytest.mark.parametrize('tracking', [0, 1, -2])
def test_other_tracking_keeps_native_pair_flush(source, tracking):
    before = execute(source, 'Maria', tracking=tracking)
    after = execute(compile_dispatch(source), 'Maria', tracking=tracking)
    for field in ('glyphs', 'pixels', 'final_x', 'copy_calls'):
        assert before[field] == after[field]
    assert after['glyphs'][-1]['code'] == 32


@pytest.mark.parametrize('mode', [4, 16])
@pytest.mark.parametrize('text', ['Maria', 'L1', 'R1', 'A港町B'])
def test_scoped_repair_preserves_controller_class_even_at_minus_one(source, mode, text):
    before = execute(source, text, tracking=-1, mode=mode, font_class='controller-icons')
    after = execute(compile_scoped_dispatch(source), text, tracking=-1, mode=mode,
                    font_class='controller-icons')
    for field in ('glyphs', 'cp932_glyphs', 'pixels', 'final_x', 'copy_calls'):
        assert before[field] == after[field]


@pytest.mark.parametrize('text', ['港町', 'A港町B', 'AB港町C'])
def test_compact_cp932_keeps_bytes_and_odd_address_consumption(source, text):
    before = execute(source, text, tracking=0)
    after = execute(compile_scoped_dispatch(source), text, tracking=0)
    for field in ('glyphs', 'cp932_glyphs', 'pixels', 'final_x'):
        assert before[field] == after[field]
    assert [g['code'] for g in after['cp932_glyphs']] == [0x8D60, 0x92AC]


def test_scoped_class_and_cp932_source_mutations_rejected(source):
    for offset in (0xD570C, 0xD5778, 0x152DD4, 0x160400):
        changed = bytearray(source)
        changed[offset] ^= 1
        with pytest.raises(ValueError):
            compile_scoped_dispatch(changed)
    changed = bytearray(source)
    changed[0x100:0x104] = bytes.fromhex('a84d0d02')
    with pytest.raises(ValueError, match='Unmapped font class'):
        compile_scoped_dispatch(changed)


@pytest.mark.parametrize('mode', [4, 16])
def test_scoped_generic_pixels_retain_full_caption(source, mode):
    result = execute(compile_scoped_dispatch(source), 'Maria', mode=mode)
    assert [g['x'] for g in result['glyphs']] == [18, 23, 28, 33, 38]
    assert result['pixels'] == expected_pixels(source, 'Maria', 18, 70, mode)
