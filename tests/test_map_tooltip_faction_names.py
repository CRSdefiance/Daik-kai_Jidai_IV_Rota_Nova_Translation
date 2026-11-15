import struct
from pathlib import Path

import pytest

from scripts.probe_map_tooltip_faction_names import ROUTE_FACTIONS, execute_name


@pytest.fixture(scope='module')
def source():
    return Path('work/analysis/map_creature_complete_v139/proposed_arm9.bin').read_bytes()


@pytest.mark.parametrize('route', range(4))
def test_current_route_uses_complete_player_name_from_native_storage(source, route):
    result = execute_name(source, ROUTE_FACTIONS[route], route, b'First Last Fleet')
    assert result['player_selected']
    assert bytes.fromhex(result['full_text_hex']) == b'First Last Fleet\0'
    assert result['stack_return_and_adjacent_owner_guards_preserved']


@pytest.mark.parametrize('index', range(20))
def test_fixed_faction_initializer_and_name_getter_preserve_full_name(source, index):
    route = next(r for r, faction in enumerate(ROUTE_FACTIONS) if faction != index)
    result = execute_name(source, index, route)
    assert not result['player_selected']
    assert result['text']
    assert result['native_constructor_and_name_getter_executed']


@pytest.mark.parametrize('index,route', [(-1, 0), (20, 0), (0, -1), (0, 4)])
def test_unmapped_native_faction_and_route_indices_reject(source, index, route):
    with pytest.raises(ValueError, match='mapped source bounds'):
        execute_name(source, index, route)


def test_wrong_name_accessor_field_rejects(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x3CFAC, 0x05940008)
    with pytest.raises(ValueError, match='name selection'):
        execute_name(bytes(changed), 19, 0)


def test_changed_route_mapping_rejects(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x115264, 1)
    with pytest.raises(ValueError, match='route-to-faction'):
        execute_name(bytes(changed), 19, 0)


def test_changed_virtual_name_method_rejects(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x137248, 0x0203CFEC)
    with pytest.raises(ValueError, match='vtable'):
        execute_name(bytes(changed), 19, 0)


def test_name_above_actual_faction_editor_limit_rejects(source):
    with pytest.raises(ValueError, match='eighteen-byte'):
        execute_name(source, 0, 0, b'A' * 19)
