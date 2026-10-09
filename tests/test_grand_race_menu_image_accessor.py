import struct

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_menu_image_accessor import OWNER, execute, execute_raster_dispatch


@pytest.fixture
def arm9():
    return NdsImage.open('out/all_routes_combined_v134_candidate.nds').read_file('/__arm9__.bin')


@pytest.mark.parametrize(('state', 'normal', 'selected', 'expected'), [
    (0, 0, 0, OWNER + 0x10),
    (0, OWNER + 0x2000, OWNER + 0x3000, OWNER + 0x2000),
    (2, OWNER + 0x2000, OWNER + 0x3000, OWNER + 0x3000),
    (2, OWNER + 0x2000, 0, OWNER + 0x2000),
])
def test_actual_native_accessor_resolves_owner_and_state(arm9, state, normal, selected, expected):
    result = execute(arm9, state=state, normal=normal, selected=selected)
    assert result['returned_image_pointer'] == expected


def test_wrong_inheritance_adjustment_does_not_silently_read_other_data(arm9):
    damaged = bytearray(arm9)
    # The derived subobject must adjust exactly -0xAC before reading button state.
    struct.pack_into('<I', damaged, 0x140AB0, 0xFFFFFF50)
    with pytest.raises(ValueError, match='outside initialized'):
        execute(damaged)


def test_native_raster_handoff_uses_owner_and_copied_label_buffer(arm9):
    result = execute_raster_dispatch(arm9)
    assert result['callback'] == 0x020ACB10
    assert result['this_pointer'] == OWNER
    assert result['text_buffer_pointer'] == OWNER + 0x68


def test_wrong_owner_vtable_callback_is_rejected(arm9):
    damaged = bytearray(arm9)
    struct.pack_into('<I', damaged, 0x140A30, 0x020D1604)
    with pytest.raises(ValueError, match='wrong callback'):
        execute_raster_dispatch(damaged)
