"""Close ordinary selector entry edges and explicit-width forwarding."""

import struct
from pathlib import Path

from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census, CURRENT
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.research_scheme_name_width_v787 import ROOT, PRIOR, WIDTH, live, scheme, widget, WIDGET, IDS, get
from scripts.verify_village_wrap_v608 import read, save


def main():
    arm = (ROOT/'WIDTH_RESEARCH_ONLY.bin').read_bytes()
    proof = read(ROOT/'native_width_verification.json')
    assert sha(arm) == proof['target_ARM9_sha256']
    clean, current = [NdsImage.open(p) for p in ('work/clean.nds', CURRENT)]
    source = clean.read_file('/__arm9__.bin')
    expected_edges = {
        0x0204F0AC: (0x0204EF40, 0x0204EFC0, 0x0209B39C),
        0x0204EF0C: (0x020967C4,),
        0x0204EF6C: (0x020407BC, 0x0204AB98)}
    reference_census = []
    for target, callers in expected_edges.items():
        expected = [['ARM_branch', 'section0', at, target, False] for at in callers]
        for name, rom in (('clean', clean), ('V783', current)):
            result = census(rom, [[target, target+4]], [])
            assert sorted(result) == sorted(expected), (name, hex(target), result)
            reference_census.append({'version': name, 'target': target, 'all_incoming_references': result})

    # Original external caller fragments each write their width argument as
    # constant zero. Other registers are explicit ABI inputs,not eligible
    # quest/faction/object-list claims.
    caller_cases = []
    for begin, end, offset in ((0x40784, 0x407BC, 0), (0x4AB70, 0x4AB98, 0),
                               (0x967A4, 0x967C4, 4), (0x9B36C, 0x9B39C, 4)):
        assert arm[begin:end+4] == source[begin:end+4]
        cpu = live(arm, True)
        widget(cpu)
        cpu.mem_write(STACK-0x100, bytes(0x600))
        for reg, value in ((UC_ARM_REG_R0, WIDGET), (UC_ARM_REG_R1, 0), (UC_ARM_REG_R2, 0),
                           (UC_ARM_REG_R3, 0), (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
            cpu.reg_write(reg, value)
        cpu.emu_start(BASE+begin, BASE+end, count=1000)
        assert cpu.reg_read(UC_ARM_REG_PC) == BASE+end
        value = struct.unpack('<I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP)+offset, 4))[0]
        assert value == 0
        caller_cases.append({'source_span': [BASE+begin, BASE+end],
            'source_current_bytes_sha256': sha(source[begin:end+4]),
            'original_call_site': BASE+end, 'width_argument_stack_offset_at_call': offset,
            'observed_explicit_width': value})

    forwards = []
    for fn, end, input_offset in ((0x4EF0C, 0x4EF40, 4), (0x4EF6C, 0x4EFC0, 0)):
        assert arm[fn:end+4] == source[fn:end+4]
        cpu = live(arm, True)
        widget(cpu)
        cpu.mem_write(IDS, struct.pack('<I', 0x0D000000))
        cpu.mem_write(STACK, struct.pack('<5I', 0, 0, 0, 0, 1))
        values = [WIDGET, IDS, 1, 0] if fn == 0x4EF0C else [IDS, 1, 0, 0]
        for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), values):
            cpu.reg_write(reg, value)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.emu_start(BASE+fn, BASE+end, count=100000)
        assert cpu.reg_read(UC_ARM_REG_PC) == BASE+end
        assert struct.unpack('<I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP)+4, 4))[0] == 0
        forwards.append({'original_wrapper': BASE+fn, 'stop_before_constructor_call': BASE+end,
            'caller_width_parameter_stack_offset': input_offset,
            'forwarded_constructor_width_parameter_stack_offset': 4, 'forwarded_width': 0,
            'full_original_stack_and_native_constructor_prefix_executed': True})

    width_cases = []
    for kind in range(10):
        cpu = live(arm, True)
        obj = scheme(cpu, kind)
        before = bytes(cpu.mem_read(BASE, 0x800000))
        assert get(cpu, WIDTH-BASE, (obj,)) == 24
        assert bytes(cpu.mem_read(BASE, 0x800000)) == before
        width_cases.append({'type': kind, 'cells': 24, 'whole8MiB_and_callee_saved_ABI_exact': True})
    save(ROOT/'selector_entry_closure.json', {'source_ARM9_sha256': sha(source),
        'research_ARM9_sha256': sha(arm), 'all_clean_current_constructor_reference_edges': reference_census,
        'four_original_external_auto_width_fragments': caller_cases,
        'two_original_forwarding_wrappers': forwards, 'ten_complete_width_getter_contracts': width_cases,
        'all_discovered_external_constructor_entries_request_automatic_class_width': True,
        'no_absolute_ADR_Thumb_or_other_ARM_entry_reference_leads': True,
        'ordinary_static_entry_closure_not_unbounded_indirect_control_flow_proof': True,
        'CPU_field_inputs_not_actual_letter_acquisition_or_quest_eligibility': True,
        'full_SDK_allocation_GPU_and_actual_menu_playback_still_pending': True,
        'no_registered_ROM_or_editorial_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('All six original selector edges,four auto-width caller fragments,two forwarding wrappers and ten8MiB/ABI width-getter cases pass. Actual UI allocation/playback remain pending.', flush=True)


if __name__ == '__main__':
    main()
