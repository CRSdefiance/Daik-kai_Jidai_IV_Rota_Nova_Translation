"""Calibrate indexed leads and check the one arithmetic address coincidence."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, call, machine
from scripts.trace_control_aliases_v688 import sections
from scripts.trace_frame_crop_arguments_v584 import branch
from scripts.trace_indexed_owners_v738 import ROOT, scan
from scripts.verify_village_wrap_v608 import read, save

CONTROL = 0x02450000
TARGET = 0x023139C0
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR)


def assembled(text):
    return bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(text, CONTROL)[0])


def controls(arm):
    code = assembled('ldr r2, literal; add r1,r0,r0,lsl #2; add r0,r2,r1,lsl #2; bx lr; literal: .word 0x0231390c')
    found, _ = scan([('supplied_affine_control', CONTROL, code)], {TARGET: 'supplied Confirm target'})
    assert len(found) == 1 and found[0]['witnesses'] == [
        {'index': 9, 'owner': TARGET, 'filename': 'supplied Confirm target'}]
    u = machine(arm)
    u.mem_write(CONTROL, code)
    native = []
    for index in (0, 1, 9, 255, 0xFFFFFFFF):
        before = bytes(u.mem_read(BASE, 0x400000))
        call(u, CONTROL - BASE, (index,))
        result = u.reg_read(UC_ARM_REG_R0)
        assert result == (0x0231390C + index * 20) & 0xFFFFFFFF
        assert bytes(u.mem_read(BASE, 0x400000)) == before
        native.append({'index': index, 'native_result': result, 'complete_RAM_and_call_ABI_pass': True})
    table = CONTROL + 32
    code = assembled(f'ldr r2, literal; ldr r0,[r2,r0,lsl #2]; bx lr; literal: .word {table}')
    code = code.ljust(32, b'\0') + struct.pack('<4I', 0, 0, TARGET, 0)
    found, _ = scan([('supplied_indexed_table_control', CONTROL, code)], {TARGET: 'supplied Confirm target'})
    assert len(found) == 1 and found[0]['kind'] == 'indexed_source_table'
    assert found[0]['witnesses'] == [{'index': 2, 'address': table + 8, 'owner': TARGET,
                                     'filename': 'supplied Confirm target'}]
    u.mem_write(CONTROL, code)
    before = bytes(u.mem_read(BASE, 0x400000))
    call(u, CONTROL - BASE, (2,))
    assert u.reg_read(UC_ARM_REG_R0) == TARGET
    assert bytes(u.mem_read(BASE, 0x400000)) == before
    boundaries = []
    for label, instruction in (('conditional', 'movne r2,r2'), ('call', 'bl 0x02450100'),
                                ('store', 'str r1,[r2]'), ('write_PC', 'mov pc,lr')):
        code = assembled(f'ldr r2,literal; {instruction}; add r0,r2,r0,lsl #2; bx lr; literal: .word {TARGET - 4}')
        found, _ = scan([(label, CONTROL, code)], {TARGET: 'supplied target'})
        assert not found
        boundaries.append({'boundary': label, 'analysis_forgets_prior_values_not_a_global_nonuse_control': True})
        if label == 'write_PC':
            u.mem_write(CONTROL, code)
            call(u, CONTROL - BASE, (1,))
            assert u.reg_read(UC_ARM_REG_R0) == 1
    # A source-compatible selection beyond the declared analysis window is
    # intentionally missed. Do not turn a finite search into a global claim.
    base = TARGET - 20 * 256
    code = assembled(f'ldr r2,literal; add r1,r0,r0,lsl #2; add r0,r2,r1,lsl #2; bx lr; literal: .word {base}')
    found, _ = scan([('outside_window', CONTROL, code)], {TARGET: 'supplied target'})
    assert not found
    u.mem_write(CONTROL, code)
    call(u, CONTROL - BASE, (256,))
    assert u.reg_read(UC_ARM_REG_R0) == TARGET
    return {'five_full_native_affine_and_U32_wrap_cases': native,
            'indexed_readonly_table_control_and_native_return_exact': True,
            'conservative_boundary_controls': boundaries,
            'write_PC_native_control_returns_before_dead_arithmetic': True,
            'index256_native_hit_outside_search_window_control_proves_finite_limit': True,
            'unaligned_memory_rotation_multiple_variables_and_opaque_flows_not_validated': True}


def callers(parts, target):
    direct, pointers, thumb = [], [], []
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for label, base, data in parts:
        for offset in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, offset)[0]
            if branch(word, base + offset) == target:
                direct.append({'unit': label, 'PC': base + offset, 'link': bool(word & 0x01000000)})
        for offset in range(len(data) - 3):
            if struct.unpack_from('<I', data, offset)[0] & ~1 == target:
                pointers.append({'unit': label, 'address': base + offset})
        for offset in range(0, len(data) - 3, 2):
            first, second = struct.unpack_from('<2H', data, offset)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800):
                continue
            ins = next(decoder.disasm(data[offset:offset + 4], base + offset, count=1), None)
            if ins and ins.mnemonic in ('bl', 'blx') and ins.op_str.startswith('#0x') and int(ins.op_str[1:], 16) == target:
                thumb.append({'unit': label, 'PC': ins.address})
    return {'ARM_direct': direct, 'stored_absolute_pointers': pointers, 'Thumb_direct': thumb,
            'computed_indirect_callers_not_excluded': True}


def main():
    assert not (ROOT / 'proof.json').exists()
    result = read(ROOT / 'verified_leads.json')
    assert result['producer_sha256'] == sha(Path('scripts/trace_indexed_owners_v738.py').read_bytes())
    assert len(result['targets']) == 21
    assert result['all315_initialized_resource_names_writes_and_executed_code_clean_current_exact']
    rows = []
    for label, path in (('clean', Path('work/clean.nds')), ('current', Path('out/all_routes_combined_v712_candidate.nds'))):
        rom = NdsImage.open(path)
        arm, parts = rom.read_file('/__arm9__.bin'), sections(rom)
        version = result['versions'][label]
        assert version['candidate_sha256'] == sha(path.read_bytes())
        assert version['parts'] == [{'name': n, 'base': b, 'bytes': len(d), 'sha256': sha(d)} for n, b, d in parts]
        lead, = version['leads']
        assert lead['PC'] == 0x020D2ED4 and lead['kind'] == 'affine_owner_base'
        assert lead['witnesses'] == [{'index': 102, 'owner': 0x02313B8C, 'filename': '_pxl/seamap.pxl'}]
        assert (lead['constant'], lead['coefficient'], lead['variable']) == (0x0231220C, 64, 'r0')
        calibration = controls(arm)
        census = callers(parts, 0x020D2ECC)
        assert census['ARM_direct'] == [{'unit': 'main0', 'PC': pc, 'link': True} for pc in (0x020D2EA4, 0x020D2EAC)]
        assert not census['stored_absolute_pointers'] and not census['Thumb_direct']
        u = machine(arm)
        observed = []
        for index in (0, 1, 102):
            u.reg_write(UC_ARM_REG_R0, index)
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            before, registers, flags = bytes(u.mem_read(BASE, 0x400000)), [u.reg_read(r) for r in REGS], u.reg_read(UC_ARM_REG_CPSR)
            u.emu_start(0x020D2ECC, 0x020D2ED8, count=3)
            assert u.reg_read(UC_ARM_REG_PC) == 0x020D2ED8
            assert u.reg_read(UC_ARM_REG_R0) == 0x0231220C + index * 64
            assert u.reg_read(UC_ARM_REG_R1) == 0x0231220C and u.reg_read(UC_ARM_REG_R12) == struct.unpack_from('<I', arm, 0xD2EE0)[0] == 0x02100498
            assert all(u.reg_read(r) == value for r, value in zip(REGS, registers, strict=True)
                       if r not in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R12))
            assert bytes(u.mem_read(BASE, 0x400000)) == before and u.reg_read(UC_ARM_REG_CPSR) == flags
            observed.append({'supplied_index': index, 'native_pointer': u.reg_read(UC_ARM_REG_R0),
                             'complete4MiB_RAM_flags_and_unwritten_registers_exact': True,
                             'stopped_before_original_tail_target_not_a_graphics_draw': True})
        source_inputs = []
        for start, stop in ((0x020D2E98, 0x020D2EA4), (0x020D2EA8, 0x020D2EAC)):
            before = bytes(u.mem_read(BASE, 0x400000))
            u.reg_write(UC_ARM_REG_R0, 0xBABA1234)
            u.reg_write(UC_ARM_REG_R1, 0xBABA5678)
            u.emu_start(start, stop, count=3)
            assert u.reg_read(UC_ARM_REG_PC) == stop and u.reg_read(UC_ARM_REG_R0) == 1
            assert bytes(u.mem_read(BASE, 0x400000)) == before
            source_inputs.append({'source_prefix': [start, stop], 'native_next_call_index': 1})
        # Independent source evidence of exactly two initialized 64-byte objects.
        assert arm[0xD2F08:0xD2F18] == bytes.fromhex('016086e2020056e3405085e2f8ffffba')
        assert struct.unpack_from('<I', arm, 0xD2F70)[0] == 0x0231220C
        rows.append({'version': label, 'analysis_units': version['statistics'],
                     'calibration': calibration, 'call_reference_census': census,
                     'three_original_address_prefix_witnesses': observed,
                     'both_direct_call_prefixes_supply_index1': source_inputs,
                     'two_object_initialization_source_range': [0x020D2EE4, 0x020D2F18],
                     'address102_coincidence_not_an_identified_original_seamap_consumer': True,
                     'original_prefix_bytes_sha256': sha(arm[0xD2ECC:0xD2EE4]),
                     'initializer_loop_bytes_sha256': sha(arm[0xD2EE4:0xD2F74])})
    for path, digest in result['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', {
        'versions': rows, 'all21_owner_targets_accounted': result['targets'],
        'bounded_index0_to255_AL_one_variable_lead_scope_complete': True,
        'one_seamap_address_match_is_not_a_display_parent': True,
        'original_four_unresolved_consumer_families_and_full_goal_remain_open': True,
        'source_tables_runtime_mutation_unaligned_reads_Thumb_variable_and_other_index_domains_not_excluded': True,
        'prototype_tail_target_transcription_corrected_to_exact_source_literal_02100498_no_ROM_change': True,
        'previous_goal_turn_classification': 'progress: V737 final graphics copy gate and exact full rebuild',
        'producer_sha256': result['producer_sha256'], 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'release_hashes_unchanged': result['release_hashes_unchanged'], 'full_goal_complete': False})
    print('V738: both source versions have one arithmetic coincidence; original direct callers use1,not102. No new original graphics parent.', flush=True)


if __name__ == '__main__':
    main()
