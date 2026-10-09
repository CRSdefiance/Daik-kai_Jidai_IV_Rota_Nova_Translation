import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_append import execute
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE


@pytest.fixture
def source():
    return bytearray(NdsImage.open(CANDIDATE).read_file('/__arm9__.bin'))


@pytest.mark.parametrize('length,inserted', [(14, b'B'), (15, b'B'),
                                          (14, 'ア'.encode('cp932')), (15, 'ア'.encode('cp932'))])
def test_actual_end_append_preserves_complete_input(source, length, inserted):
    result = execute(source, b'A' * length, inserted)
    assert bytes.fromhex(result['result_hex']) == b'A' * length + inserted
    assert result['terminated_at'] == length + len(inserted)
    assert result['writes'] == list(range(length, length + len(inserted) + 1))


def test_native_name_capacity_splits_cp932(source):
    inserted = 'ア'.encode('cp932')
    result = execute(source, b'A' * 15, inserted, capacity=16)
    assert bytes.fromhex(result['result_hex']) == b'A' * 15 + inserted[:1]
    with pytest.raises(UnicodeDecodeError):
        bytes.fromhex(result['result_hex']).decode('cp932')


def test_mutated_nul_destination_cannot_pass(source):
    struct.pack_into('<I', source, 0xB094C, 0xE5C71000)  # strb r1,[r7], not destination.
    with pytest.raises(ValueError, match='Unsupported end-insertion opcode'):
        execute(source, b'A' * 15, b'B')
