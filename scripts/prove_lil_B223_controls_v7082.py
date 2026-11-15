"""Bind the unforced source predicate,letter staging,normal end and two structural paths."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_controls_v7082')
SOURCE=Path('work/analysis/lil_B223_source_v7078/all17_clean_current_letter_notices_reactions_full1316_inverse.json')
INPUT=Path('work/analysis/current_V7067_native_v7077/current_native_input.json')
BRANCH=Path('work/analysis/lil_B223_branches_v7081/original_relative_skip_operand_proof.json')
SEEDED=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks[223] for i in images];spec=packet['blocks'][0]
    assert packet['source_relative_sites']==4 and packet['source_predicates']==1 and packet['source_typed_commands']==1 and packet['source_A000']==1
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');predicates=[];structural=[];ends=[]
    adapter=read(SEEDED)['source_owned_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::seeded-normal-end','exec'),env)
    for label,image,block,key in zip(['clean-source','current'],images,blocks,['all_clean_native_commands','all_current_native_commands'],strict=True):
        assert len(block)==8+struct.unpack_from('<H',block,4)[0]==1316 and block[1312:]==bytes(4)
        command=next(c for c in spec[key] if c['word']==0x8000);assert command['offset']==1138 and command['whole_command_hex']=='0080ffff0dfe0030'
        value=ctx.execute(predicate,block,command);ctx.machines.pop();assert value['native_result'][0]==2 and value['native_result'][1] in [0,1] and value['native_extent']==8;predicates.append(dict(version=label,**value))
        for command in spec[key]:
            if command['word'] not in [0x4500,0x4621,0xA000]:continue
            raw=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;result=walk(image.read_file('/__arm9__.bin'),isolated)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==command['word'] and result['rows'][0]['native_extent']==command['native_extent']
            structural.append(dict(version=label,original_offset=command['offset'],word=command['word'],source_command_hex=raw.hex(),**result))
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**env['end_case'](image.read_file('/__arm9__.bin'),block,1312,previous,seed)))
    assert predicates[0]['native_result']==predicates[1]['native_result'] and not ctx.machines and len(structural)==10 and len(ends)==50 and all(not e['flagged_terminal'] and e['native_result'][0]==0 and e['native_result'][1]==e['initial_value_word'] for e in ends)
    for a,b in zip(structural[:5],structural[5:],strict=True):assert a['original_offset']==b['original_offset'] and a['source_command_hex']==b['source_command_hex'] and a['rows']==b['rows'] and a['opaque_effect_bridges']==b['opaque_effect_bridges']
    branch=read(BRANCH);assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==40 and len(branch['operands_requiring_adjustment_when_resizing'])==4
    commands={c['offset']:c for c in spec['all_clean_native_commands']};routes=[]
    for value in [0,1]:
        at=8;visited=[];last=0
        while at<1316:
            c=commands[at];visited.append(at)
            if c['word']==0x8000:last=value
            if c['word'] in [0x100,0x200,0x300]:at=next(r for r in branch['cases'] if r['version']=='clean' and r['offset']==at and r['last_choice_or_result']==last)['original_next_command_offset']
            else:at+=c['native_extent']
        speeches=[c['offset'] for c in commands.values() if c['offset'] in visited and c['word']==0x4000]
        assert len(speeches)==8+2*value and (1158 in speeches)==bool(value) and (1270 in speeches)==bool(value)
        routes.append(dict(predicate_Boolean_value=value,offsets=visited,speech_offsets=speeches,structural_model_only_not_forced_gameplay_or_natural_reachability=True))
    save(ROOT/'two_unforced_predicate_cases_ten_structural_cases50_seeded_ends_two_route_models.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),predicate_cases=predicates,original_predicate_type2_Boolean_not_menu_or_outer_eligibility=True,raw0dfe0030_preserved_complete_operand_meaning_not_inferred=True,four_relative_sites40_native_cases=str(BRANCH),four_relative_sites40_native_cases_sha256=sha(BRANCH.read_bytes()),two_structural_route_models=routes,source4500_4621_A000_structural_cases=structural,all_five_opaque_source_operands_and_extents_preserved=True,opaque_staging_resource_or_effect_bodies_bridged_not_explained_or_actual_gameplay=True,normal_terminal_seed_cases=ends,normal_state0_retains_seeded_value_word_in_all50_cases=True,original_end1312_full4bytes_and_zero_tail_preserved=True,no_predicate_event_role_roster_RNG_or_gameplay_result_forced=True,original_predicate_source=inspect.getsource(predicate),source_owned_seeded_end_adapter=adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),natural_event223_location_earned_progress_full_effects_routes_and_hardware_unclaimed=True,new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,BRANCH,SEEDED,Path(__file__)]},full_goal_complete=False))
    print(dict(predicate_results=[r['native_result'][:2] for r in predicates],opaque_cases=10,normal_seeded_cases=50,structural_speeches=[len(r['speech_offsets']) for r in routes],credit=0))
