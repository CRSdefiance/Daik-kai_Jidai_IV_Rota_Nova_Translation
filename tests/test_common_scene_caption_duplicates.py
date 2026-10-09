from collections import Counter

import pytest

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.inventory_common_scene_caption_duplicates import captions, inventory


@pytest.fixture(scope='module')
def inputs():
    clean = NdsImage.open('work/clean.nds')
    source = clean.read_file('/__arm9__.bin')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), source)
    current = NdsImage.open('out/all_routes_combined_v137_candidate.nds').read_file('/__arm9__.bin')
    return source, current, entries


def test_adjacent_lil_and_hodram_arrays_have_separate_owners(inputs):
    rows = captions(inputs[0])
    assert Counter(row['route_index'] for row in rows) == {0: 46, 1: 41, 2: 39, 3: 38}
    assert len({row['pointer_field'] for row in rows}) == 164
    lil = [row for row in rows if row['route_index'] == 2]
    assert lil[-1]['pointer_field'] == 0x115A00
    assert lil[-1]['index'] == 38


def test_common_duplicates_do_not_become_common_consumer_proof(inputs):
    rows, selections = inventory(*inputs)
    assert len(selections) == 245
    assert all(row['common_consumer_verified'] is False for row in selections)
    assert sum(bool(row['exact_inline_offsets']) for row in selections) == 126
    assert sum(bool(row['mapped_caption_fields']) for row in selections) == 123
    assert all(not row['mapped_caption_fields'] for row in selections if row['message_id'] < 3320)
    assert sum(row['changed_from_clean'] for row in rows) == 1


def test_port_town_keeps_its_actual_interior_pointer_and_leading_character(inputs):
    rows, selections = inventory(*inputs)
    port = next(row for row in selections if row['message_id'] == 3393)
    assert port['exact_inline_offsets'] == [0x13898C]
    assert port['mapped_caption_fields'] == [0x115CAC]
    caption = next(row for row in rows if row['pointer_field'] == 0x115CAC)
    assert caption['current_text'] == '港町１'
    assert caption['current_offset'] == 0x13898C
