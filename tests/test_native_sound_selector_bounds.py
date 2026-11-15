import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_native_sound_selector_bounds import update


@pytest.mark.parametrize('index,delta,expected', [(2, -1, 39), (39, 1, 2), (20, 1, 21)])
def test_native_bgm_selector_wraps(index, delta, expected):
    source = NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin')
    assert update(source, index, delta)['result'] == expected


def test_changed_wrap_can_select_promotional_text():
    source = bytearray(NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin'))
    struct.pack_into('<I', source, 0x108FCC, 0xC3A00028)
    with pytest.raises(ValueError, match='escapes native range'):
        update(bytes(source), 39, 1)
