import struct
from pathlib import Path

import pytest

from scripts.execute_grand_race_result_frame import execute


@pytest.fixture
def source():
    return bytearray(Path('work/analysis/grand_race_complete_ui_proposal_v136/proposed_arm9.bin').read_bytes())


@pytest.mark.parametrize('row', range(4))
@pytest.mark.parametrize('selected', [False, True])
@pytest.mark.parametrize('name', [b'ABCDEFGHIJKLMNOP', 'ア'.encode('cp932') * 8])
def test_native_complete_result_frame_and_text(source, row, selected, name):
    proof = execute(source, b'1st Place 1P ' + name, row, selected)
    assert proof['text_end_x'] == 212
    assert proof['x'] == 38
    assert proof['y'] == 32 + row * 28
    assert proof['renderer_flag_restored']
    assert proof['stack_and_callee_registers_preserved']


def test_wrong_native_frame_width_rejected(source):
    struct.pack_into('<I', source, 0x12ED04, 156)
    with pytest.raises(ValueError, match='centering'):
        execute(source, b'1st Place 1P ABCDEFGHIJKLMNOP', 0)


def test_native_first_character_skip_rejected(source):
    struct.pack_into('<I', source, 0xD1610, 0xE5D73001)
    with pytest.raises(ValueError, match='dropped complete text'):
        execute(source, b'1st Place 1P ABCDEFGHIJKLMNOP', 0)
