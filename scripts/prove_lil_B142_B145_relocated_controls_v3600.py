"""Bind final relocated dispatches,predicates,payments,pictures and UI requests to source contracts."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B141_funds_v3537b as funds_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.prepare_lil_B142_B145_research_v3597 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_relocated_controls_v3600')
DOC=Path('translations/lil_B142_B145_editorial_manuscript_v4.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);packet=read(doc['source_context']);dispatchproof=read(doc['control_contract']);fundsproof=read(doc['source_finance_contract']);predproof=read(doc['source_predicate_contract']);effectproof=read(doc['source_effect_boundary_contract']);picturepath=Path('work/analysis/lil_B145_picture_controls_v3587/three_original_item_picture_descriptors_and_hide_eight_cases.json');pictureproof=read(picturepath);old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks for p in [PARENT,ROM]];assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dispatchproof['source_owned_adapters'].items():exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](NdsImage.open(ROM));money_namespace=dict(funds_base.__dict__)
    for name,text in fundsproof['source_owned_adapters'].items():exec(compile(text,str(Path(__file__))+'::'+name,'exec'),money_namespace)
    ROOT.mkdir(parents=True);ctx=CurrentContext(dispatchproof['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context');rows={r['id']:r for r in doc['records']};dispatches=[];predicates=[];uis=[];pictures=[];numeric=[]
    for b in plan['blocks']:
        n=b['block'];assert sha(new[n])==b['research_block_sha256'] and sha(old[n])==b['source_block_sha256']
        for r in b['text_records']:
            value=bytes.fromhex(r['target_hex']);assert new[n][r['new_offset']:r['new_offset']+len(value)]==value;result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==(None if value[0]==254 else rows[r['id']]['source_selector']) and result['registered_catalog_match'] is None;expected=value[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert result['boundaries'][1]['text_hex']==expected.hex();dispatches.append(dict(id=r['id'],block=n,new_offset=r['new_offset'],stored_target_hex=value.hex(),**result))
        for c in b['command_map']:
            if c['word'] in [0xA000,0x6301,0x630A,0x6327,0x4821,0x4822,0x4823,0x4700,0xC200,0x8000]:
                previous=old[n][c['old_offset']:c['old_offset']+c['old_extent']];value=new[n][c['new_offset']:c['new_offset']+c['new_extent']];assert previous==value;numeric.append(dict(block=n,word=c['word'],old_offset=c['old_offset'],new_offset=c['new_offset'],source_current_target_hex=value.hex()));command=dict(offset=c['new_offset'],word=c['word'],native_extent=c['new_extent'],whole_command_hex=value.hex())
                if c['word']==0x8000:
                    result=ctx.execute(probe,new[n],command);ctx.machines.pop();previous_case=next(p for p in predproof['cases'] if p['block']==n and p['source_command_hex']==value.hex());assert result['native_result']==previous_case['native_result'] and result['original_event_completion_calls']==previous_case['original_event_completion_calls'];predicates.append(dict(block=n,current_source_case=previous_case,relocated_case=result))
                elif c['word']==0xC200:
                    result=ctx.execute(C200,new[n],command);ctx.machines.pop();previous_case=next(p for p in effectproof['source_C200_cases'] if p['block']==n and p['version']=='current');assert result['native_result']==previous_case['native_result'] and result['source_owned_UI_writes']==previous_case['source_owned_UI_writes'] and result['source_owned_UI_request_words']==previous_case['source_owned_UI_request_words']==[1,0,13,0,0,0,1];uis.append(dict(block=n,current_source_case=previous_case,relocated_case=result))
                elif c['word'] in [0x4821,0x4822,0x4823,0x4700]:
                    result=ctx.execute(picture,new[n],command);ctx.machines.pop();previous_case=next(p for p in pictureproof['cases'] if p['version']=='current' and p['source_command_hex']==value.hex());assert result['original_picture_boundary_calls']==previous_case['original_picture_boundary_calls'] and result['native_result']==previous_case['native_result'];pictures.append(dict(block=n,current_source_case=previous_case,relocated_case=result))
    financial=[]
    for oldcase in fundsproof['cases']:
        n=oldcase['block'];funds=oldcase['input_funds'];b=next(b for b in plan['blocks'] if b['block']==n);fixture=ctx.execute(money_namespace['finance'],funds);ctx.machines.pop();fixture.pop('raw_after');raw=bytearray(ctx.raw);struct.pack_into('<I',raw,fixture['funds_field']-0x02000000,funds);raw=bytes(raw);word=oldcase['source_payment']['source_command_hex'];c=next(c for c in b['command_map'] if old[n][c['old_offset']:c['old_offset']+c['old_extent']].hex()==word);command=dict(offset=c['new_offset'],word=c['word'],native_extent=c['new_extent'],whole_command_hex=word);payment=ctx.execute(money_namespace['payment'],new[n],command,raw=raw);ctx.machines.pop();assert payment['before_funds']==funds and payment['after_funds']==oldcase['source_payment']['after_funds'];condition=None
        if n==142:
            c=next(c for c in b['command_map'] if old[n][c['old_offset']:c['old_offset']+c['old_extent']].hex()=='0080ffff0e0001a1');command=dict(offset=c['new_offset'],word=c['word'],native_extent=c['new_extent'],whole_command_hex='0080ffff0e0001a1');condition=ctx.execute(probe,new[n],command,raw=raw);ctx.machines.pop();assert condition['native_result']==oldcase['source_predicate']['native_result']
        financial.append(dict(block=n,input_funds=funds,relocated_source_predicate=condition,relocated_payment=payment,original_source_case=oldcase,source_semantics_and_owned_money_field_exact=True))
    assert len(dispatches)==38 and len(predicates)==6 and len(uis)==2 and len(pictures)==4 and len(financial)==13 and not ctx.machines;assert sum(c['word']==0xA000 for c in numeric)==8 and sum(c['word'] in [0x6301,0x630A,0x6327] for c in numeric)==4
    save(ROOT/'all38_dispatches6_predicates13_funding_cases_two_C200_and_four_pictures.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),relocated_dispatch_cases=dispatches,relocated_predicate_pairs=predicates,relocated_C200_pairs=uis,relocated_picture_pairs=pictures,relocated_financial_boundary_cases=financial,source_current_target_numeric_controls=numeric,all38_expected_progressive_or_FE_consumers_FI_and_static_actors_exact=True,all6_source_predicates_and13_financial_cases_semantically_preserved=True,all8_A000_operands_and4_630x_sites_source_current_target_exact=True,other_six_A000_effect_bodies_not_fully_executed=True,all_C200_source_owned_UI_writes_and_unowned_RAM_preserved=True,all_original_picture_descriptors_layouts_and_hide_boundary_preserved=True,all_presentation_resource_and630x_callee_bodies_unexecuted=True,source630x30_boundary_cases_reused_by_exact_word_runtime_and_dispatch=True,all_financial_cases_offline_copied_inputs_not_earned_progression=True,registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,Path(doc['control_contract']),Path(doc['source_finance_contract']),Path(doc['source_predicate_contract']),Path(doc['source_effect_boundary_contract']),picturepath,Path(__file__)]},actual_selected_B142_B145_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False));print('38 relocated dispatches,6predicate pairs,13financial cases,twoC200 andfourpicture pairs pass;all8A000/four630x numeric sites exact.')
