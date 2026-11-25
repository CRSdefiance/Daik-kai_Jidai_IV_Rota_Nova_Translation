import struct
from pathlib import Path

import pytest

from scripts.execute_golden_route_empty_copy import execute as copy
from scripts.execute_scene_caption_raster import execute
from scripts.probe_scene_caption_raster import expected_pixels


@pytest.fixture(scope='module')
def source():
    return Path('work/analysis/golden_route_viewer_complete_v138/proposed_arm9.bin').read_bytes()


@pytest.mark.parametrize('table,texts', [(0x12EC10, ['Back']),
                                      (0x12EC28, ['Back', 'Next', 'Previous']),
                                      (0x12EC3C, ['Back', 'Switch'])])
@pytest.mark.parametrize('mode', [4, 16])
def test_complete_native_footer_states_and_transfer(source, table, texts, mode):
    result = execute(source, 'unused', footer_table=table, mode=mode)
    assert [draw['text'] for draw in result['footer_draws']] == texts
    assert result['footer_labels'] == list(struct.unpack_from('<6I', source, table))
    text = ''.join(texts)
    assert result['pixels'] == expected_pixels(source, text, 0, 0, mode, advance=6)
    assert [glyph['code'] for glyph in result['glyphs']] == list(text.encode('ascii'))
    if table == 0x12EC28:
        assert result['footer_metadata'][:6] == [99, 48, 48, 169, 24, 24]


@pytest.mark.parametrize('count', [1, 2, 255])
def test_nonzero_record_count_skips_empty_dialog(source, count):
    result = copy(source, count=count)
    assert result['empty_dialog_selected'] is False
    assert 0x5473C not in result['executed_offsets']


def test_zero_record_native_printf_and_macro_copy_keep_full_english(source):
    result = copy(source)
    assert bytes.fromhex(result['complete_text_hex']) == b'No Golden Route records.\0'
    assert result['native_printf_macro_expansion']


def test_native_macro_parser_cannot_silently_drop_a_new_leading_character(source):
    changed = bytearray(source)
    offset = struct.unpack_from('<I', source, 0xF14D8)[0] - 0x02000000
    changed[offset] = ord('F')
    with pytest.raises(ValueError, match='drops or changes'):
        copy(changed)


@pytest.mark.parametrize('mode', [4, 16])
def test_complete_native_modal_renderer_and_style(source, mode):
    text = 'No Golden Route records.'
    result = execute(source, text, modal=True, mode=mode)
    assert [glyph['code'] for glyph in result['glyphs']] == list(text.encode('ascii'))
    assert all(glyph['style'] == 15 for glyph in result['glyphs'])
    assert result['pixels'] == expected_pixels(source, text, 0, 0, mode, advance=6, style=15)
    assert result['final_x'] == 144


def test_source_modal_dimension_change_is_rejected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x118AE8, 128)
    with pytest.raises(ValueError, match='dimensions differ'):
        execute(changed, 'No Golden Route records.', modal=True)
