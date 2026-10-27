"""Adapt the reviewed original native functions to relocated active Lil targets."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    old=Path('scripts/prove_lil_shrines_relocated_controls_v3197.py');new=Path('scripts/prove_lil_B111_B119_relocated_controls_v3243b.py')
    root=Path('work/analysis/lil_B111_B119_control_tools_v3243');assert not new.exists() and not root.exists()
    t=old.read_text(encoding='utf-8')
    swaps={
        'import struct':'import struct\nfrom types import SimpleNamespace',
        'prove_lil_shrines_temples_controls_v3168c as native':'prove_lil_shrines_temples_controls_v3168c as prior',
        'prepare_lil_shrines_research_v3194':'prepare_lil_B111_B119_research_v3240b',
        'lil_Shrines_Temples_relocated_controls_v3197':'lil_B111_B119_relocated_controls_v3243b',
        'lil_shrines_temples_editorial_manuscript_v7.json':'lil_B111_B119_editorial_manuscript_v5.json',
        'lil_shrines_temples_actor_style_manuscript_v5.json':'lil_B111_B119_actor_style_manuscript_v4.json',
        'lil_Shrines_Temples_reference_census_v3196/all421_commands114_relative_sites_and_shipped_entry_census.json':'lil_B111_B119_reference_census_v3242/all305_commands64_relative_sites_and_shipped_entry_census.json',
        'lil_Shrines_Temples_fonts_v3183b':'lil_B111_B119_fonts_v3234c',
        'native.CATALOG_LOOKUP,catalog_binding=native.bind_current_catalog(parent)':"namespace={**prior.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}\n    for name,text in original['source_owned_adapters'].items():\n        exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)\n    native=SimpleNamespace(**namespace)\n    namespace['CATALOG_LOOKUP'],catalog_binding=native.bind_current_catalog(parent)",
        'prefix=208 if isvoice else value[0]':"prefix=row['source_selector'] if isvoice else value[0]",
        'virtual_D0_not_stored':'actual_virtual_prefix_not_stored',
        "assert not result['original_event_completion_calls']":"assert all(q['args'][1]==319 for q in result['original_event_completion_calls'])",
        "assert pairs[0]['source_command_hex']==pairs[1]['source_command_hex']":"assert pairs[0]['source_command_hex']==pairs[1]['source_command_hex']\n            assert pairs[0]['original_event_completion_calls']==pairs[1]['original_event_completion_calls']",
        "len(dispatches)==220 and sum(c['source_selector']==254 for c in dispatches)==30":"len(dispatches)==150 and sum(c['source_selector']==254 for c in dispatches)==1",
        'len(whole)==16 and len(catalog[\'cases\'])==3312 and len(predicates)==21':"len(whole)==12 and len(catalog['cases'])==2484 and len(predicates)==16",
        "all(c['source_selector']==208 and c['resolved_actor_ID']==151 and c['original_actor_style']==4 for c in whole)":"all(c['source_selector'] in [208,209,214,215,220] and c['resolved_actor_ID']==151 and c['original_actor_style']==4 for c in whole) and {c['source_selector'] for c in whole}=={208,209,214,215,220}",
        'all3312_catalog_getter_cases_cover_every_actor_style_without_role_assignment':'all2484_catalog_getters_preserve_each_original_style_pointer_and_alias',
        'all220_dispatch16_style_commands3312_getters21_predicate_pairs.json':'all150_dispatch12_style_commands2484_getters16_predicate_query_pairs.json',
        'all220_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text':'all150_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text',
        'all30_FE_preserve_original_null_actor_before_dynamic_fallback':'one_FE_preserves_original_null_actor_before_dynamic_fallback',
        'all16_style_commands_use_unforced_D0_fallback151_style4_without_role_assignment':'all12_style_commands_use_actual_variable_source_prefix_unforced_fallback151_style4_without_role_assignment',
        'all3312_pointer_cases_and_all_source_alias_groups_preserved':'all2484_pointer_cases_and_all_source_alias_groups_preserved',
        'all21_current_relocated_predicate_results_and_source_operands_equal':'all15_predicate_and_one_query_current_relocated_results_and_source_operands_equal',
        'original_event_queries=[],':'original_event_queries=queries,canonical_Maria32_copy_not_dispatched_under_Lil_context=True,',
        'actual_selected_Shrines_Temples_IDs':'actual_selected_B111_B119_IDs',
        '220relocated dispatches/16whole actor-style commands/3312catalog pointers/21current-target predicate pairs pass. No forced roles,flags ornewgameplay.':'150relocated dispatches/12whole variable-selector commands/2484catalog pointers/15predicate andoneevent319query pairs pass. No forced roles,flags ornewgameplay.'}
    for a,b in swaps.items():assert a in t,a;t=t.replace(a,b)
    anchor="    evidence={str(p):sha(p.read_bytes())"
    assert t.count(anchor)==1
    t=t.replace(anchor,"""    queries=[dict(block=p['block'],old_offset=p['old_offset'],new_offset=p['new_offset'],event=q['args'][1],args=q['args']) for p in predicates for q in p['cases'][0]['original_event_completion_calls']]
    assert len(queries)==1 and queries[0]['block']==114 and queries[0]['old_offset']==46 and queries[0]['event']==319
"""+anchor)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');root.mkdir(parents=True)
    save(root/'relocated_native_tools_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),source_owned_native_adapters_reused_from3219=True,actual5style_prefixes_and_event319_query_explicit=True,canonical_Maria32_not_dispatched=True,no_executed_producer_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
