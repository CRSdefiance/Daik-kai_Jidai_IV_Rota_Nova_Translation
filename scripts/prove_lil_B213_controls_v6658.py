"""Bind unforced predicate, staging/effect operands and seeded normal termination; effects remain opaque."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B213_controls_v6658');SOURCE=Path('work/analysis/lil_B213_source_v6651/eighteen_clean_current_full_prophecy_exchange_source_references.json');INPUT=Path('work/analysis/current_V6641_native_v6650/current_native_input.json');BRANCH=Path('work/analysis/lil_B213_branches_v6654/original_relative_skip_operand_proof.json');SEEDED=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks[213] for i in images];spec=packet['blocks'][0];ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');predicates=[]
    for label,block,key in zip(['clean-source','current'],blocks,['all_clean_native_commands','all_current_native_commands'],strict=True):
        command=next(c for c in spec[key] if c['word']==0x8000);assert (command['offset'],command['whole_command_hex'])==(740,'0080ffff09fe0030');value=ctx.execute(predicate,block,command);ctx.machines.pop();assert value['native_result'][0]==2 and value['native_result'][1] in [0,1] and value['native_extent']==8;predicates.append(dict(version=label,**value))
    assert predicates[0]['native_result']==predicates[1]['native_result'] and not ctx.machines;adapter=read(SEEDED)['source_owned_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::same-seeded-terminal-contract','exec'),env);structural=[];ends=[]
    for label,image,block,key in zip(['clean-source','current'],images,blocks,['all_clean_native_commands','all_current_native_commands'],strict=True):
        arm=image.read_file('/__arm9__.bin');assert len(block)==1028 and 8+struct.unpack_from('<H',block,4)[0]==1026 and block[1022:]==bytes(6)
        for command in spec[key]:
            if command['word'] not in [0x4821,0x4720,0xA000]:continue
            raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;result=walk(arm,isolated);assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==command['word'] and result['rows'][0]['native_extent']==command['native_extent'];structural.append(dict(version=label,original_offset=command['offset'],word=command['word'],source_command_hex=raw.hex(),**result))
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**env['end_case'](arm,block,1022,previous,seed)))
    assert len(structural)==6 and len(ends)==50 and all(not e['flagged_terminal'] and e['native_result'][0]==0 and e['native_result'][1]==e['initial_value_word'] for e in ends)
    for a,b in zip(structural[:3],structural[3:],strict=True):assert a['original_offset']==b['original_offset'] and a['source_command_hex']==b['source_command_hex'] and a['rows']==b['rows'] and a['opaque_effect_bridges']==b['opaque_effect_bridges']
    branch=read(BRANCH);assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==40 and [(r['offset'],r['matched_skip_target']) for r in branch['operands_requiring_adjustment_when_resizing']]==[(748,756),(752,760),(756,830),(826,830)];routes=[];commands={c['offset']:c for c in spec['all_clean_native_commands']}
    for value in [0,1]:
        at=8;visited=[]
        while at<1026:
            c=commands[at];visited.append(at)
            if c['word'] in [0x100,0x200,0x300]:
                case=next(r for r in branch['cases'] if r['version']=='clean' and r['offset']==at and r['last_choice_or_result']==value);at=case['original_next_command_offset']
            else:at+=c['native_extent']
        spoken=[c['offset'] for c in spec['all_clean_native_commands'] if c['offset'] in visited and c['word']==0x4000];assert len(spoken)==17+value and (760 in spoken)==bool(value);routes.append(dict(predicate_Boolean=value,offsets=visited,speech_offsets=spoken,structural_routes_using_native_branch_cases_not_full_VM_or_actual_reachability=True))
    save(ROOT/'two_unforced_predicates_six_structural_cases50_seeded_ends_two_branch_models.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),predicate_cases=predicates,original_8000_predicate_type2_Boolean_not_choice_or_event_eligibility=True,raw09fe0030_operand_preserved_no_unproved_membership_semantics=True,four_relative_sites40_native_cases=str(BRANCH),four_relative_sites40_native_cases_sha256=sha(BRANCH.read_bytes()),two_structural_route_models=routes,source4821_4720_A000_structural_cases=structural,all_three_opaque_source_operands_and_extents_preserved=True,opaque_staging_resource_or_item_effect_bodies_bridged_not_explained_or_claimed_as_actual=True,normal_terminal_seed_cases=ends,normal_state0_retains_seeded_value_word_in_all50_cases=True,original_end1022_full4bytes_and_tail2_preserved=True,no_predicate_event_flag_role_roster_RNG_or_gameplay_result_forced=True,original_predicate_source=inspect.getsource(predicate),source_owned_seeded_end_adapter=adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),natural_event213_location_earned_progress_full_effects_routes_hardware_unclaimed=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(Path(p).read_bytes()) for p in [SOURCE,INPUT,BRANCH,SEEDED,Path(__file__)]},full_goal_complete=False));print(dict(predicate_results=[p['native_result'][:2] for p in predicates],opaque_structural_cases=6,seeded_normal_ends=50,structural_speech_path_counts=[len(r['speech_offsets']) for r in routes],credit=0))
