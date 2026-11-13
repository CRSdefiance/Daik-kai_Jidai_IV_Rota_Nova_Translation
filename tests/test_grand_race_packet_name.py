import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_packet_name import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE


@pytest.fixture
def source():
    return bytearray(NdsImage.open(CANDIDATE).read_file('/__arm9__.bin'))


@pytest.mark.parametrize('player', range(4))
@pytest.mark.parametrize('name', [b'Raphael', b'A' * 16, 'ア'.encode('cp932') * 8])
def test_exact_full_name_and_last_terminator(source, player, name):
    field = (name + b'\0').ljust(17, b'\xa5')
    proof = execute(source, field, player)
    assert proof['saved_field_hex'] == field.hex()
    assert proof['terminated_at'] == len(name)
    assert proof['name_slot_offset'] == 0xD0 + player * 17


def test_transfer_does_not_synthesize_missing_nul(source):
    proof = execute(source, b'A' * 17, 0)
    assert proof['terminated_at'] == -1


def test_changed_slot_stride_cannot_pass(source):
    struct.pack_into('<I', source, 0xFA5BC, 0xE3A03012)
    with pytest.raises(ValueError, match='adjacent slot'):
        execute(source, b'A' * 16 + b'\0', 3)


def test_changed_loop_length_cannot_pass(source):
    struct.pack_into('<I', source, 0xFA5DC, 0xE3A0E009)
    with pytest.raises(ValueError, match='field length'):
        execute(source, b'A' * 16 + b'\0', 0)
