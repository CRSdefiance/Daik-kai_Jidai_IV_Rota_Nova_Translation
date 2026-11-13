"""Expanded pool startup must return fully, never credit an instruction cutoff."""

import json
import struct
from pathlib import Path

import pytest
from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_SP

from dk4tool.patch.main_pool_cache_visibility import BASE, cache_plan, transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_persistent_name_arm7_boot_overlap import execute
from scripts.verify_ordinary_name_fidelity_research import initialized


def test_expanded_item_pool_complete_native_copy_preserves_registers_and_stack():
    source = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/item_interface_plan.json').read_text(encoding='utf-8'))
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    payload = bytes(MainCodeFile(source, 0x02000000).sections[3].data[:-48])
    result = execute(source, bytes(image.rom.arm7), image.rom.arm7RamAddress, plan['copy_entry'], payload)
    assert result['late_copy_instruction_budget'] > 10000
    assert result['late_copy_reached_caller_continuation']
    assert result['actual_startup_call_preserves_r0_r3']
    assert result['repair_returns_with_stack_preserved']
    assert result['repaired_pool_matches_complete_payload']


def test_canvas_setup_receives_complete_pool_and_restored_initial_stack():
    source = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    machine = initialized(source)
    payload = bytes(MainCodeFile(source, 0x02000000).sections[3].data[:-48])
    assert bytes(machine.mem_read(0x02387A20, len(payload))) == payload
    assert machine.reg_read(UC_ARM_REG_SP) == 0x027F0000


def test_cache_wrapper_full_copy_ABI_and_ordered_model():
    old = Path('work/analysis/item_interface_research_arm9.bin').read_bytes()
    source, _plan = transform(old)
    image = NdsImage.open('out/all_routes_combined_v158_candidate.nds')
    payload = bytes(MainCodeFile(source, BASE).sections[3].data[:-48])
    result = execute(source, bytes(image.rom.arm7), image.rom.arm7RamAddress, True, payload)
    assert result['late_copy_reached_caller_continuation']
    assert result['actual_startup_call_preserves_r0_r3']
    assert result['late_copy_cache_model']['line_count'] == 612
    assert result['SDK_staged_code_cache_line_coverage']['all_instruction_lines_selected']
    assert result['SDK_staged_code_cache_line_coverage']['all_data_lines_selected']
    assert result['late_copy_cache_model']['native_cache_instruction_count'] == 1837
    assert result['late_copy_cache_model']['worst_case_dirty_data_and_stale_instruction_model_visible']
    machine = initialized(source)
    assert bytes(machine.mem_read(0x02387A20, len(payload))) == payload


@pytest.mark.parametrize('operation_offset', (24, 28, 44))
def test_missing_instruction_invalidation_data_clean_or_final_drain_rejected(operation_offset):
    source, plan = transform(Path('work/analysis/item_interface_research_arm9.bin').read_bytes())
    code = MainCodeFile(source, BASE)
    offset = plan['cache']['entry'] - code.sections[3].ramAddress + operation_offset
    struct.pack_into('<I', code.sections[3].data, offset, 0xE1A00000)
    with pytest.raises(ValueError, match='cache wrapper differs'):
        cache_plan(bytes(code.save()))
