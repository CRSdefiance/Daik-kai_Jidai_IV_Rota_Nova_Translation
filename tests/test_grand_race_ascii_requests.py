import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_ascii_requests import execute


@pytest.fixture(scope='module')
def source():
    return NdsImage.open('out/all_routes_combined_v136_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize('text', ['Southeast Asia', 'You are Player 4.', "The race is full. You can't join.", 'A'])
def test_actual_renderer_requests_every_first_and_last_character(source, text):
    proof = execute(source, text, 16, 64)
    assert ''.join(row['character'] for row in proof['requests']) == text
    assert proof['requests'][0]['x'] == 16
    assert proof['requests'][-1]['x'] == 16 + 6 * (len(text) - 1)


def test_first_byte_skip_mutation_rejects(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xD1610, 0xE5D73001)
    with pytest.raises(ValueError, match='lose text'):
        execute(changed, 'Natural English', 16, 64)


def test_wrong_ascii_advance_mutation_rejects(source):
    changed = bytearray(source)
    struct.pack_into('<I', changed, 0xD169C, 0xE285500C)
    with pytest.raises(ValueError, match='positions/style'):
        execute(changed, 'Natural English', 16, 64)


def test_style_and_native_call_stack_are_preserved(source):
    proof = execute(source, 'Race Results', 48, 144, 1)
    assert proof['stack_balanced']
    assert all(row['style'] == 1 and row['y'] == 144 for row in proof['requests'])
