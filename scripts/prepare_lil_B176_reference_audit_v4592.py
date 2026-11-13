"""Derive the independent integration-ready ledger and source-reference audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B176_reference_audit_tools_v4592')
assert not root.exists()
source=Path('scripts/verify_editorial_handoff_v4538.py')
text=source.read_text(encoding='utf-8')
start=text.index("    assert len(visual['all6_actual_sheets_viewed'])")
end=text.index('    receipt=read(',start)
old_visual=text[start:end]
new_visual="""    assert len(visual['all2_actual_sheets_viewed'])==2 and all(s['viewed'] for s in visual['all2_actual_sheets_viewed'])
    assert len(visual['paired_full_screen_views'])==2 and all(s['viewed'] for s in visual['paired_full_screen_views'])
    assert sum(len(s['frames'])*2 for s in visual['paired_full_screen_views'])==8
    assert len(visual['all115_sampled_nontext_region_checks'])==visual['nontext_equal_samples']==115
    assert not visual['nontext_difference_samples'] and not visual['actual_timing_differences']
    assert visual['all10_complete_held_planes_and_source_paired_regions_match'] and visual['source_A0008_C200384_single_end386_actually_executed']
    assert visual['all_sampled_whole_RGB_from5290_through9001_equal'] and visual['whole_RGB_final9001_equal']
    assert all(visual['postscene9001_native_component_equality'].values()) and visual['postscene9001_whole1A04_actor_models_and_captain2_equal']
    assert visual['PRNG_equality'] and visual['postscene9001_PRNG_seeds']==[403514907,403514907]
    assert visual['future_world_equivalence_and_full_RAM_equality_not_claimed']
    assert visual['all_content_jobs_terminal'] and all(r['exit_code']==0 for r in visual['reaped_tool_sessions'])
    assert visual['following_B120_offset606_in_progress_at_end_adds_no_editorial_credit']
    assert len(control['relocated_A000_structural_pairs'])==1
"""
start=text.index("    save(ROOT/'verified_handoff.json'")
old_tail=text[start:]
new_tail="""    save(ROOT/'verified_handoff.json',dict(checkpoint='V4591',ledger_sha256=sha(lp.read_bytes()),fresh_reread=5875,integrated=5865,pending=10,
        source_prose=5878,revised=3728,retained=2137,new_source_prose_reviews=0,new_completed_records=0,
        all_prior_ledger_values_history_counts_and_wider_scope_preserved=True,all10_actual_and5_retained_prose_unchanged=True,
        all13_commands_single_end10_relocated_dispatches40_stored_cases_and2_end_decodes_bound=True,
        actual10_panels9_progressive1_impersonal_FE_A000_C200_single_end_and_town_return_approved=True,
        all115_nontext_samples_and_all22_command_timings_equal=True,
        final9001_whole_RGB_components_actor_captain_and_PRNG_equal=True,
        no_natural_event_eligibility_earned_state_earlier_location_full_RAM_future_world_or_hardware_claim=True,
        all_jobs_terminal=True,main_V4541_registry_builder_and_pins_preserved=True,full_goal_active=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('V4591 independently audited:ten actual/ref-approved pending;all history/counts/main V4541 preserved. Registered compiler/integration next.')
"""
tool=derive(source,'scripts/verify_editorial_handoff_v4592.py',{
    'B175':'B176','lil_B175':'lil_B176',
    'checkpoint_lil_B175_references_v4537':'checkpoint_lil_B176_references_v4591',
    'editorial_handoff_verification_v4538':'editorial_handoff_verification_v4592',
    'unfinished_editorial_scope_v4537':'unfinished_editorial_scope_v4591',
    'lil_B175_reference_reconciliation_v4537':'lil_B176_reference_reconciliation_v4591',
    'unfinished_editorial_scope_v4519':'unfinished_editorial_scope_v4573',
    'B175_reference_and_actual_coverage_v4537':'B176_reference_and_actual_coverage_v4591',
    '==(5833,5868,3709,2124)':'==(5865,5878,3728,2137)',
    '==(5865,5833,32)':'==(5875,5865,10)',
    "len(doc['records'])==32":"len(doc['records'])==10",
    "=={'revise':19,'retain-wording':13}":"=={'revise':5,'retain-wording':5}",
    "b['actual_complete_native_panels']==32":"b['actual_complete_native_panels']==10",
    '==(4266,4234)':'==(4276,4266)',
    "scope['incomplete_route_source_prose']==32":"scope['incomplete_route_source_prose']==10",
    "scope['remaining_B176_B180_physical_speeches']==58":"scope['remaining_B177_B180_physical_speeches']==48",
    "block['block']==175 and len(block['command_map'])==39 and len(block['text_records'])==32":
        "block['block']==176 and len(block['command_map'])==13 and len(block['text_records'])==10",
    '==[(1702,1690),(1706,1694)]':'==[(386,400)]','.blocks[175]':'.blocks[176]',
    '==(1712,1700)':'==(392,404)','==(128,68,60)':'==(40,16,24)',
    "len(control['relocated_dispatch_cases'])==32":"len(control['relocated_dispatch_cases'])==10",
    "sum(r['resolved_actor_ID'] is None for r in control['relocated_dispatch_cases'])==9":
        "sum(r['resolved_actor_ID'] is None for r in control['relocated_dispatch_cases'])==1",
    "len(control['all7_source_current_target_nonrelative_nonspeech_leaves'])==7":
        "len(control['all3_source_current_target_nonrelative_nonspeech_leaves'])==3",
    "len(ends['cases'])==4":"len(ends['cases'])==2",old_visual:new_visual,
    "promoted['profile']=='all-routes-unified-v4496'":"promoted['profile']=='all-routes-unified-v4541'",
    '# Current editorial handoff - V4537':'# Current editorial handoff - V4591',old_tail:new_tail,
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,source_prose_or_completion_credit_added=0,full_goal_complete=False))
