"""Reconcile constant-flow leads with exact native loads and prior owner census."""

import struct
from pathlib import Path

from unicorn import arm_const

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.trace_control_aliases_v688 import ROOT, TARGETS
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre = read(ROOT / 'preflight.json')
    leads = read(ROOT / 'constant_flow_leads.json')
    owners = read(ROOT / 'native_owner_proof.json')
    assert leads['analyzer_sha256'] == sha(Path('scripts/trace_control_aliases_v688.py').read_bytes())
    assert owners['verifier_sha256'] == sha(Path('scripts/verify_control_owners_v688.py').read_bytes())
    old_frame = read('work/analysis/frame_callers_v584/crop_argument_census.json')
    expected_frame = sorted(r['owner_load'] for r in old_frame['owner_load_cases'])
    assert len(expected_frame) == 48
    native = []
    by_version = {}
    register_ids = {f'r{n}': getattr(arm_const, 'UC_ARM_REG_R' + str(n)) for n in range(13)}
    for version, data in leads['versions'].items():
        u = machine(NdsImage.open(data['ROM']).read_file('/__arm9__.bin'))
        rows = data['owner_candidates']
        assert len(rows) == 50 and all(r['direct_literal_owner_load'] for r in rows)
        assert all(r['owner_field_offset'] == 0 for r in rows)
        assert sorted(r['PC'] for r in rows if r['target'] == 'Frame') == expected_frame
        assert [r['PC'] for r in rows if r['target'] == 'Confirm'] == [0x0210EBDC, 0x0210EBE8]
        by_version[version] = [(r['PC'], r['target'], r['value']) for r in rows]
        for row in rows:
            pc = row['PC']
            dest = {'sb': 'r9', 'sl': 'r10', 'fp': 'r11', 'ip': 'r12'}.get(row['register'], row['register'])
            assert struct.unpack('<I', u.mem_read(row['source_word_address'], 4))[0] == TARGETS[row['target']][0]
            last = row['bounded_instruction_chain'][-1]
            assert last['PC'] == pc and bytes(u.mem_read(pc, 4)).hex() == last['bytes']
            for n, reg in enumerate(register_ids.values()):
                u.reg_write(reg, 0xA5550000 + n * 4)
            u.reg_write(arm_const.UC_ARM_REG_SP, 0x027F0000)
            u.reg_write(arm_const.UC_ARM_REG_LR, 0x027E0000)
            before = {name: u.reg_read(reg) for name, reg in register_ids.items()}
            ram = bytes(u.mem_read(0x02000000, 0x400000))
            u.emu_start(pc, pc + 4, count=1)
            assert u.reg_read(arm_const.UC_ARM_REG_PC) == pc + 4
            assert u.reg_read(register_ids[dest]) == row['value']
            assert all(u.reg_read(reg) == before[name] for name, reg in register_ids.items() if name != dest)
            assert bytes(u.mem_read(0x02000000, 0x400000)) == ram
            assert u.reg_read(arm_const.UC_ARM_REG_SP) == 0x027F0000
            assert u.reg_read(arm_const.UC_ARM_REG_LR) == 0x027E0000
            native.append({'version': version, 'PC': pc, 'owner': row['value'],
                'native_single_literal_load_and_other_registers_RAM_stack_unchanged': True,
                'not_a_full_parent_or_rendering_execution': True})
    assert by_version['source'] == by_version['current']
    assert len(native) == 100
    current = leads['versions']['current']
    assert any(s['section'] == 'verified_startup_copy_live_POOL' for s in current['sections'])
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', {
        'constant_flow_sha256': sha((ROOT / 'constant_flow_leads.json').read_bytes()),
        'native_owner_proof_sha256': sha((ROOT / 'native_owner_proof.json').read_bytes()),
        'two_complete_native_initializers_and_guarded_constructor_controls_pass': True,
        'all100_source_current_literal_load_instructions_verified': native,
        'actual20_byte_owners_exclude_neighbor_plate4016_and_next_Frame_resource': True,
        'no_additional_computed_owner_lead_in_supported_bounded_ARM_constant_flow': True,
        '50_known_sites_per_version_match_prior2_Confirm48_Frame_census': True,
        'both_staged_storage_and_verified_live_POOL_instruction_views_included': True,
        'Thumb_dynamic_alias_cross_call_and_branch_value_flows_not_excluded': True,
        'six_actual_control_contexts_still_open_no_global_unused_claim': True,
        'next_action_other_dynamic_reader_or_distinct_gameplay_context_not_repeat_same_owner_census': True,
        'no_ROM_code_artwork_registry_or_release_pointer_changed': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V688:20-byte boundaries source-bound;100 native load controls; no new bounded alias lead; six contexts remain open.', flush=True)


if __name__ == '__main__':
    main()
