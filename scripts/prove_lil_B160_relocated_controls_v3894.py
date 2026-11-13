"""Bind22 relocated consumers,five predicates,C283/C200 and12 exact leaves."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.prepare_lil_B160_research_v3890b import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B160_relocated_controls_v3894')
DOC=Path('translations/lil_B160_editorial_manuscript_v4.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan=map(read,[DOC,PLAN]);packet=read(doc['source_context']);dp=read(doc['control_contract']);cp=read(doc['source_effect_and_predicate_contract']);old,new=[IlnkContainer.parse(NdsImage.open(p).read_file('/data/SC2.DK4')).blocks[160] for p in [PARENT,ROM]];assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256'];namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dp['source_owned_adapters'].items():exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](NdsImage.open(ROM));ROOT.mkdir(parents=True);ctx=CurrentContext(dp['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context');rows={r['id']:r for r in doc['records']};dispatches=[];predicates=[];leaves=[];uis=[];assert len(plan['blocks'])==1;b=plan['blocks'][0];assert sha(new)==b['research_block_sha256'] and sha(old)==b['source_block_sha256']
    for r in b['text_records']:
        v=bytes.fromhex(r['target_hex']);assert new[r['new_offset']:r['new_offset']+len(v)]==v;result=ctx.execute(namespace['dispatch'],v[0],v[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==(None if v[0]==254 else rows[r['id']]['source_selector']) and result['registered_catalog_match'] is None;expected=v[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.');assert result['boundaries'][1]['text_hex']==expected.hex();dispatches.append(dict(id=r['id'],block=160,new_offset=r['new_offset'],stored_target_hex=v.hex(),**result))
    for c in b['command_map']:
        if c['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        previous=old[c['old_offset']:c['old_offset']+c['old_extent']];v=new[c['new_offset']:c['new_offset']+c['new_extent']];assert previous==v;leaves.append(dict(block=160,word=c['word'],old_offset=c['old_offset'],new_offset=c['new_offset'],source_current_target_hex=v.hex()))
        if c['word']==0x8000:
            command=dict(offset=c['new_offset'],word=c['word'],native_extent=c['new_extent'],whole_command_hex=v.hex());result=ctx.execute(probe,new,command);ctx.machines.pop();before=next(p for p in cp['source_predicate_cases'] if p['offset']==c['old_offset']);assert result['native_result']==before['native_result'] and result['original_event_completion_calls']==before['original_event_completion_calls'];predicates.append(dict(block=160,current_source_case=before,relocated_case=result))
        if c['word']==0xC200:
            command=dict(offset=c['new_offset'],word=c['word'],native_extent=c['new_extent'],whole_command_hex=v.hex());result=ctx.execute(C200,new,command);ctx.machines.pop();before=next(p for p in cp['source_C200_pairs'] if p['source_offset']==c['old_offset'])['cases'][1];assert result['source_owned_UI_writes']==before['source_owned_UI_writes'] and result['source_owned_UI_request_words']==before['source_owned_UI_request_words']==[1,0,13,0,0,0,1];uis.append(dict(block=160,current_source_case=before,relocated_case=result))
    assert len(uis)==1
    assert len(dispatches)==22 and len(predicates)==5 and len(leaves)==12 and not ctx.machines;assert sum(c['word']==0xA000 for c in leaves)==0 and sum(c['word']&0xFF00==0x6300 for c in leaves)==3 and sum(c['word']==0 for c in leaves)==2;paths=[DOC,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)];save(ROOT/'all22_dispatches_five_predicates_C200_and12_source_exact_leaves.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),relocated_dispatch_cases=dispatches,relocated_predicate_pairs=predicates,relocated_C200_pairs=uis,all12_source_current_target_nonrelative_nonspeech_leaves=leaves,all22_progressive_consumers_six_static_actors_FI1_exact=True,all_five_unforced_predicates_match_source_results=True,source_no_A000_three630x_C283_C200_no_pause_FE_all_leaves_and_twoends_exact=True,all30_resource_boundary_cases_reused_by_exact_words_runtime_and_dispatch=True,resource_presentation_and_A000_bodies_not_fully_executed=True,registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in paths},actual_selected_B160_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_orcompletion_change=True,full_goal_complete=False));print('22 relocated consumers/five unforced predicates/one C200 pass;all12 numeric/nontext leaves exact. No actual eligibility or effect-body claim.')
