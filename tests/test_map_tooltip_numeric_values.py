import struct
from pathlib import Path

import pytest

from scripts.probe_map_tooltip_numeric_values import execute_pair, verify_mixed


@pytest.fixture(scope='module')
def source():
    return Path('work/analysis/map_creature_complete_v139/proposed_arm9.bin').read_bytes()


@pytest.mark.parametrize('entry', [0, 1, 2, None])
def test_native_percentage_selection_and_unsigned_armament_maximum(source, entry):
    result = execute_pair(source, 255, 65535, entry=entry)
    assert result['percentage'] == (0 if entry is None else 255)
    assert bytes.fromhex(result['armament_hex']).decode('cp932') == '６５５３５'


@pytest.mark.parametrize('ring_index', [0, 31])
def test_ring_wrap_retains_both_complete_numeric_strings(source, ring_index):
    result = execute_pair(source, 0, 0, ring_index=ring_index)
    assert result['percent_pointer'] != result['armament_pointer']
    assert result['complete_digits_nul_stack_and_distinct_ring_slots_preserved']


@pytest.mark.parametrize('name', ['Fleet', 'FleetX'])
@pytest.mark.parametrize('mode', [4, 16])
def test_mixed_native_digits_keep_armament_leading_character_and_all_numeric_requests(source, name, mode):
    result = verify_mixed(source, name, 255, 65535, mode)
    assert result['width'] == 126
    assert result['cp932_pixel_painter_is_contract']


@pytest.mark.parametrize('percentage,armament', [(256, 0), (-1, 0), (0, 65536), (0, -1)])
def test_values_outside_native_load_bounds_reject(source, percentage, armament):
    with pytest.raises(ValueError, match='source byte/halfword'):
        execute_pair(source, percentage, armament)


def test_changed_digit_conversion_loses_exact_value_and_rejects(source):
    changed = bytearray(source)
    # Change the CP932 digit's trail-byte base from 0x4F to 0x50.
    struct.pack_into('<I', changed, 0xABF9C, 0xE2851050)
    with pytest.raises(ValueError, match='full-width digits'):
        execute_pair(bytes(changed), 0, 0)
