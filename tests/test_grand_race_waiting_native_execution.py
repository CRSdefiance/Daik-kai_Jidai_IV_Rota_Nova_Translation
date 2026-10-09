import struct

import pytest

from dk4tool.patch.grand_race_waiting_widget import rewrite_function
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_waiting_widgets import execute


@pytest.fixture
def proposed():
    # Execute real native constructor/setter/list code from the clean ROM.
    arm9 = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    return rewrite_function(arm9)[0]


def test_actual_native_loop_constructs_three_complete_linked_widgets(proposed):
    pointers = (0x02200000, 0x02200100, 0x02200200)
    report = execute(proposed, pointers)
    assert [widget['text_pointer'] for widget in report['widgets']] == list(pointers)
    assert [widget['y'] for widget in report['widgets']] == [64, 80, 96]
    assert len(report['native_calls']) == 9
    assert report['stack_balanced'] and report['following_objects_untouched']


@pytest.mark.parametrize(('offset', 'instruction'), [
    (0xF85CC, 0xE3590002),  # Original count silently drops the third English line.
    (0xF8514, 0xE1A00000),  # Missing derived vtable breaks virtual text selection.
    (0xFB030, 0xE28DD008),  # Unbalanced constructor return corrupts the caller.
])
def test_native_execution_rejects_dropped_widget_missing_vtable_and_stack_corruption(proposed, offset, instruction):
    damaged = bytearray(proposed)
    struct.pack_into('<I', damaged, offset, instruction)
    with pytest.raises(ValueError):
        execute(damaged, (0x02200000, 0x02200100, 0x02200200))
