"""Prepare an independent final pending-reference/history audit for B178."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_reference_audit_tools_v4698');assert not ROOT.exists()
source=Path('scripts/verify_editorial_handoff_v4592.py');text=source.read_text(encoding='utf-8')
a=text.index("    assert len(visual['all2_actual_sheets_viewed'])");b=text.index("    receipt=read(CHECKPOINT/",a)
visual="""    assert len(visual['all3_actual_sheets_viewed'])==3 and all(s['viewed'] for s in visual['all3_actual_sheets_viewed'])
    assert len(visual['paired_full_screen_views'])==4 and all(s['viewed'] for s in visual['paired_full_screen_views'])
    assert sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==16
    assert len(visual['all115_sampled_nontext_region_checks'])==visual['nontext_equal_samples']==115
    assert not visual['nontext_difference_samples'] and len(visual['actual_timing_differences'])==14
    assert visual['exact_timing_difference_counts']=={'total':14,'speech':12,'control_or_end':2}
    assert visual['all13_complete_held_planes_and_source_paired_regions_match'] and visual['source_A0008_C200488_single_end490_actually_executed']
    assert visual['sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames'] and visual['whole_RGB_final9001_equal']
    differences=visual['sampled_postscene_whole_RGB_differences_unmasked']
    assert [(r['frame'],r['whole_frame_difference_bbox']) for r in differences]==[
        (6970,[224,360,240,371]),(7150,[224,360,240,371]),(7930,[224,360,240,376]),(8110,[224,360,240,376])]
    assert visual['all_four_following_indicator_differences_viewed_in_full_and_retained']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[3306586022,3306586022]
    assert visual['fixture_return_frames']==[5977,5976] and visual['no_new_PRNG_causal_trace']
    assert visual['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert visual['all_content_jobs_terminal'] and all(r['exit_code']==0 for r in visual['reaped_tool_sessions'])
    assert visual['following_scene_adds_no_editorial_credit'] and len(control['relocated_A000_structural_pairs'])==1
"""
tool=derive(source,'scripts/verify_editorial_handoff_v4698.py',{
    text[a:b]:visual,
    'checkpoint_lil_B176_references_v4591':'checkpoint_lil_B178_references_v4697',
    'editorial_handoff_verification_v4592':'editorial_handoff_verification_v4698',
    'unfinished_editorial_scope_v4591':'unfinished_editorial_scope_v4697',
    'lil_B176_reference_reconciliation_v4591':'lil_B178_reference_reconciliation_v4697',
    '(5865,5878,3728,2137)':'(5885,5901,3738,2147)','(5875,5865,10)':'(5898,5885,13)',
    "len(doc['records'])==10":"len(doc['records'])==13","=={'revise':5,'retain-wording':5}":"=={'revise':2,'retain-wording':11}",
    "b['actual_complete_native_panels']==10":"b['actual_complete_native_panels']==13",
    '(4276,4266)':'(4299,4286)',
    'unfinished_editorial_scope_v4573':'unfinished_editorial_scope_v4679',
    "scope['incomplete_route_source_prose']==10 and scope['remaining_B177_B180_physical_speeches']==48":
        "scope['incomplete_route_source_prose']==13 and scope['remaining_B179_B180_physical_speeches']==25",
    'B176_reference_and_actual_coverage_v4591':'B178_reference_and_actual_coverage_v4697',
    "block['block']==176 and len(block['command_map'])==13 and len(block['text_records'])==10":
        "block['block']==178 and len(block['command_map'])==16 and len(block['text_records'])==13",
    '==[(386,400)]':'==[(490,452)]','blocks[176]':'blocks[178]','==(392,404)':'==(496,456)',
    '==(40,16,24)':'==(52,28,24)',"len(control['relocated_dispatch_cases'])==10":"len(control['relocated_dispatch_cases'])==13",
    "promoted['profile']=='all-routes-unified-v4541'":"promoted['profile']=='all-routes-unified-v4595'",
    "assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']==ledger['current_integrated_candidate']['sha256']":
        "assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']\n    assert ledger['current_integrated_candidate']['profile']=='all-routes-unified-v4655'\n    assert sha(Path(ledger['current_integrated_candidate']['path']).read_bytes())==ledger['current_integrated_candidate']['sha256']",
    '# Current editorial handoff - V4591':'# Current editorial handoff - V4697',
    "checkpoint='V4591'":"checkpoint='V4697'",
    'fresh_reread=5875,integrated=5865,pending=10':'fresh_reread=5898,integrated=5885,pending=13',
    'source_prose=5878,revised=3728,retained=2137':'source_prose=5901,revised=3738,retained=2147',
    'all10_actual_and5_retained_prose_unchanged':'all13_actual_and11_retained_prose_unchanged',
    'all13_commands_single_end10_relocated_dispatches40_stored_cases_and2_end_decodes_bound':
        'all16_commands_single_end13_relocated_dispatches52_stored_cases_and2_end_decodes_bound',
    'actual10_panels9_progressive1_impersonal_FE_A000_C200_single_end_and_town_return_approved':
        'actual13_panels12_progressive1_impersonal_FE_A000_C200_single_end_and_parent_return_approved',
    'all115_nontext_samples_and_all22_command_timings_equal':
        'all115_upper_name_portrait_samples_equal_14_timings_and4_indicator_differences_retained',
    'final9001_whole_RGB_components_actor_captain_and_PRNG_equal':
        'final9001_RGB_five_components_actor_captain_and_PRNG3306586022_equal',
    'main_V4541_registry_builder_and_pins_preserved':'main_V4595_registry_builder_and_pins_preserved',
    'Independently audit sealed B176':'Independently audit sealed B178',
    'V4591 independently audited:ten actual/ref-approved pending;all history/counts/main V4541 preserved.':
        'V4697 independently audited:thirteen actual/ref-approved pending;all history/counts/main V4595 preserved.',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,full_root_and_nested_history_preserved=True,
    source_current_stored_references_and11_retentions_required=True,actual14_timings4_indicator_differences_and_equal_PRNG_bound=True,
    no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
