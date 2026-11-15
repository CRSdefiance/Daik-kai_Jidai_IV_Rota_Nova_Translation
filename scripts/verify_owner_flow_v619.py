"""Independent native control witnesses and original-owner follow-up for the flow scan."""

from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from keystone import KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB, Ks
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.trace_resource_owner_tables_v585 import initialize
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/owner_flow_v619')
ROM = Path('out/all_routes_combined_v617_candidate.nds')


def main():
    proof_path = ROOT / 'flow_candidates.json'
    p = read(proof_path)
    assert p['script_sha256'] == sha(Path('scripts/scan_owner_flow_v619.py').read_bytes())
    assert p['candidate_sha256'] == sha(ROM.read_bytes())
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    assembly = 'mov r0,#64; mov r1,#65; mov r2,#66; mov r3,#67; mov ip,#68; bx lr'
    arm_callee = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, 0x02100000)[0])
    thumb_callee = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(
        'movs r0,#64; movs r1,#65; movs r2,#66; movs r3,#67; bx lr', 0x02100000)[0])
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    controls = []
    for row in p['synthetic_analysis_controls']:
        data = bytes.fromhex(row['bytes_hex'])
        assert sha(data) == row['input_sha256']
        stop = next(i.address for i in md.disasm(data, BASE) if i.mnemonic == 'bx' and i.op_str == 'lr')
        cases = []
        for branch_input in (0, 1):
            u = machine(arm)
            u.mem_write(BASE, data)
            u.mem_write(0x02100000, thumb_callee if row['name'].startswith('interworking') else arm_callee)
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_R0, branch_input)
            u.reg_write(UC_ARM_REG_R1, 0x02460000)
            u.reg_write(UC_ARM_REG_R5, branch_input)
            u.emu_start(BASE, stop, count=500)
            assert u.reg_read(UC_ARM_REG_PC) == stop
            actual = u.reg_read(UC_ARM_REG_R0)
            expected = {
                'cross_branch_and_preserved_register_call': 0x023139C0,
                'indexed_table': 0x023139C4,
                'interworking_call_preserves_saved_register': 0x023139C0,
                'clobbered_argument_negative': 68,
                'unknown_index_negative': 0x023139C4 if branch_input else 4,
                'unknown_branch_join_negative': 0x02460000 if branch_input else 0x023139C0,
            }[row['name']]
            assert actual == expected, (row['name'], branch_input, actual, expected)
            cases.append({'input': branch_input, 'native_r0': actual, 'stop_before_final_return': stop})
        controls.append({'name': row['name'], 'native_execution_cases': cases,
                         'unknown_join_or_index_can_include_target_and_is_not_nonuse_proof': row['name'] in (
                             'unknown_index_negative', 'unknown_branch_join_negative')})
    assert len(controls) == 6
    current = NdsImage.open(ROM)
    clean = NdsImage.open('work/clean.nds')
    a, _, executed, writes, owners, filenames = initialize(current)
    b, _, source_executed, source_writes, source_owners, source_filenames = initialize(clean)
    assert executed == source_executed and writes == source_writes
    assert owners == source_owners and filenames == source_filenames
    assert all(a.mem_read(pc, 4) == b.mem_read(pc, 4) for pc in executed)
    expected = [0x02085460, 0x0210E1D4, 0x0210E1D8, 0x0210E1DC,
                0x0210EBF0, 0x0210EBF4, 0x0210EBF8]
    assert [r['instruction'] for r in p['flow']['candidates']] == expected
    assert p['flow']['candidate_rows_recomputed_only_after_fixed_point_converged']
    assert any(r['name'] == 'runtime_pool_copy' for r in p['source_units'])
    before = read('work/analysis/frame_callers_v584/crop_argument_census.json')
    frame = next(r for r in before['owner_load_cases'] if r['owner_load'] == 0x02085434)
    assert frame['call'] == 0x02085470 and frame['source_XYWH'] == [80, 216, 8, 8]
    original = clean.read_file('/__arm9__.bin')
    assert arm[0x85420:0x85480] == original[0x85420:0x85480]
    save(ROOT / 'flow_followup_proof.json', {'candidate_sha256': p['candidate_sha256'],
         'flow_proof_sha256': sha(proof_path.read_bytes()), 'independent_native_control_witnesses': controls,
         'original_complete_initializer_instructions': len(executed), 'original_initialized_owners': len(owners),
         'current_clean_initializer_bytes_writes_owners_and_filenames_exact': True,
         'six_owner_memory_candidates_are_original_initializer_fields': expected[1:],
         'sole_frame_copy_candidate_source_rect': frame['source_XYWH'],
         'sole_frame_copy_candidate_original_source_code_exact': True,
         'no_new_ordinary_Confirm_or_miniature_consumer_found_in_this_bounded_model': True,
         'unresolved_switch_Thumb_runtime_alias_and_other_readers_remain_open': True,
         'neither_global_unused_nor_full_goal_completion_proven': True,
         'production_ROM_and_patch_unchanged': True, 'all18_plaques_incomplete_all22_scopes_retained': True,
         'full_goal_complete': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('12 independent native ISA witnesses;complete original315-owner initializer;all7 flow candidates classified. No new ordinary parent credit.')


if __name__ == '__main__':
    main()
