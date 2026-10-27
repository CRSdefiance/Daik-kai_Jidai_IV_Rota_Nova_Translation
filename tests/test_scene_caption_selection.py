import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_scene_caption_selection import execute


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v137_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('table,count', [(0x115CAC, 46), (0x115A04, 41), (0x115968, 39), (0x115834, 38)])
def test_native_selection_first_and_last_valid_caption(source, table, count):
    for index in (0, count - 1):
        case = execute(source, table, index, count)
        assert case['stack_and_registers_preserved']
        assert case['y'] == 70 and case['style'] == 1
        assert case['full_text_hex'].endswith('00')


def test_changed_consumer_dropping_leading_bytes_is_rejected(source):
    changed = bytearray(source)
    # Replace the actual second table lookup with ADD r2,r0,#1.
    struct.pack_into('<I', changed, 0x42FF8, 0xE2802001)
    with pytest.raises(ValueError, match='different complete caption'):
        execute(changed, 0x115CAC, 0, 46)


def test_changed_centering_width_is_rejected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x42FDC, 0xE3A0C005)
    with pytest.raises(ValueError, match='centering/Y/style differs'):
        execute(changed, 0x115CAC, 0, 46)


def test_lil_array_cannot_be_scanned_into_hodram(source):
    with pytest.raises(ValueError, match='inside its native route array'):
        execute(source, 0x115968, 39, 39)
