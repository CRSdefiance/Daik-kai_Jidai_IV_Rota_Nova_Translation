"""Prepare a source-locked compiler for ten raw predicates and one Boolean query."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_compiler_tools_v3449');a=Path('dk4tool/patch/lil_B137_editorial_v2.py');b=Path('dk4tool/patch/lil_B138_editorial_v1.py');assert not root.exists() and not b.exists()
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert read('out/all_routes_combined_v3416_candidate.manifest.json')['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    t=a.read_text(encoding='utf-8')
    replacements=[('lil_B137_layout_v3','lil_B138_layout_v2'),('lil_B137','lil_B138'),('B137','B138'),('[137]','[138]'),('all117_physical_nested_command_boundaries_and48_relative_sites_verified','all111_physical_nested_command_boundaries_and45_relative_sites_verified'),('all240_relocated_relative_skip_cases_preserve_original_targets','all225_relocated_relative_skip_cases_preserve_original_targets'),('all12_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM','all10_predicates_and1_query_current_relocated_results_and_source_operands_equal'),('all48_final_planes192_macros_static_dispatches_and12_predicates_bound','all44_final_planes176_macros_static_dispatches10_predicates_and1_query_bound'),('all12_predicate_current_relocated_results_and_source_operands_equal','all10_predicates_and1_query_current_relocated_results_and_source_operands_equal'),("len(controls['relocated_predicate_pairs'])==12 and controls['original_event_queries']==[]","len(controls['relocated_predicate_pairs'])==11 and controls['original_event_queries']==mapping['original_event_queries']"),('all48','all44'),('==48','==44'),('==117','==111'),('==31','==23'),('{2,9,14,16,17,20,22,23,38,92,198}','{2,14,20,21,22,23,92}'),('48speech','44speech'),('48complete','44complete'),('48 progressive speeches;12 predicates and48 relative spans','44 progressive speeches;ten raw predicates,one event137 query and45 spans'),('all44_speeches48_relative_operands_verified','all44_speeches45_relative_operands_verified')]
    for x,y in replacements:assert x in t,x;t=t.replace(x,y)
    needle="    _require(mapping['original_event_queries']==[],'unexpected event query')";assert needle in t
    t=t.replace(needle,"    _require(len(mapping['original_event_queries'])==1 and mapping['original_event_queries'][0]['event']==137 and mapping['original_event_queries'][0]['source_command_hex']=='00818900','exact original event137 query required')")
    marker="    _require(len(native['source_consumer_negative_controls'])==23";assert marker in t
    extra="""    source_controls=load(doc['control_contract'])
    conditional=load(source_controls['source_exact_conditional_result_contract'])
    constants=conditional['scoped_expected_unforced_results']
    _require(controls['source_predicate_result_constants']==constants and constants.get('0080ffff200301a1')==2,'source raw predicate-result contract differs')
    expected_adapter='SCOPED_RESULTS='+repr(constants)+'\\n'+source_controls['source_owned_adapters']['predicate']
    _require(controls['portable_source_owned_adapters']['predicate']==expected_adapter,'portable source-specific predicate constants required')
    pairs=controls['relocated_predicate_pairs']
    _require(sum(p['word']==0x8000 for p in pairs)==10 and sum(p['word']==0x8100 for p in pairs)==1,'ten predicates andone query required')
    for pair in pairs:
        _require(len(pair['cases'])==2 and pair['source_operands_results_and_unowned_RAM_exact'],'complete source-relocated conditional pair required')
        left,right=pair['cases']
        _require(left['source_command_hex']==right['source_command_hex'] and left['native_result']==right['native_result'],'source conditional operands/results changed')
        operand=left['source_command_hex']
        _require(operand in constants and left['native_result']==[2,constants[operand],0,0,0,0],'unforced source conditional result differs')
        _require(all(p['all_unowned4MiB_actor_models_ABI_input_owner_and_output_canaries_exact'] and p['sole_scratch_restore_recovers_all4MiB_exact'] and p['no_predicate_or_event_flag_forced'] for p in pair['cases']),'conditional RAM/ABI proof differs')
        for p in pair['cases']:
            calls=p['original_event_completion_calls']
            _require((len(calls)==1 and calls[0]['args'][1]==137 and operand=='00818900') if pair['word']==0x8100 else calls==[],'original event query differs')
"""
    t=t.replace(marker,extra+marker)
    needle="_require(raw[0] in {2,14,20,21,22,23,92},'unapproved speaker:'+ident)";assert needle in t
    t=t.replace(needle,"_require(raw[0] in {2,14,20,21,22,23,92} and row['source_selector']==raw[0],'unapproved speaker:'+ident)")
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),compiler=str(b),compiler_sha256=sha(b.read_bytes()),source_static_selectors=[2,14,20,21,22,23,92],predicates=10,event_queries=1,raw_result2_operand='0080ffff200301a1',portable_source_predicate_constants_bound=True,registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_registry_or_ledger_mutation=True,full_goal_complete=False))
