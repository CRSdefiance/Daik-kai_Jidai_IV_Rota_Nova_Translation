import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.plan_grand_race_ui_allocation_v136 import CANDIDATE
from scripts.probe_grand_race_name_sources_v136 import inspect_names


@pytest.fixture
def source():
    return bytearray(NdsImage.open(CANDIDATE).read_file('/__arm9__.bin'))


def test_complete_current_names(source):
    rows = inspect_names(source)
    assert [row['bytes_before_nul'] for row in rows] == [7, 6, 3, 5]
    for row in rows:
        assert bytes.fromhex(row['native_copy']['stored_hex']).startswith(
            row['name'].encode('ascii') + b'\0')


def test_unterminated_name_rejected(source):
    pointer = struct.unpack_from('<I', source, 0x120B80)[0] - 0x02000000
    source[pointer:pointer + 17] = b'Raphael' + b'x' * 10
    with pytest.raises(ValueError, match='complete translated source name'):
        inspect_names(source)


def test_missing_leading_character_rejected(source):
    pointer = struct.unpack_from('<I', source, 0x120B80)[0]
    struct.pack_into('<I', source, 0x120B80, pointer + 1)
    with pytest.raises(ValueError, match='complete translated source name'):
        inspect_names(source)


def test_out_of_range_pointer_rejected(source):
    struct.pack_into('<I', source, 0x120B80, 0xFFFFFFFF)
    with pytest.raises(ValueError, match='outside ARM9'):
        inspect_names(source)
