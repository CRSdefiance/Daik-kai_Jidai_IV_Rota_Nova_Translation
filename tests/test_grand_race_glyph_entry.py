import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_grand_race_glyph_entry_v136 import verify_entry


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v136_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('mode', [16, 4])
@pytest.mark.parametrize('x', [0, 1, 2, 3])
def test_native_entry_selects_full_glyph_and_nonzero_row(source, mode, x):
    assert verify_entry(source, 'W', mode, x)['glyph_source_and_all_pixels_verified']


@pytest.mark.parametrize('mode', [16, 4])
def test_actual_blank_glyph_zero_stores_and_stack_balance(source, mode):
    proof = verify_entry(source, ' ', mode, 3)
    assert proof['stack_balanced']
    assert not proof['copy_calls']


def test_wrong_ascii_font_index_is_detected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xD183C, 0xE2403022)
    with pytest.raises(ValueError, match='pixels differ|wrong complete glyph'):
        verify_entry(changed, 'W', 16, 0)


def test_wrong_packed_address_shift_is_detected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xD1774, 0xE1A021C5)
    with pytest.raises(ValueError, match='pixels differ'):
        verify_entry(changed, 'W', 4, 7)
