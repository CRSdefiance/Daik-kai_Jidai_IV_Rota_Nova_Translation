import struct
from pathlib import Path

import pytest
from ndspy.code import MainCodeFile

from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_raster import execute
from scripts.probe_map_tooltip_cp932_pixels import verify, verify_name


@pytest.fixture(scope='module')
def source():
    return Path('work/analysis/map_creature_complete_v139/proposed_arm9.bin').read_bytes()


@pytest.fixture(scope='module')
def font():
    return NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')


@pytest.mark.parametrize('mode', [4, 16])
@pytest.mark.parametrize('name', ['Fleet', 'A' * 18])
def test_actual_itcm_numeric_glyph_pixels_and_shadows_match_full_buffer(source, font, mode, name):
    result = verify(source, font, name, 255, 65535, mode)
    assert result['native_itcm_and_font_lookup_executed']
    assert result['independent_full_buffer_pixels_match']
    assert result['stack_registers_and_buffer_guards_preserved']


@pytest.mark.parametrize('mode', [4, 16])
def test_changed_itcm_pixel_mask_rejects(source, font, mode):
    section = next(s for s in MainCodeFile(source, 0x02000000).sections if s.ramAddress == 0x01FF8000)
    start = source.index(bytes(section.data[:256]))
    changed = bytearray(source)
    struct.pack_into('<I', changed, start + 0x5C4, 0x00400040)
    with pytest.raises(ValueError, match='full-buffer CP932 pixels'):
        verify(bytes(changed), font, 'Fleet', 0, 0, mode)


def test_changed_font_asset_rejects(source, font):
    changed = bytearray(font)
    changed[100] ^= 1
    with pytest.raises(ValueError, match='Exact clean ROM'):
        verify(source, bytes(changed), 'Fleet', 0, 0, 16)


def test_incomplete_font_asset_rejects(source, font):
    with pytest.raises(ValueError, match='complete 3340-cell'):
        execute(source, 'Fleet\n  ０', tooltip=True, kanji_font=font[:-1])


def test_original_request_only_mode_retains_explicit_painter_contract(source):
    result = execute(source, 'Fleet\n  ０', tooltip=True)
    assert result['cp932_pixel_painter_is_contract']
    assert not result['itcm_executed_addresses']


@pytest.mark.parametrize('mode', [4, 16])
@pytest.mark.parametrize('name', ['ア' * 9, 'A' + 'ア' * 8])
def test_cp932_player_name_both_parities_keep_leading_class_and_all_pixels(source, font, mode, name):
    result = verify_name(source, font, name, 'Monster Fish', mode)
    assert result['complete_ordered_glyph_sequence_and_independent_pixels_match']
    assert result['leading_class_x'] == 6
