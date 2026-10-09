import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_sender import execute as send
from scripts.execute_grand_race_saved_name import execute as storage
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE


@pytest.fixture
def source():
    return bytearray(NdsImage.open(CANDIDATE).read_file('/__arm9__.bin'))


@pytest.mark.parametrize('name', [b'Raphael', b'A' * 16, 'ア'.encode('cp932') * 8])
@pytest.mark.parametrize('role', ['host', 'join'])
def test_complete_saved_loaded_and_sent_field(source, name, role):
    field = (name + b'\0').ljust(17, b'\xa5')
    saved = storage(source, field, 'save')
    loaded = storage(source, bytes.fromhex(saved['output_hex']), 'load')
    sent = send(source, bytes.fromhex(loaded['output_hex']), role)
    assert sent['payload_field_hex'] == field.hex()
    assert sent['terminated_at'] == len(name)
    assert [call['field_byte'] for call in loaded['calls']] == list(range(17))


@pytest.mark.parametrize('at,mode', [(0x830D0, 'save'), (0x82FD8, 'load')])
def test_omitted_last_storage_byte_rejected(source, at, mode):
    struct.pack_into('<I', source, at, 0xE358000F)
    with pytest.raises(ValueError, match='final terminator'):
        storage(source, b'A' * 16 + b'\0', mode)


@pytest.mark.parametrize('at,role', [(0xF8EDC, 'join'), (0xF9C4C, 'host')])
def test_short_sender_loop_rejected(source, at, role):
    struct.pack_into('<I', source, at, 0xE3A03007)
    with pytest.raises(ValueError, match='field boundary'):
        send(source, b'A' * 16 + b'\0', role)
