"""Bind the unforced predicate,630B/A000 structure,normal residual end and both original branch models."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B216_controls_v6796');SOURCE=Path('work/analysis/lil_B216_source_v6785/eleven_clean_current_Arthur_exchange_source_references.json');INPUT=Path('work/analysis/current_V6775_native_v6784/current_native_input.json');BRANCH=Path('work/analysis/lil_B216_branches_v6787/original_relative_skip_operand_proof.json');SEEDED=Path('work/analysis/lil_B212_seeded_ends_v6634/150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);spec=packet['blocks'][0];ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');predicates=[];structural=[];ends=[];adapter=read(SEEDED)['source_owned_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::original-seeded-end','exec'),env)
    for label,path,key in [('clean-source','work/clean.nds','all_clean_native_commands'),('current',packet['current_ROM'],'all_current_native_commands')]:
        im=NdsImage.open(path);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[216];commands=spec[key];assert len(block)==580 and 8+struct.unpack_from('<H',block,4)[0]==580 and block[576:]==bytes(4) and len(commands)==19;command=next(c for c in commands if c['word']==0x8000);assert (command['offset'],command['whole_command_hex'])==(454,'0080ffff09fe0030');result=ctx.execute(predicate,block,command);ctx.machines.pop();assert result['native_result'][0]==2 and result['native_result'][1] in [0,1] and result['native_extent']==8 and result['sole_scratch_restore_recovers_all4MiB_exact'];predicates.append(dict(version=label,**result))
        for c in commands:
            if c['word'] not in [0x630B,0xA000]:continue
            raw=bytes.fromhex(c['whole_command_hex']);isolated=b'CS\0\1'+len(raw).to_bytes(2,'little')+bytes(2)+raw;value=walk(arm,isolated);assert value['error'] is None and value['stopped_offset']==value['logical_end']==len(isolated) and len(value['rows'])==1 and value['rows'][0]['word']==c['word'] and value['rows'][0]['native_extent']==c['native_extent'];structural.append(dict(version=label,original_offset=c['offset'],word=c['word'],source_command_hex=raw.hex(),**value))
        for previous in [0,1,2,3,0xFFFFFFFF]:
            for seed in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**env['end_case'](arm,block,576,previous,seed)))
    assert predicates[0]['native_result']==predicates[1]['native_result'] and len(structural)==4 and len(ends)==50 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends) and not ctx.machines
    for a,b in zip(structural[:2],structural[2:],strict=True):assert a['source_command_hex']==b['source_command_hex'] and a['rows']==b['rows'] and a['opaque_effect_bridges']==b['opaque_effect_bridges']
    branch=read(BRANCH);assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==40 and [(r['offset'],r['matched_skip_target']) for r in branch['operands_requiring_adjustment_when_resizing']]==[(462,470),(466,524),(520,568),(564,568)];commands={c['offset']:c for c in spec['all_clean_native_commands']};routes=[]
    for last in [0,1]:
        at=8;visited=[]
        while at<580:
            c=commands[at];visited.append(at)
            if c['word'] in [0x100,0x200,0x300,0x400]:case=next(r for r in branch['cases'] if r['version']=='clean' and r['offset']==at and r['last_choice_or_result']==last);at=case['original_next_command_offset']
            else:at+=c['native_extent']
        spoken=[commands[at]['offset'] for at in visited if commands[at]['word']==0x4000];assert len(spoken)==10 and (470 in spoken)==(last==0) and (524 in spoken)==(last==1);routes.append(dict(predicate_Boolean=last,offsets=visited,speech_offsets=spoken,structural_routes_not_forced_gameplay_or_eligibility=True))
    save(ROOT/'two_predicates_four_structural_cases50_seeded_ends_two_ten_speech_models.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),predicate_cases=predicates,original_raw09fe0030_type2_Boolean_and_owned_unaligned_scratch_preserved=True,complete_predicate_membership_or_outer_eligibility_not_claimed=True,source630B_A000_structural_cases=structural,opaque_effect_bodies_bridged_not_fully_explained=True,normal_terminal_seed_cases=ends,normal_state0_retains_seeded_value_in_all50_cases=True,source_owned_seeded_end_adapter=adapter,four_relative_sites40_cases=str(BRANCH),four_relative_sites40_cases_sha256=sha(BRANCH.read_bytes()),two_structural_route_models=routes,Boolean0_Camille_Boolean1_static151_suggestion_without_forced_crew=True,normal_end576_full4bytes_no_tail_preserved=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,BRANCH,SEEDED,Path(__file__)]},full_goal_complete=False));print(dict(predicates=[r['native_result'][:2] for r in predicates],structural_cases=4,seeded_ends=50,route_speeches=[len(r['speech_offsets']) for r in routes],credit=0))
