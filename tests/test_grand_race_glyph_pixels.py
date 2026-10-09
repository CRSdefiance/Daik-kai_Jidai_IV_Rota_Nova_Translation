import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_grand_race_glyph_pixels_v136 import verify_glyph


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v136_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('mode', [16, 4])
@pytest.mark.parametrize('x', [0, 1, 2, 3])
def test_full_glyph_at_every_packed_pixel_phase_preserves_neighbors(source, mode, x):
    assert verify_glyph(source, 'W', mode, x)['glyph_and_neighbor_pixels_exact']


@pytest.mark.parametrize('mode', [16, 4])
def test_blank_space_uses_native_mode_behavior(source, mode):
    assert verify_glyph(source, ' ', mode, 3)['glyph_and_neighbor_pixels_exact']


def test_lost_visible_glyph_column_mutation_is_detected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xD1738, 0xE3550004)
    with pytest.raises(ValueError, match='pixels differ'):
        verify_glyph(changed, 'W', 16, 0)


def test_wrong_packed_nibble_step_is_detected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xD17F0, 0xB2877008)
    with pytest.raises(ValueError, match='pixels differ'):
        verify_glyph(changed, 'W', 4, 0)
