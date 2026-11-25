"""Create a guarded two-block compiler including the exact C200 source contract."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('dk4tool/patch/lil_B138_editorial_v1.py');b=Path('dk4tool/patch/lil_B139_B140_editorial_v1.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    changes=[
      ('Source/runtime-locked44 progressive speeches;ten raw predicates,one event137 query and45 spans.','Source/runtime-locked67 progressive speeches;twelve predicates,query129,C200 and52 spans.'),
      ('lil_B138','lil_B139_B140'),('Lil B138','Lil B139/B140'),('dk4-lil-B138','dk4-lil-B139-B140'),('BLOCKS=[138]','BLOCKS=[139,140]'),
      ('all111_physical_nested_command_boundaries_and45_relative_sites_verified','all146_physical_nested_command_boundaries_and52_relative_sites_verified'),('all225_relocated_relative_skip_cases','all260_relocated_relative_skip_cases'),('all10_predicates_and1_query_current_relocated_results_and_source_operands_equal','all12_predicates_and1_query_current_relocated_results_and_source_operands_equal'),('all44_active_speech_targets_preserved','all67_active_speech_targets_preserved'),
      ("['event']==137","['event']==129"),('00818900','00818100'),('event137','event129'),('all44_final_planes176_macros_static_dispatches10_predicates_and1_query_bound','all67_final_planes268_macros_static_dispatches12_predicates1_query_and_C200_bound'),('all44_final_stored_paragraphs','all67_final_stored_paragraphs'),("len(controls['relocated_predicate_pairs'])==11","len(controls['relocated_predicate_pairs'])==13"),
      ("constants.get('0080ffff200301a1')==2","constants==source_controls['source_predicate_result_constants'] and constants.get('00818100')==0"),('source raw predicate-result contract differs','source predicate-result contract differs'),("expected_adapter='SCOPED_RESULTS='+repr(constants)+'\\n'+source_controls['source_owned_adapters']['predicate']","expected_adapter=source_controls['source_owned_adapters']['predicate']"),
      ("sum(p['word']==0x8000 for p in pairs)==10","sum(p['word']==0x8000 for p in pairs)==12"),('ten predicates andone query','twelve predicates andone query'),("calls[0]['args'][1]==137","calls[0]['args'][1]==129"),('{2,14,20,21,22,23,92}','{2,4,9,16,20,21,171}'),
      ("len(doc['records'])==len(refs)==44","len(doc['records'])==len(refs)==67"),("len(fonts)==44","len(fonts)==67"),('44speech coverage','67speech coverage'),('44complete native cases','67complete native cases'),('two choice labels required','no choice labels allowed'),('one exact block required','two exact blocks required'),('sum(expected_commands.values())==111','sum(expected_commands.values())==146'),("len(changes)==len({r['id'] for r in changes})==44","len(changes)==len({r['id'] for r in changes})==67"),('only_SC2_selected_one_block_changed','only_SC2_selected_two_blocks_changed'),('all335_other_SC2_blocks','all334_other_SC2_blocks'),('all44_speeches45_relative_operands','all67_speeches52_relative_operands'),('all44_progressive_consumers','all67_progressive_consumers')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    anchor="    _require(len(native['source_consumer_negative_controls'])==23"
    assert t.count(anchor)==1
    extra='''    _require(mapping.get('all1_C200_current_relocated_source_owned_UI_writes_and_unowned_RAM_equal') is True,'C200 source-owned request approval required')
    _require(controls['portable_source_owned_adapters'].get('C200')==source_controls['source_owned_adapters']['C200'],'portable C200 adapter differs')
    ui=controls.get('relocated_C200_pairs',[])
    _require(len(ui)==1 and ui[0]['block']==139 and ui[0]['word']==0xC200 and len(ui[0]['cases'])==2,'one complete C200 source-relocated pair required')
    source_ui=load(source_controls['source_C200_contract'])['cases'][0]
    for p in ui[0]['cases']:
        _require(p['source_command_hex']=='00c2' and p['native_extent']==2 and p['native_result'][0]==3,'C200 source extent/result type differs')
        _require(p['source_owned_UI_request_words']==source_ui['source_owned_UI_request_words']==[1,0,13,0,0,0,1] and p['source_owned_UI_writes']==source_ui['source_owned_UI_writes'] and len(p['source_owned_UI_writes'])==9,'C200 exact source-owned queue/flag writes differ')
        _require(p['all_other4MiB_actor_roster_event_RNG_and_models_exact'] and p['original_input_owner_guards_and_ABI_exact'] and p['native_presentation_resource_bodies_not_executed'] and p['resource_call_returns_are_unused_by_original_continuation'],'C200 source-owned/unexecuted resource boundary contract differs')
    ui_command=next(c for block in mapping['blocks'] if block['block']==139 for c in block['mapped_native_commands'] if c['word']==0xC200)
    _require(ui[0]['old_offset']==ui_command['old_offset'] and ui[0]['new_offset']==ui_command['new_offset'] and all(ui_command[k]==2 for k in ['old_native_extent','new_native_extent']),'C200 mapped source boundary differs')
    actual=load(representative['shared_C200_actual_representative'])
    _require(actual['shared_C200_result3_extent2_and_normal_return_behavior_class_has_actual_evidence'] and actual['current_offline_two_resource_bodies_remain_unexecuted'] and actual['actual_B24_gameplay_is_historical_and_not_selected_B139_B140'],'C200 scoped actual representative binding required')
'''
    t=t.replace(anchor,extra+anchor);compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B139_B140_compiler_tools_v3485');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),exact_C200_source_owned_UI_writes_and_actual_behavior_class_required=True,type3_only_first_word_semantic=True,producer_sha256=sha(Path(__file__).read_bytes()),all_prior_artifacts_preserved=True,full_goal_complete=False))
