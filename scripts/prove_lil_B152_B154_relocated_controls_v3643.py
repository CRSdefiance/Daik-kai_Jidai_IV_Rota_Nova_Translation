"""Bind relocated speech/conditions/UI/pictures/pause and source-exact effect ownership."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.map_lil_B122_B127_source_v3260c import control2000
from scripts.prepare_lil_B152_B154_research_v3640 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B154_relocated_controls_v3643')
DOC=Path('translations/lil_B152_B154_editorial_manuscript_v6.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);packet=read(doc['source_context']);dispatchproof=read(doc['control_contract']);controls=read(doc['source_effect_and_predicate_contract']);old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks for p in [PARENT,ROM]];assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dispatchproof['source_owned_adapters'].items():exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](NdsImage.open(ROM));ROOT.mkdir(parents=True);ctx=CurrentContext(dispatchproof['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context');rows={r['id']:r for r in doc['records']};dispatches=[];predicates=[];uis=[];pictures=[];pauses=[];leaves=[]
    for b in plan['blocks']:
        n=b['block'];assert sha(new[n])==b['research_block_sha256'] and sha(old[n])==b['source_block_sha256']
        for r in b['text_records']:
            value=bytes.fromhex(r['target_hex']);assert new[n][r['new_offset']:r['new_offset']+len(value)]==value;result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==rows[r['id']]['source_selector'] and result['registered_catalog_match'] is None;expected=value[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert result['boundaries'][1]['text_hex']==expected.hex();dispatches.append(dict(id=r['id'],block=n,new_offset=r['new_offset'],stored_target_hex=value.hex(),**result))
        for c in b['command_map']:
            word=c['word']
            if word in [0x4000,0x100,0x200,0x300,0x400]:continue
            previous=old[n][c['old_offset']:c['old_offset']+c['old_extent']];value=new[n][c['new_offset']:c['new_offset']+c['new_extent']];assert previous==value;leaves.append(dict(block=n,word=word,old_offset=c['old_offset'],new_offset=c['new_offset'],source_current_target_hex=value.hex()));command=dict(offset=c['new_offset'],word=word,native_extent=c['new_extent'],whole_command_hex=value.hex())
            if word==0x8000:
                result=ctx.execute(probe,new[n],command);ctx.machines.pop();before=next(p for p in controls['source_predicate_cases'] if p['block']==n and p['offset']==c['old_offset']);assert result['native_result']==before['native_result'] and result['original_event_completion_calls']==before['original_event_completion_calls'];predicates.append(dict(block=n,current_source_case=before,relocated_case=result))
            elif word==0xC200:
                result=ctx.execute(C200,new[n],command);ctx.machines.pop();pair=next(p for p in controls['source_C200_pairs'] if p['block']==n and p['source_offset']==c['old_offset']);before=next(p for p in pair['cases'] if p['version']=='current');assert result['native_result']==before['native_result'] and result['source_owned_UI_writes']==before['source_owned_UI_writes'] and result['source_owned_UI_request_words']==before['source_owned_UI_request_words']==[1,0,13,0,0,0,1];uis.append(dict(block=n,current_source_case=before,relocated_case=result))
            elif word in [0x4821,0x4822,0x4823,0x4700]:
                result=ctx.execute(picture,new[n],command);ctx.machines.pop();pair=next(p for p in controls['source_picture_pairs'] if p['block']==n and p['source_offset']==c['old_offset']);before=next(p for p in pair['cases'] if p['version']=='current');a=before['original_picture_boundary_calls'];z=result['original_picture_boundary_calls']
                if word==0x4700:
                    assert a[0]['args'][3]==0x02660000+c['old_offset'] and z[0]['args'][3]==0x02660000+c['new_offset'];a=[{**a[0],'args':a[0]['args'][:3]+[0x02660000]}];z=[{**z[0],'args':z[0]['args'][:3]+[0x02660000]}]
                assert a==z and result['native_result']==before['native_result'];pictures.append(dict(block=n,current_source_case=before,relocated_case=result,carried_R3_cursor_mapped_when_hide=True))
            elif word==0x2000:
                result=control2000(NdsImage.open(ROM).read_file('/__arm9__.bin'),command);before=controls['source2000_pause_and_resume'][0];assert result==before['cases'];mapping=b['original2000_pause_and_resume_maps'];assert len(mapping)==1 and mapping[0]['new_offset']==c['new_offset'] and mapping[0]['target_resume']==c['new_offset']+2;pauses.append(dict(block=n,cases=result,source_resume=before['next_source_instruction_offset'],target_resume=mapping[0]['target_resume'],full_UI_body_and_input_not_executed=True))
    assert (len(dispatches),len(predicates),len(uis),len(pictures),len(pauses),len(leaves))==(59,2,3,5,1,37) and not ctx.machines;assert sum(c['word']==0xA000 for c in leaves)==5 and sum(c['word']&0xFF00==0x6300 for c in leaves)==7
    evidence=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)];save(ROOT/'all59_dispatches_two_predicates_three_C200_five_pictures_and_pause.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),relocated_dispatch_cases=dispatches,relocated_predicate_pairs=predicates,relocated_C200_pairs=uis,relocated_picture_pairs=pictures,relocated_pause_cases=pauses,all37_source_current_target_nonrelative_nonspeech_leaves=leaves,all59_progressive_consumers_eight_static_actors_FI3_FA1_exact=True,all_five_A000_and_seven630x_and_opaque_operands_source_exact=True,all70_resource_boundary_cases_reused_by_same_exact_word_runtime_and_dispatch=True,resource_UI_picture_pause_and_A000_bodies_not_fully_executed=True,hide_R3_source_cursor_maps_from526_to560=True,registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in evidence},actual_selected_B152_B154_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False));print('59 relocated dispatches,2predicates,3C200,5pictures,10pause cases pass;all37 opaque leaves exact. No gameplay/effect-body claim.')
