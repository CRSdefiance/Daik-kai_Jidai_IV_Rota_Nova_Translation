import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_fleet_name_display_callers import execute


@pytest.fixture(scope='module')
def source():
    return Path('work/analysis/fleet_name_relocated_arm9.bin').read_bytes()


@pytest.fixture(scope='module')
def font():
    return NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')


@pytest.mark.parametrize('caller', ['fixed', 'centered'])
@pytest.mark.parametrize('name', [None, 'Indigo海'])
def test_connected_native_fleet_glyphs_and_independent_pixels(source, font, caller, name):
    result, _ = execute(source, caller, name, raster=True, kanji_font=font)
    assert result['full_glyph_order_bounds_and_independent_pixels_verified']
    assert (result['bitmap_width'], result['bitmap_height']) == (192, 72)


def test_altered_native_bitmap_width_rejects(source, font):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x876C8, 0xE3A000BF)
    with pytest.raises(ValueError, match='bitmap geometry'):
        execute(bytes(changed), 'fixed', None, raster=True, kanji_font=font)


def test_altered_native_cp932_shadow_rejects_independent_pixels(source, font):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xD1984, 0xE3A0000E)
    with pytest.raises(ValueError, match='independent font decode'):
        execute(bytes(changed), 'fixed', '海', raster=True, kanji_font=font)
