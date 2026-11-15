"""Gallery counter geometry must come from its actual selected image header."""

import struct
from pathlib import Path

import pytest

from scripts.probe_item_counter_canvas import verify


def test_native_counter_source_view_and_clear_are_bounded():
    result = verify(Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes())
    assert result['header_pointer'] == 0x022BD7D8
    assert result['actual_view_geometry'] == [144, 36]
    assert result['native_backing_geometry'] == [256, 92]
    assert result['clear_only_view_preserves_adjacent_rows_columns_and_guards']


def test_neighboring_text_image_cannot_be_mistaken_for_counter_allocation():
    source = bytearray(Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes())
    instruction = struct.unpack_from('<I', source, 0x44F50)[0]
    field = 0x44F50 + 8 + (instruction & 0xFFF)
    struct.pack_into('<I', source, field, 0x022BD7EC)
    with pytest.raises(ValueError, match='Actual Gallery counter image header differs'):
        verify(bytes(source))
