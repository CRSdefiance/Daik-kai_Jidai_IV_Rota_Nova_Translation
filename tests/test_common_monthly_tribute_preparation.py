import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_monthly_tribute_preparation import execute


def test_native_monthly_amount_and_leading_text_survive():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    result = execute(source, "This month's tribute is %s gold coins. Please accept it.", 999999, 1)
    assert result['complete_prepared_text'] == "This month's tribute is ９９９９９９ gold coins. Please accept it."


def test_missing_native_formatter_is_detected():
    source = bytearray(NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin'))
    struct.pack_into('<I', source, 0x54150, 0xE1A00000)
    with pytest.raises(ValueError, match='Portrait preparation writes beyond buffers or stack'):
        execute(bytes(source), "This month's tribute is %s gold coins.", 999999, 1)
