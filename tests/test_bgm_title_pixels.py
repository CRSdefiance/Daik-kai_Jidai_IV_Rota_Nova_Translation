import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_bgm_title_pixels import center, verify


@pytest.mark.parametrize('mode', [4, 16])
def test_longest_bgm_title_keeps_every_character_inside_panel(mode):
    rom = NdsImage.open('out/all_routes_combined_v143_candidate.nds')
    result = verify(rom.read_file('/__arm9__.bin'), rom.read_file('/GRP/KANJI.FNT'),
                    'Southeast Asian Village', mode)
    assert len(result['glyph_events']) == 23
    assert result['glyph_events'][0]['x'] == 7
    assert result['glyph_events'][-1]['x'] + 6 == 123


def test_wrong_native_tracking_is_detected():
    source = bytearray(NdsImage.open('out/all_routes_combined_v143_candidate.nds').read_file('/__arm9__.bin'))
    struct.pack_into('<I', source, 0x109280, 0xE3A02000)
    with pytest.raises(ValueError, match='centering differs'):
        center(bytes(source), 'Southeast Asian Village')
