"""Native duty-based COMMON consumers retain special, sentinel and table paths."""

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_connected_role_common_consumers import connected


@pytest.fixture(scope='module')
def resources():
    image = NdsImage.open('out/all_routes_combined_v159_candidate.nds')
    return image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4')


@pytest.mark.parametrize(('caller', 'route', 'attribute', 'state'), (
    (0, 0, 0, 'matching'), (1, 3, 20, 'matching'),
    (0, 2, 12, 'matching'), (1, 1, 16, 'matching'),
    (0, 3, 5, 'unassigned'), (1, 2, 5, 'null-ship'),
))
def test_actual_duty_to_native_COMMON_selection_and_complete_copy(resources, caller, route, attribute, state):
    result = connected(*resources, caller, route, attribute, state)
    assert result['actual_duty_search_ship_virtual_table_selector_COMMON_copy_and_ABI_pass']
    assert not result['remaining_245_id_overlap']
    assert (result['selected_id'] is None) == (state != 'matching')


def test_unproven_null_role_is_not_executed_as_valid_input(resources):
    with pytest.raises(ValueError, match='Null role table'):
        connected(*resources, 0, 0, 9)


def test_changed_role_virtual_is_rejected(resources):
    source, common = resources
    damaged = bytearray(source)
    damaged[0x132C4] ^= 1
    with pytest.raises(ValueError, match='ship role virtual'):
        connected(bytes(damaged), common, 0, 0, 5)
