"""Bind both branch values, original staging effects and complete ends; no forced gameplay."""
import struct,inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.research_wedding_command_v676 import walk
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_B209_source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json')
INPUT=Path('work/analysis/current_V6439_native_v6449/current_native_input.json')
ROOT=Path('work/analysis/lil_B209_controls_v6460')
OWNER,STREAM,RESULT,LENGTH=0x02650000,0x02660000,0x02668000,0x02668100
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]];blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[209] for im in images];g=packet['blocks'][0]
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');predicates=[]
    for label,block,key in zip(['source','current'],blocks,['all_clean_native_commands','all_current_native_commands'],strict=True):
        command=next(c for c in g[key] if c['word']==0x8000);p=ctx.execute(predicate,block,command);ctx.machines.pop();predicates.append(dict(version=label,**p))
    assert len(predicates)==2 and all(p['native_result']==[2,0,0,0,0,0] and p['native_extent']==8 for p in predicates) and not ctx.machines
    cases=[];edges=[];structural=[];ends=[]
    for label,image,block,key in zip(['source','current'],images,blocks,['all_clean_native_commands','all_current_native_commands'],strict=True):
        arm=image.read_file('/__arm9__.bin');original=images[0].read_file('/__arm9__.bin')
        assert all(arm[a:b]==original[a:b] for a,b in [(0x2A414,0x2A530),(0x24048,0x24118)])
        commands=g[key];logical=8+struct.unpack_from('<H',block,4)[0];assert logical==len(block)==1148 and block[1144:]==bytes(4)
        boundaries={c['offset'] for c in commands}|{logical};cpu=machine(arm);cpu.mem_write(STREAM-16,b'\xa5'*(len(block)+32));cpu.mem_write(STREAM,block)
        for command in commands:
            if command['word'] in [0x100,0x200,0x300,0x400]:
                at,word=command['offset'],command['word'];span=struct.unpack_from('<H',block,at+2)[0]
                assert at+4 in boundaries and at+4+span in boundaries
                if label=='source':edges.append(dict(offset=at,word=word,span=span,fallthrough=at+4,skip_target=at+4+span))
                for previous in [0,1,2,3,0xFFFFFFFF]:
                    cpu.mem_write(OWNER-16,b'\xa5'*64);cpu.mem_write(OWNER,struct.pack('<4I',0,STREAM+at,0,0));guard=bytes(cpu.mem_read(OWNER-16,64));cpu.mem_write(RESULT-16,b'\xa5'*80);cpu.mem_write(RESULT,bytes(24));cpu.mem_write(LENGTH-16,b'\xa5'*36);cpu.mem_write(LENGTH,bytes(4))
                    call(cpu,0x2A510,(RESULT,OWNER,LENGTH,previous));extent=struct.unpack('<I',cpu.mem_read(LENGTH,4))[0]
                    taken=word==0x100 or (word==0x200 and previous==0) or (word==0x300 and previous==1) or (word==0x400 and previous==2)
                    assert extent==4+(span if taken else 0) and struct.unpack('<6I',cpu.mem_read(RESULT,24))==(3,0,0,0,0,0)
                    assert bytes(cpu.mem_read(OWNER-16,64))==guard and bytes(cpu.mem_read(STREAM,len(block)))==block
                    for p in [STREAM-16,STREAM+len(block),RESULT-16,RESULT+24,LENGTH-16,LENGTH+4]:assert bytes(cpu.mem_read(p,16))==b'\xa5'*16
                    cases.append(dict(version=label,offset=at,word=word,previous_Boolean_or_choice_value=previous,skip_taken=taken,extent=extent,next_offset=at+extent,exact_native_boundary=True,input_owner_result_length_guards_and_ABI_exact=True))
            elif command['word'] in [0x4500,0x4621,0xA000]:
                value=bytes.fromhex(command['whole_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(value))+bytes(2)+value;result=walk(arm,isolated)
                assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated) and len(result['rows'])==1 and result['rows'][0]['word']==command['word'] and result['rows'][0]['native_extent']==command['native_extent']
                structural.append(dict(version=label,source_offset=command['offset'],word=command['word'],source_command_hex=command['whole_command_hex'],**result))
        for previous in [0,1,2,3,0xFFFFFFFF]:ends.append(dict(version=label,**end_case(arm,block,1144,previous)))
    assert [(e['offset'],e['span'],e['skip_target']) for e in edges]==[(694,4,702),(698,338,1040),(1036,54,1094),(1090,0,1094)]
    assert len(cases)==40 and len(structural)==10 and len(ends)==10
    for a,b in zip(structural[:5],structural[5:],strict=True):
        assert a['source_offset']==b['source_offset'] and a['source_command_hex']==b['source_command_hex'] and a['rows']==b['rows'] and a['opaque_effect_bridges']==b['opaque_effect_bridges']
    actual=read('work/analysis/lil_B209_source_actual_v6456/six_actual_panels24_visited_of27_stored_commands_and_honest_conditional_scope.json')
    live=next(r for r in actual['command_pairs'] if r['source_offset']==686);assert live['native_result']==[2,0]
    assert next(r for r in cases if r['version']=='source' and r['offset']==694 and r['previous_Boolean_or_choice_value']==0)['extent']==8
    save(ROOT/'two_predicates40_relative_cases10_staging_structural_cases_and10_complete_ends.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),predicate_cases=predicates,predicate_result_type=2,predicate_Boolean_value=0,actual_source_predicate_result_words=[2,0],type2_is_not_Boolean_value2=True,four_relative_edges=edges,source_current_relative_cases=cases,all_skip_and_fallthrough_targets_exact_native_boundaries=True,source4500_4621_A000_structural_cases=structural,opaque_effect_bodies_bridged_not_full_UI_resource_or_item_quest_semantics=True,source_background_and_portrait_changes_observed_separately_in6457=True,complete_end_cases=ends,all18_original_commands_complete_source_operands_and1148_bytes_bound=True,source_current_static_and_D0_voices_already_proved_separately=True,no_original_predicate_role_actor_or_gameplay_result_forced=True,natural_event209_location_earned_progress_full_effects_routes_and_hardware_unclaimed=True,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),original_helpers={n:inspect.getsource(f) for n,f in [('predicate',predicate),('structural',walk),('end',end_case)]},new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},full_goal_complete=False))
    print('B209 two original predicates(type2/Boolean0),40 relative paths,10 staging/effect structural cases and10 guarded ends pass. Full UI/effect semantics and native display remain separate.')
