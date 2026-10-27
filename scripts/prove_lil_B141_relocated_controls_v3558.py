"""Bind relocated speeches,predicates,payment and unchanged numeric controls."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prove_lil_B141_funds_v3537b import finance,payment
from scripts.prove_lil_B141_controls_v3538b import control630A
from scripts.prepare_lil_B141_research_v3554 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_relocated_controls_v3558')
DOC=Path('translations/lil_B141_editorial_manuscript_v6.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);sourcepath=Path(doc['source_context']);packet=read(sourcepath);sourcecontrols=read(doc['control_contract']);image=NdsImage.open(ROM);old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[141] for p in [PARENT,ROM]];spec=plan['blocks'][0];byid={r['id']:r for r in doc['records']};namespace={**prior.__dict__,'SOURCE':sourcepath,'CATALOG_LOOKUP':{}}
    for name,text in sourcecontrols['source_owned_adapters'].items():
        if name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B141_voices_v3533/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');dispatches=[];predicates=[];ui=[]
    for r in spec['text_records']:
        value=bytes.fromhex(r['target_hex']);assert new[r['new_offset']:r['new_offset']+len(value)]==value
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==byid[r['id']]['source_selector'] and result['boundaries'][1]['text_hex']==value[1:].replace(b'FI',b'Lil').hex() and result['registered_catalog_match'] is None;dispatches.append(dict(id=r['id'],new_offset=r['new_offset'],stored_target_hex=value.hex(),**result))
    for c in spec['command_map']:
        if c['word'] not in [0x8000,0xC200]:continue
        pair=[]
        for label,block,at,extent in [('current',old,c['old_offset'],c['old_extent']),('relocated',new,c['new_offset'],c['new_extent'])]:
            command=dict(offset=at,word=c['word'],native_extent=extent,whole_command_hex=block[at:at+extent].hex());result=ctx.execute(C200 if c['word']==0xC200 else probe,block,command);ctx.machines.pop();pair.append(dict(version=label,**result))
        assert pair[0]['source_command_hex']==pair[1]['source_command_hex'] and pair[0]['native_result']==pair[1]['native_result']
        item=dict(word=c['word'],old_offset=c['old_offset'],new_offset=c['new_offset'],cases=pair)
        if c['word']==0xC200:assert pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes'] and pair[0]['source_owned_UI_request_words']==pair[1]['source_owned_UI_request_words']==[1,0,13,0,0,0,1];ui.append(item)
        else:predicates.append(item)
    money=next(c for c in spec['command_map'] if c['word']==0xA000 and old[c['old_offset']:c['old_offset']+c['old_extent']].hex()=='00a0ffffbdff0191');financial=[];reference=read(doc['source_finance_contract']);threshold=next(c for c in spec['command_map'] if old[c['old_offset']:c['old_offset']+c['old_extent']].hex()=='0080ffff0e0001a1')
    for priorcase in reference['cases']:
        funds=priorcase['input_funds'];fixture=ctx.execute(finance,funds);ctx.machines.pop();fixture.pop('raw_after');raw=bytearray(ctx.raw);struct.pack_into('<I',raw,fixture['funds_field']-0x02000000,funds);raw=bytes(raw)
        at=money['new_offset'];command=dict(offset=at,word=0xA000,native_extent=8,whole_command_hex=new[at:at+8].hex());effect=ctx.execute(payment,new,command,raw=raw);ctx.machines.pop();at=threshold['new_offset'];command=dict(offset=at,word=0x8000,native_extent=8,whole_command_hex=new[at:at+8].hex());condition=ctx.execute(probe,new,command,raw=raw);ctx.machines.pop();assert effect['after_funds']==priorcase['source_payment']['after_funds'] and condition['native_result']==priorcase['source_predicate']['native_result'];financial.append(dict(input_funds=funds,relocated_source_predicate=condition,relocated_payment=effect,source_semantics_and_owned_money_field_exact=True))
    opaque=next(c for c in spec['command_map'] if c['word']==0x630A);assert new[opaque['new_offset']:opaque['new_offset']+2]==old[opaque['old_offset']:opaque['old_offset']+2]==bytes.fromhex('0a63');original_A000=[c for c in spec['command_map'] if c['word']==0xA000];assert len(original_A000)==4 and all(old[c['old_offset']:c['old_offset']+8]==new[c['new_offset']:c['new_offset']+8] for c in original_A000)
    assert len(dispatches)==14 and len(predicates)==3 and len(ui)==1 and len(financial)==7 and not ctx.machines
    save(ROOT/'all14_dispatches3_predicates7_funding_cases_and_C200.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocated_dispatch_cases=dispatches,relocated_predicate_pairs=predicates,relocated_C200_pairs=ui,relocated_financial_boundary_cases=financial,all14_expected_progressive_consumers_and_FI_text_exact=True,all3_source_predicates_and7_monetary_cases_semantically_preserved=True,C200_nine_source_owned_writes_index0_and_all_unowned_RAM_preserved=True,opaque630A_source_current_target_bytes_and_original_boundary_exact=True,all4_A000_owned_operands_exact=True,three_other_A000_effect_bodies_not_fully_executed=True,resource_and630A_callee_bodies_unexecuted=True,all_funding_cases_offline_copied_one_word_inputs_not_earned_progression=True,registered_catalog_binding=binding,portable_source_owned_adapters={**sourcecontrols['source_owned_adapters'],'predicate':inspect.getsource(probe),'finance':inspect.getsource(finance),'payment':inspect.getsource(payment)},native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,Path(doc['source_context']),Path(doc['source_finance_contract']),Path(doc['control_contract']),Path(__file__)]},actual_selected_B141_IDs=[],new_emulator_runs=0,no_ROM_registry_orcompletion_change=True,full_goal_complete=False))
    print('14 relocated dispatches,3 predicate pairs,7 million-threshold/900000-payment cases and C200 pair pass;all other numeric operands exact.')
