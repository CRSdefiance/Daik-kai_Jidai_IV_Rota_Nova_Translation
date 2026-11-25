import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_name_copy import execute


@pytest.fixture(scope='module')
def arm9():
    return NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('name', [b'', b'A', b'ABCDEFGHIJKLMNOP', '一二三四五六七八'.encode('cp932')])
def test_actual_name_copier_retains_complete_input_and_nul(arm9, name):
    result = execute(arm9, name)
    stored = bytes.fromhex(result['stored_hex'])
    assert stored[:len(name) + 1] == name + b'\0'
    assert stored[len(name) + 1:] == b'\xa5' * (16 - len(name))
    assert result['leading_byte_intact']


def test_missing_terminator_store_is_detected(arm9):
    changed = bytearray(arm9)
    struct.pack_into('<I', changed, 0xCEDC0, 0xE12FFF1E)
    with pytest.raises(ValueError, match='changed name bytes'):
        execute(changed, b'ABCDEFGHIJKLMNOP')


def test_removed_first_byte_store_is_detected(arm9):
    changed = bytearray(arm9)
    struct.pack_into('<I', changed, 0xCEDAC, 0xE3A01000)
    with pytest.raises(ValueError):
        execute(changed, b'First')


def test_model_does_not_certify_an_overlength_input(arm9):
    with pytest.raises(ValueError, match='at most 16 bytes'):
        execute(arm9, b'A' * 17)
