import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_player_index import execute_guard, prove_guard


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v136_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('index', [-(1 << 31), -1, 0, 1, 2, 3, 4, (1 << 31) - 1])
def test_actual_signed_guard_preserves_four_entry_bounds(source, index):
    assert execute_guard(source, index)['passes_guard'] == (0 <= index < 4)


def test_off_by_one_guard_mutation_is_rejected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xF8CC4, 0xE3500005)
    with pytest.raises(ValueError, match='invalid four-entry'):
        prove_guard(changed)


def test_removed_lower_bound_branch_is_rejected(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xF8CC0, 0xE1A00000)
    with pytest.raises(ValueError, match='opcode'):
        prove_guard(changed)
