import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.compile_scene_caption_single_dispatch import compile_scoped_dispatch
from scripts.execute_scene_caption_raster import execute
from scripts.probe_scene_caption_raster import expected_pixels
from scripts.probe_scene_caption_wrappers import validate_callers


@pytest.fixture(scope='module')
def proposed():
    source = Path('work/analysis/scene_caption_complete_tracking_v137/proposed_arm9.bin').read_bytes()
    return compile_scoped_dispatch(source)


def test_all_twelve_argument_owners(proposed):
    rows = validate_callers(proposed)
    assert len(rows) == 12
    assert [(row['call'], row['mode']) for row in rows if row['mode'] != 1] == [(0x43008, 0)]


@pytest.mark.parametrize('offset,word', [(0x42CD8, 0xE3A06002),
                                       (0x42CD4, 0xE3A06002),
                                       (0x4419C, 0xE58D1000),
                                       (0x44748, 0xE3A01000)])
def test_mode_definition_and_store_mutations_rejected(proposed, offset, word):
    changed = bytearray(proposed)
    struct.pack_into('<I', changed, offset, word)
    with pytest.raises(ValueError):
        validate_callers(changed)


def test_unknown_direct_and_literal_callers_rejected(proposed):
    for word in (0xEB000000 | ((0x456A0 - 0x100 - 8) // 4), 0x020456A0):
        changed = bytearray(proposed)
        struct.pack_into('<I', changed, 0x100, word)
        with pytest.raises(ValueError):
            validate_callers(changed)


@pytest.mark.parametrize('mode', [4, 16])
def test_full_wrapper_preserves_complete_caption_and_cleanup(proposed, mode):
    result = execute(proposed, 'Maria', wrapper=True, caller_mode=0, mode=mode)
    assert [row['code'] for row in result['glyphs']] == list(b'Maria')
    assert result['pixels'] == expected_pixels(proposed, 'Maria', 18, 70, mode)
    assert result['actual_tracking'] == 0xFFFFFFFF
    assert result['clear_calls'] == []
    assert 0xD5A58 in result['executed_offsets']


@pytest.mark.parametrize('clear', [0, 1])
@pytest.mark.parametrize('text', ['Ironclad', 'A港町B'])
def test_original_wrapper_behavior_against_combined_rom(proposed, clear, text):
    original = NdsImage.open('out/all_routes_combined_v137_candidate.nds').read_file('/__arm9__.bin')
    before = execute(original, text, wrapper=True, clear=clear)
    after = execute(proposed, text, wrapper=True, clear=clear)
    for field in ('glyphs', 'cp932_glyphs', 'pixels', 'final_x', 'clear_calls'):
        assert before[field] == after[field]
