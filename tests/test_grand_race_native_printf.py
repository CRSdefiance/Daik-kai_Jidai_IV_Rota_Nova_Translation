import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_native_printf import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE


@pytest.fixture
def source():
    return bytearray(NdsImage.open(CANDIDATE).read_file('/__arm9__.bin'))


@pytest.mark.parametrize('place', ['1st Place', '2nd Place', '3rd Place', '4th Place'])
@pytest.mark.parametrize('player', ['1P', '2P', '3P', '4P'])
@pytest.mark.parametrize('name', [b'ABCDEFGHIJKLMNOP', 'ア'.encode('cp932') * 8])
def test_actual_native_complete_compound_row(source, place, player, name):
    proof = execute(source, place, player, name)
    assert bytes.fromhex(proof['full_row_hex']) == place.encode() + b' ' + player.encode() + b' ' + name + b'\0'
    assert proof['bytes_with_nul'] == 30
    assert proof['stack_balanced']
    assert proof['callee_registers_preserved']
    assert 0xD7950 in proof['executed_offsets']


def test_missing_native_nul_store_rejected(source):
    struct.pack_into('<I', source, 0xD7798, 0xE1A00000)
    with pytest.raises(ValueError, match='dropped text/NUL'):
        execute(source, '1st Place', '1P', b'Raphael')


def test_wrong_native_stack_cleanup_rejected(source):
    struct.pack_into('<I', source, 0xD774C, 0xE28DD00C)
    with pytest.raises(ValueError, match='caller stack'):
        execute(source, '1st Place', '1P', b'Raphael')
