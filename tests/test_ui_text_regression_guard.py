"""The UI verifier must distinguish owned cache data from actual corruption."""
import struct

import pytest

from scripts.review_ui_text_smoke import verify_runtime_helpers


def fixture():
    section = bytearray(4096)
    struct.pack_into('<I', section, 0x194, 0x01FFC680)
    ram, observed = bytearray(0x400000), bytearray(section)
    struct.pack_into('<I', observed, 0x2D8, 0x023A9880)
    struct.pack_into('<I', observed, 0x680, 0x023A9FA0)
    struct.pack_into('<5I', ram, 0x3A9FA0, 4, 46, 36,
                     (0x02125A20 - 0x023A9FA0) & 0xFFFFFFFF, 32)
    return section, observed, ram


def test_both_declared_cache_allocations_have_valid_headers_and_bounds():
    section, observed, ram = fixture()
    result = verify_runtime_helpers(section, observed, ram)
    assert result['immutable_helper_bytes_verified'] == 4088
    assert result['market_cache_header_validated']


@pytest.mark.parametrize('address', [0x21C, 0x260, 0x300, 0x67C, 0x684, 0xFFF])
def test_clipping_code_and_neighbours_of_cache_slots_cannot_change(address):
    section, observed, ram = fixture()
    observed[address] ^= 1
    with pytest.raises(AssertionError):
        verify_runtime_helpers(section, observed, ram)


@pytest.mark.parametrize('field,value', [(0, 0), (4, 45), (8, 37), (12, 0), (16, 20)])
def test_initialized_market_cache_cannot_hide_a_corrupt_surface(field, value):
    section, observed, ram = fixture()
    struct.pack_into('<I', ram, 0x3A9FA0 + field, value)
    with pytest.raises(AssertionError):
        verify_runtime_helpers(section, observed, ram)


@pytest.mark.parametrize('slot,value', [(0x2D8, 0x023FFFF0), (0x680, 0x023FF800), (0x680, 1)])
def test_cache_allocations_cannot_extend_outside_ram(slot, value):
    section, observed, ram = fixture()
    struct.pack_into('<I', observed, slot, value)
    with pytest.raises(AssertionError):
        verify_runtime_helpers(section, observed, ram)
