"""Regression guards for whole item labels and actual same-row overlap."""

import copy
import json
import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.verify_item_interface_research import verify_page


@pytest.fixture(scope='module')
def sources():
    return (Path('work/analysis/item_interface_research_arm9.bin').read_bytes(),
            json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8')),
            NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT'))


def test_actual_counter_extremes_preserve_both_numbers_and_whole_heading(sources):
    source, plan, font = sources
    for count in (0, 99, 100, 198):
        native = verify_page(source, plan, 'counter', count, font, 16)
        assert native['item_draws'][0]['text'] == f'Items Acquired {count:3d}/198'


def test_actual_crew_ship_price_and_advice_branches_remain_readable(sources):
    source, plan, font = sources
    for kind in (2, 3, 4):
        native = verify_page(source, plan, 'main', (255, kind), font, 4)
        assert native['stack_and_registers_preserved']
    for flag in (0, 1):
        verify_page(source, plan, 'standalone', (255, flag), font, 16)


def test_original_owner_column_overlaps_complete_heading_and_is_rejected(sources):
    source, plan, font = sources
    broken = bytearray(source)
    struct.pack_into('<I', broken, 0x4D800, 0xE3A02030)
    expected = copy.deepcopy(plan)
    expected['owner_name_x'] = 48
    with pytest.raises(ValueError, match='cells overlap'):
        verify_page(bytes(broken), expected, 'main', (255, 3), font, 16)


def test_original_effect_column_overlaps_complete_heading_and_is_rejected(sources):
    source, plan, font = sources
    broken = bytearray(source)
    struct.pack_into('<I', broken, 0x4D6D4, 0xE3A030CE)
    expected = copy.deepcopy(plan)
    expected['effect_numeric_x'] = 206
    with pytest.raises(ValueError, match='cells overlap'):
        verify_page(bytes(broken), expected, 'main', (255, 2), font, 16)


def test_complete_long_category_and_boarding_role_use_native_private_getters(sources):
    source, plan, font = sources
    for page in ('main', 'standalone'):
        native = verify_page(source, plan, page, (255, 3 if page == 'main' else 1, 1, 7), font, 4)
        assert any(row['text'] == 'Navigation Gear ' for row in native['item_draws'])
        assert any(row['text'] == 'Boarding Leader ' for row in native['item_draws'])
        assert native['item_pool_executed_addresses']
        assert 'item_description_provider' not in native['item_provider_contracts']


def test_old_role_column_overlaps_real_proof_map_and_is_rejected(sources):
    source, plan, font = sources
    broken = bytearray(source)
    struct.pack_into('<I', broken, 0x4D698, 0xE3A02034)
    expected = copy.deepcopy(plan)
    expected['role_x'] = 52
    with pytest.raises(ValueError, match='cells overlap'):
        verify_page(bytes(broken), expected, 'main', (255, 3, 1, 7), font, 16)


def test_shifted_effect_pointer_loses_initial_letter_and_is_rejected(sources):
    source, plan, font = sources
    broken = bytearray(source)
    pointer = struct.unpack_from('<I', broken, 0x4D864)[0]
    struct.pack_into('<I', broken, 0x4D864, pointer + 1)
    with pytest.raises(ValueError, match='complete prose'):
        verify_page(bytes(broken), plan, 'main', (255, 2), font, 4)
