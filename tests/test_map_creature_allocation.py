import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.compile_map_creature_allocation import NEW_TABLE, OLD_TABLE, OWNED, compile_allocation
from scripts.execute_golden_route_heading import TABLE_LITERAL, execute
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references


@pytest.fixture(scope='module')
def compiled():
    images = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds',
        'out/all_routes_combined_v139_candidate.nds')]
    proposed, report = compile_allocation(*images)
    return images[2], proposed, report


def test_unsorted_adjacent_pool_references_are_all_found():
    data = bytearray(40)
    for field, target in ((0, 0x02000012), (4, 0x02000015), (8, 0x02000025)):
        struct.pack_into('<I', data, field, target)
    ranges = [(0x20, 0x28), (0x10, 0x14), (0x14, 0x18)]
    assert byte_pointer_references(data, ranges) == {0: 0x12, 4: 0x15, 8: 0x25}


def test_overlapping_source_owners_reject():
    with pytest.raises(ValueError, match='Overlapping source owners'):
        byte_pointer_references(bytes(40), [(0x20, 0x28), (0x10, 0x14), (0x12, 0x18)])


def test_full_labels_fit_and_creature_constructors_select_complete_english(compiled):
    _, _, report = compiled
    assert report['string_bytes'] == 151
    assert report['string_capacity'] == 172
    assert len(report['selections']) == 15
    assert [row['text'] for row in report['native_classes'][34:38]] == [
        'Monster Fish', 'Giant Squid', 'Shark', 'Whale']


@pytest.mark.parametrize('selection', [0, 1])
def test_relocated_title_table_native_heading_matches_original(compiled, selection):
    current, proposed, _ = compiled
    assert struct.unpack_from('<I', proposed, TABLE_LITERAL)[0] == 0x02000000 + NEW_TABLE
    before, after = execute(current, selection), execute(proposed, selection)
    for field in ('full_text_hex', 'x', 'y', 'style'):
        assert before[field] == after[field]


def test_bad_title_table_literal_rejects(compiled):
    changed = bytearray(compiled[1])
    struct.pack_into('<I', changed, TABLE_LITERAL, 0x03000000)
    with pytest.raises(ValueError, match='table escapes'):
        execute(bytes(changed), 0)


def test_unrelated_bytes_and_shared_strings_are_retained(compiled):
    current, proposed, report = compiled
    allowed = [*OWNED, (TABLE_LITERAL, TABLE_LITERAL + 4),
               *((r['old_pointer_field'], r['old_pointer_field'] + 4) for r in report['selections'])]
    assert all(any(lo <= i < hi for lo, hi in allowed)
               for i, (a, b) in enumerate(zip(current, proposed, strict=True)) if a != b)
    for row in report['shared_full_strings']:
        raw = row['text'].encode('ascii') + b'\0'
        assert proposed[row['offset']:row['offset'] + len(raw)] == raw
    assert byte_pointer_references(proposed, [(OLD_TABLE, OLD_TABLE + 8)]) == {}
