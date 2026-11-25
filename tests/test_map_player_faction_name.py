import struct
from pathlib import Path

import pytest

from scripts.execute_grand_race_name_append import execute as append
from scripts.probe_map_player_faction_name import (
    default_name,
    edit_dispatch,
    native_copy,
    serialize,
)


@pytest.fixture(scope='module')
def source():
    return Path('work/analysis/map_creature_complete_v139/proposed_arm9.bin').read_bytes()


@pytest.mark.parametrize('route,expected', [(0, 'Castor Co.'), (1, 'Bergstrom Fleet'),
                                          (2, 'Argot Co.'), (3, 'Li Clan')])
def test_actual_default_faction_name_producer(source, route, expected):
    assert default_name(source, route)['text'] == expected


@pytest.mark.parametrize('name', [b'A', b'A' * 17, b'A' * 18, 'ア'.encode('cp932') * 9])
def test_editor_native_setter_and_nineteen_byte_save_load_keep_complete_name(source, name):
    assert edit_dispatch(source, name)['limit'] == 18
    field = native_copy(source, name)
    assert field[:len(name) + 1] == name + b'\0'
    assert len(field) == 19
    assert bytes.fromhex(serialize(source, field)['complete_field_hex']) == field
    assert bytes.fromhex(serialize(source, field, restore=True)['complete_field_hex']) == field


@pytest.mark.parametrize('name', [b'', b'A' * 19, b'A\0B'])
def test_names_outside_actual_editor_bound_reject(source, name):
    with pytest.raises(ValueError, match='eighteen-byte'):
        native_copy(source, name)


def test_changed_editor_capacity_rejects(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0x9DF74, 0xE3A01010)
    with pytest.raises(ValueError, match='keyboard limit'):
        edit_dispatch(bytes(changed), b'A' * 18)


@pytest.mark.parametrize('restore,offset', [(False, 0x83070), (True, 0x83168)])
def test_shortened_serialization_extent_rejects(source, restore, offset):
    changed = bytearray(source)
    struct.pack_into('<I', changed, offset, 0xE3580011)
    with pytest.raises(ValueError, match='nineteen-byte extent'):
        serialize(bytes(changed), b'A' * 18 + b'\0', restore=restore)


@pytest.mark.parametrize('size', [16, 17, 18])
@pytest.mark.parametrize('inserted', [b'B', 'ア'.encode('cp932')])
def test_inherited_atomic_append_at_actual_faction_capacity(source, size, inserted):
    result = append(source, b'A' * size, inserted, 18, full_return=True)
    expected = b'A' * size + inserted if size + len(inserted) <= 18 else b'A' * size
    assert bytes.fromhex(result['result_hex']) == expected


def test_unterminated_saved_field_is_preserved_without_inventing_validation(source):
    result = serialize(source, b'A' * 19, restore=True)
    assert bytes.fromhex(result['complete_field_hex']) == b'A' * 19
    assert result['physical_io_backend_is_contract']
