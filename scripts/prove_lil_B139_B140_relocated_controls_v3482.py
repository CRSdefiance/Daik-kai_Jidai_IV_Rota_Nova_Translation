"""Prove 67 relocated dispatches,13 conditionals and the original C200 request."""
from pathlib import Path
from types import SimpleNamespace
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts import prove_lil_B139_C200_v3461e as c200_globals
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prepare_lil_B139_B140_research_v3479 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B139_B140_relocated_controls_v3482')
DOC=Path('translations/lil_B139_B140_editorial_manuscript_v6.json')
REFERENCE=Path('work/analysis/lil_B139_B140_reference_census_v3481/all146_commands52_relative_sites_and_shipped_entry_census.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,plan,reference=map(read,[DOC,PLAN,REFERENCE]);source=read(doc['source_context']);original=read(doc['control_contract'])
    contract=read(original['source_exact_conditional_result_contract']);assert sha(Path(original['source_exact_conditional_result_contract']).read_bytes())==original['source_exact_conditional_result_contract_sha256']
    constants=contract['scoped_expected_unforced_results'];assert constants==original['source_predicate_result_constants'] and constants['00818100']==0
    parent,image=NdsImage.open(PARENT),NdsImage.open(ROM);assert sha(PARENT.read_bytes())==doc['current_ROM_sha256'] and sha(ROM.read_bytes())==reference['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin') and image.read_file('/COMMON/MESFILE.DK4')==parent.read_file('/COMMON/MESFILE.DK4')
    oldblocks,newblocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [parent,image]]
    namespace={**prior.predicate.__globals__,**prior.__dict__,**c200_globals.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{},'SCOPED_RESULTS':constants};portable={}
    for name,text in original['source_owned_adapters'].items():portable[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    needed={name for name in prior.predicate.__code__.co_names if name in prior.predicate.__globals__};assert needed<=namespace.keys(),needed-namespace.keys()
    assert {'predicate','C200'}<=portable.keys();native=SimpleNamespace(**namespace);namespace['CATALOG_LOOKUP'],binding=native.bind_current_catalog(parent)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B139_B140_fonts_v3474/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    dispatches=[];conditionals=[];queries=[];UI=[];byid={r['id']:r for r in doc['records']}
    for spec in plan['blocks']:
        n=spec['block'];old,new=oldblocks[n],newblocks[n];assert n in [139,140] and sha(new)==spec['research_block_sha256'] and sha(old)==spec['source_block_sha256'] and not spec['actor_style_commands']
        for r in spec['text_records']:
            row=byid[r['id']];value=bytes.fromhex(r['target_hex']);at=r['new_offset'];assert new[at:at+len(value)]==value and new[at+len(value)]==0 and value[0]==row['source_selector']
            result=ctx.execute(native.dispatch,value[0],value[1:]);ctx.machines.pop();expected=value[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
            assert result['boundaries'][1]['text_hex']==expected.hex() and result['registered_catalog_match'] is None
            dispatches.append(dict(id=r['id'],block=n,new_offset=at,stored_target_hex=value.hex(),**result))
        for c in spec['command_map']:
            if c['word'] not in [0x8000,0x8100,0xC200]:continue
            pair=[]
            for version,block,at,extent in [('current',old,c['old_offset'],c['old_extent']),('relocated',new,c['new_offset'],c['new_extent'])]:
                command=dict(offset=at,native_extent=extent,word=c['word'],whole_command_hex=block[at:at+extent].hex());result=ctx.execute(native.C200 if c['word']==0xC200 else native.predicate,block,command);ctx.machines.pop()
                if c['word']!=0xC200:
                    calls=result['original_event_completion_calls']
                    if c['word']==0x8100:assert len(calls)==1 and calls[0]['args'][1]==129 and result['native_result'][1] in [0,1]
                    else:assert not calls
                    assert result['native_result'][1]==constants[command['whole_command_hex']]
                pair.append(dict(version=version,**result))
            assert pair[0]['native_result']==pair[1]['native_result'] and pair[0]['source_command_hex']==pair[1]['source_command_hex']
            result=dict(block=n,word=c['word'],old_offset=c['old_offset'],new_offset=c['new_offset'],cases=pair,source_operands_results_and_unowned_RAM_exact=True)
            if c['word']==0xC200:
                assert n==139 and all(p['native_extent']==2 and p['native_result'][0]==3 and p['source_owned_UI_request_words']==[1,0,13,0,0,0,1] and p['all_other4MiB_actor_roster_event_RNG_and_models_exact'] and p['native_presentation_resource_bodies_not_executed'] for p in pair)
                assert pair[0]['source_owned_UI_writes']==pair[1]['source_owned_UI_writes'] and len(pair[0]['source_owned_UI_writes'])==9;UI.append(result)
            else:conditionals.append(result)
            if c['word']==0x8100:queries.append(dict(block=n,event=129,old_offset=c['old_offset'],new_offset=c['new_offset'],source_command_hex=pair[0]['source_command_hex'],source_and_relocated_calls=[p['original_event_completion_calls'] for p in pair],original_result_unchanged=True))
    assert len(dispatches)==67 and len(conditionals)==13 and sum(c['word']==0x8000 for c in conditionals)==12 and len(queries)==len(UI)==1 and not ctx.machines
    assert all(r['source_selector']==r['resolved_actor_ID'] for r in dispatches)
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,REFERENCE,Path(doc['control_contract']),Path(original['source_exact_conditional_result_contract']),Path(original['source_C200_contract']),Path(__file__)]}
    save(ROOT/'all67_relocated_dispatches12_predicates1_query_and_C200_pairs.json',dict(candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(image.read_file('/__arm9__.bin')),evidence=evidence,relocated_dispatch_cases=dispatches,relocated_predicate_pairs=conditionals,relocated_C200_pairs=UI,all67_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text=True,no_FE_source00_or_dynamic_objects=True,all12_predicates_and1_query_current_relocated_results_and_source_operands_equal=True,original_event_queries=queries,source_predicate_result_constants=constants,portable_source_owned_adapters=portable,all_seven_static_speaker_selectors_preserved_without_role_assignment=True,current_registered_catalog_binding=binding,no_predicate_flag_event_roster_RNG_health_or_outcome_fixture=True,sole_native_unaligned_operand_scratch_restore_recovers_all4MiB=True,C200_nine_source_owned_UI_writes_exact_and_all_other4MiB_preserved=True,C200_resource_bodies_explicit_unexecuted_not_actual_transition=True,type3_only_result_word0_is_meaningful_actual_VM_tail_may_be_stale=True,original_UI_preparation_progressive_FE_bodies_unexecuted_boundaries=True,complete_native_rendering_proved_separately_not_actual_gameplay=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_selected_B139_B140_IDs=[],new_emulator_runs=0,no_ROM_registry_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('67 relocated dispatches/12 predicate pairs/query129 pair/C200 pair pass;exact source operands/results,nine UI writes and unowned RAM preserved. Resource bodies and selected scenes unexecuted.')
