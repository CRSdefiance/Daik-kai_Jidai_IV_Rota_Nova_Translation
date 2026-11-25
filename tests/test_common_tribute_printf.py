import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_tribute_printf import execute, income_contribution


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')


def test_complete_two_argument_notice(source):
    result = execute(source, 'Under %s: %s gold coins.', 884629, b'ABCDEFGHIJKLMNOPQR')
    assert result['expanded_text'] == 'Under ABCDEFGHIJKLMNOPQR: ８８４６２９ gold coins.'
    assert result['output_guards_intact']


def test_signed_converter_boundary(source):
    assert execute(source, '%s coins', 2147483647)['expanded_text'] == '２１４７４８３６４７ coins'
    with pytest.raises(ValueError, match='signed integer'):
        execute(source, '%s coins', 0xFFFFFFFF)


def test_name_extent_and_argument_order(source):
    with pytest.raises(ValueError, match='eighteen-byte'):
        execute(source, '%s %s', 1, b'A' * 19)
    with pytest.raises(ValueError, match='argument count'):
        execute(source, '%s', 1, b'A')


def test_native_income_maximum_and_divisor_mutation(source):
    assert income_contribution(source, 65535, 3) == 9829
    assert income_contribution(source, 65535, 4) == 3276
    modified = bytearray(source)
    struct.pack_into('<I', modified, 0xB2620, 0x33333333)
    with pytest.raises(ValueError, match='contribution differs'):
        income_contribution(bytes(modified), 65535, 3)


def test_income_field_extent(source):
    with pytest.raises(ValueError, match='field extents'):
        income_contribution(source, 65536, 3)
