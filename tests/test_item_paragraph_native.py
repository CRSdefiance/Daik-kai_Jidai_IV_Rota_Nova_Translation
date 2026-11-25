"""Real item resource/COMMON paths and continuation-loss regressions."""

import json
import struct
from pathlib import Path

import pytest

from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link
from scripts.probe_item_lookup_abi import verify as lookup_abi
from scripts.verify_item_interface_research import verify_page


@pytest.fixture(scope='module')
def sources():
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    return (Path('work/analysis/item_interface_research_arm9.bin').read_bytes(),
            json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8')),
            image.read_file('/GRP/KANJI.FNT'), image.read_file('/COMMON/MESFILE.DK4'))


@pytest.mark.parametrize('index', (5, 22, 151))
def test_actual_item_names_properties_and_full_COMMON_paragraphs(sources, index):
    source, plan, font, common = sources
    for page in ('main', 'standalone'):
        native = verify_page(source, plan, page, (0, 4 if page == 'main' else 1), font, 16,
                             item_index=index, common=common)
        assert native['item_actual_common_ids'] == [index + 2815]
        assert 'item_resource_provider' not in native['item_provider_contracts']
        assert 'item_advice_common_provider' not in native['item_provider_contracts']
        lines = plan['item_advice_projection'][index]['compiled'].splitlines()
        assert [row['text'] for row in native['item_draws'][-len(lines):]] == lines


def test_single_native_line_call_loses_continuation_and_is_rejected(sources):
    source, plan, font, common = sources
    broken = bytearray(source)
    struct.pack_into('<I', broken, 0x4D840, branch_link(0x0204D840, 0x020D5404))
    # The execute guard permits only the pinned paragraph helper. A source
    # regression that bypasses it fails before any false whole-text proof.
    with pytest.raises(ValueError, match='paragraph helper'):
        verify_page(bytes(broken), plan, 'main', (0, 4), font, 4, item_index=22, common=common)


def test_private_getter_invalid_indices_preserve_original_fallback_and_ABI(sources):
    source, plan, _, _ = sources
    result = lookup_abi(source, plan)
    roles = [row for row in result['cases'] if row['kind'] == 'role_lookup' and row['input'] in (-1, 16, 255)]
    assert roles and all(row['returned_pointer'] == 0 for row in roles)
    assert result['all_pointers_registers_stack_guards_pass']


@pytest.mark.parametrize('index', (0, 187, 197))
def test_real_object_metadata_initializer_static_and_promotional_boundaries(sources, index):
    source, plan, font, common = sources
    native = verify_page(source, plan, 'standalone', (0, 1), font, 16, item_index=index, common=common)
    initialization = native['item_native_object_metadata_initialization']
    assert initialization['native_metadata_initialization_and_return_pass']
    assert 0xCDAC4 in initialization['executed_offsets']
    if index >= 188:
        assert 0x102BB0 in initialization['executed_offsets']
        assert len(native['item_promotional_default_initialization']['default_promotional_items']) == 10
