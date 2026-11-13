import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.inventory_map_tooltip_classes import execute_class, inventory


@pytest.fixture(scope='module')
def images():
    return (NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'),
            NdsImage.open('out/all_routes_combined_v139_candidate.nds').read_file('/__arm9__.bin'))


def test_all_native_class_initializers_and_full_creature_meanings(images):
    report, records = inventory(*images)
    assert [r['index'] for r in report['cases']] == list(range(39))
    assert [(r['class_index'], r['japanese'], r['english']) for r in records] == [
        (34, '化魚', 'Monster Fish'), (35, '大イカ', 'Giant Squid'),
        (36, 'サメ', 'Shark'), (37, '鯨', 'Whale')]
    assert report['creature_storage']['owned_bytes'] == 28
    assert report['creature_storage']['complete_english_bytes'] == 37
    assert all(r['review']['formatting'] is False for r in records)


@pytest.mark.parametrize('index', [-1, 39])
def test_class_count_boundary_rejects(images, index):
    with pytest.raises(ValueError, match='source-bounded'):
        execute_class(images[1], index)


def test_native_initializer_cannot_write_adjacent_owner(images):
    changed = bytearray(images[1])
    # Change the name-pointer store from owner+8 to owner+64. Real native
    # execution must detect the write into the next owner before approving it.
    struct.pack_into('<I', changed, 0xCD3E8, 0xE5841040)
    with pytest.raises(ValueError, match='outside owner'):
        execute_class(bytes(changed), 34)


def test_changed_native_name_vtable_rejects(images):
    changed = bytearray(images[1])
    struct.pack_into('<I', changed, 0x15EE24, 0x0201FD78)
    with pytest.raises(ValueError, match='vtable'):
        execute_class(bytes(changed), 34)
