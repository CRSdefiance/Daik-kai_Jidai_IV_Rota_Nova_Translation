"""Conditional Advice commands must survive actual descriptor and footer draws."""

import struct
from pathlib import Path

import pytest
from ndspy.code import MainCodeFile

from scripts.verify_item_advice_menus import CONFIGURATIONS, verify


@pytest.mark.parametrize('configuration', CONFIGURATIONS)
def test_actual_item_advice_menu_both_formats(configuration):
    source = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    for mode in (4, 16):
        result = verify(source, configuration, mode)
        labels = [row['text'] for row in result['footer_draws']]
        assert ('Advice' in labels) == configuration[1]
        assert result['item_menu_descriptor']['native_option_bit_query_executes']


def test_missing_first_advice_character_rejected_by_complete_footer_oracle():
    source = Path('work/analysis/item_interface_cache_research_arm9.bin').read_bytes()
    code = MainCodeFile(source, 0x02000000)
    pointer = struct.unpack_from('<I', source, 0x45664)[0]
    field = pointer - 0x02387A20
    assert bytes(code.sections[3].data[field:field + 6]) == b'Advice'
    code.sections[3].data[field:field + 6] = b' dvice'
    with pytest.raises(ValueError, match='loses a complete label'):
        verify(bytes(code.save()), ('gallery', True, True), 16)
