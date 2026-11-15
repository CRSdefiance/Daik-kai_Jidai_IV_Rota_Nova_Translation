"""Reuse exact isolated effects/clean ends; check both distinct current block ends freshly."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_controls_v7630')
SOURCE=Path('work/analysis/papal_trade_SC0_SC1_current_v7620/two_complete_current_exchanges36_source_current_refs_before_new_prose.json')
PRIOR=Path('work/analysis/lil_B234_controls_v7577/two_source_A000_structural50_normal_end_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();source,prior=map(read,[SOURCE,PRIOR]);before=read(prior['source_context'])
    old,current,clean=[NdsImage.open(p) for p in [prior['candidate'],source['current_ROM'],'work/clean.nds']]
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256'] and sha(Path(source['current_ROM']).read_bytes())==source['current_ROM_sha256']
    assert old.read_file('/__arm9__.bin')==current.read_file('/__arm9__.bin')
    clean_block=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[234]
    assert sha(clean_block)==before['blocks'][0]['clean_block_sha256']
    reused=[deepcopy(r) for r in prior['normal_terminal_seed_cases'] if r['version']=='clean-Japanese'];assert len(reused)==25
    adapter=prior['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::source-normal-end','exec'),env)
    ROOT.mkdir(parents=True);groups=[]
    for group in source['groups']:
        file,n=group['file_path'],group['block'];block=IlnkContainer.parse(current.read_file(file)).blocks[n]
        assert sha(block)==group['current_block_sha256'] and bytes.fromhex(read(source['source_packet'])['groups'][group['route']]['clean_block_hex'])==clean_block
        commands=group['all_current_native_commands'];leaves=[c for c in commands if c['word']!=0x4000]
        assert [(c['offset'],c['whole_command_hex'],c['native_extent']) for c in leaves]==[(1456,'00a0ffff6a000110',8),(1464,'00000000',4)]
        assert len(commands)==20 and len(block)==8+int.from_bytes(block[4:6],'little')==1468 and block[1464:]==bytes(4)
        effects=[]
        for label in ['clean-Japanese','current-English']:
            oldcase=deepcopy(next(c for c in prior['source_A000_structural_cases'] if c['version']==label))
            assert oldcase['source_command_hex']==leaves[0]['whole_command_hex'] and oldcase['error'] is None and oldcase['logical_end']==oldcase['stopped_offset']==16
            effects.append(dict(version=label,proof_mode='exact-isolated-eight-byte-A000-input-andwhole-ARM9-reuse',case=oldcase))
        cases=[env['end_case'](current.read_file('/__arm9__.bin'),block,1464,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]
        assert len(cases)==25 and all(not c['flagged_terminal'] and c['native_result'][0]==0 and c['native_result'][1]==c['initial_value_word'] for c in cases)
        groups.append(dict(route=group['route'],file_path=file,block=n,current_block_sha256=sha(block),source_andcurrent_two_non_speech_commands=leaves,isolated_A000_structural_proof_reuse=effects,fresh_current_normal_end_cases=cases,exact_shared_clean_normal_end_proof_reference=str(PRIOR),exact_shared_clean_normal_end_case_count=25,normal_state0_retains_seeded_value_in_all25_current_cases=True,source_andcurrent1468_logical1468_tail0_end1464_preserved=True,opaque_effects_not_full_item_blessing_ownership_location_orreward_semantics=True))
    save(ROOT/'two_current_blocks50_fresh_seeded_ends_exact_effect_andclean_end_reuse.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),prior_exact_source_control_proof=str(PRIOR),prior_exact_source_control_proof_sha256=sha(PRIOR.read_bytes()),groups=groups,fresh_current_normal_end_cases=50,distinct_exact_reused_clean_normal_end_cases=25,distinct_exact_reused_isolated_A000_structural_cases=2,reused_shared_clean_cases=reused,source_owned_seeded_end_adapter=adapter,no_source_current_opaque_operand_orend_orstorage_tail_omission=True,isolated_command_checks_not_route_gameplay_orfull_VM_effect_execution=True,no_new_emulator_run_controller_RNG_role_roster_funds_or_event_forcing=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,PRIOR,Path(prior['source_context']),Path(__file__)]},full_goal_complete=False))
    print('Both current blocks:50 fresh seeded normal ends pass;25 identical clean end cases andtwo exact isolated A000 cases reused.Zero source/target tails andcomplete four-byte ends remain;effects/activation unproved.')
