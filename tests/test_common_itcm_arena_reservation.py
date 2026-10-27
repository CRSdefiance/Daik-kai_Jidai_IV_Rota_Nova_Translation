import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import ARENA_LO_LITERAL
from scripts.probe_common_itcm_arena_reservation import initialize, verify
from scripts.probe_common_scoped_word_wrap_hook import prepare


def test_scoped_extension_reserved_by_native_getters():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    saved, _ = prepare(source)
    assert verify(saved, 0x01FF9D60)['padding_bytes'] == 28


def test_old_arena_boundary_cannot_cover_extended_code():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    saved, _ = prepare(source)
    broken = bytearray(saved)
    struct.pack_into('<I', broken, ARENA_LO_LITERAL, 0x01FF9B20)
    with pytest.raises(ValueError, match='reserve the complete aligned resident extent'):
        verify(bytes(broken), 0x01FF9B20)


def test_native_initialization_changes_only_itcm_lower_bound():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    saved, _ = prepare(source)
    old, new = initialize(source), initialize(saved)
    assert new['low'][3] == 0x01FF9D60
    assert new['high'] == old['high']
    assert new['low'][:3] + new['low'][4:] == old['low'][:3] + old['low'][4:]
    assert new['repeat_preserves_bounds']
