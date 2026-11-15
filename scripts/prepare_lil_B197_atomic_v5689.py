"""Prepare positive reconstruction and semantic pre-mutation negatives for B197."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_atomic_tools_v5689')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/validate_lil_B196_atomic_v5635c.py','scripts/validate_lil_B197_atomic_v5690.py',{
        'B196':'B197','lil_B196_editorial_v3':'lil_B197_editorial_v1','lil_B196_layout_v3':'lil_B197_layout_v1','lil_B196_profile_v2':'lil_B197_profile',
        'seal_lil_B196_references_v5631':'seal_lil_B197_references_v5687',
        'atomic_v5635c':'atomic_v5690','combined_v5580':'combined_v5637','reference_approval_v5631':'reference_approval_v5687',
        'native_approval_v5612/all36':'native_approval_v5670/all24','verification_v5633':'verification_v5675',
        "len(proof['changed_records'])==36":"len(proof['changed_records'])==24",'positive_records=36':'positive_records=24',
        "('FI-changed-to-literal-name',str(DOC),lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english='{SPEAKER:FE}Lil: Charm +1!'))":
        "('invented-FI-in-literal-Ian-notice',str(DOC),lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english='{SPEAKER:FE}{MACRO:FI}: Charm +1!'))",
        "('R74-ordinary-boundary-approval-lost',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74)['reviewed_ordinary_boundaries'].pop())":
        "('R74-ordinary-wrap-waiver-lost',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74)['qa_waivers'].pop())",
        "('offline-conditional-claimed-as-gameplay',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74).update(actual_B22_display_fixture_observed=True))":
        "('actual-speech-claimed-offline',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74).update(actual_B22_display_fixture_observed=False))",
        'command_offset=582':'command_offset=264',"typed_target_object_hex='00210000'":"typed_target_object_hex='00220000'",
        'source_logical_end=1816':'source_logical_end=880','research_logical_end=1666':'research_logical_end=1000',
        "lambda v:v['blocks'][0]['choice_commands'][0]['label_references'][0].update(new_offset=204)":
        "lambda v:v['blocks'][0]['choice_commands'][0]['label_references'][0].update(new_offset=v['blocks'][0]['choice_commands'][0]['label_references'][0]['new_offset']+1)",
        'source_offset=366':'source_offset=876','target_offset=318':'target_offset=1000',
        'current_final_stored_macro_alignment_cases=92':'current_final_stored_macro_alignment_cases=80',
        'fresh_count_calls=10':'fresh_count_calls=1',
        "('missing-relocated-predicate',doc['relocated_control_proof'],lambda v:v['relocated_unforced_predicates'].pop())":
        "('missing-relocated-picture-pair',doc['relocated_control_proof'],lambda v:v['picture_and47xx_current_relocated_pairs'].pop())",
        'all37_source_current_target_nonrelative_nonspeech_nonchoice_leaves':'all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves',
        "('invented-all-six-Buy-gameplay',doc['representative_proof'],lambda v:v.update(actual_buy_menu_offsets=owned.MENUS))":
        "('lost-actual-delegation-index',doc['representative_proof'],lambda v:v.update(actual_original_menu_indices=[0,1]))",
        "('wrong-record-specific-word-count',doc['source_bound_wrap_retention_proof'],lambda v:v.update(paragraph_words=22))":
        "('wrong-R74-exact-wrap-rows',doc['source_bound_wrap_retention_proof'],lambda v:v['visible_rows'].pop())",
        "('missing-wrap-nontransfer-case',doc['source_bound_wrap_retention_proof'],lambda v:v['six_source_or_prose_changes_do_not_inherit_review'].pop())":
        "('weak-wrap-waiver-transferred-to-R5',str(DOC),lambda v:v['records'][0].update(qa_waivers=['weak-line-ending'],qa_waiver_reason='copy'))",
        "('wrong-FI-expansion',doc['actor_terminology_reconciliation'],lambda v:v.update(current_source_FI_expansion='Rafael'))":
        "('wrong-Ian-notice-name',str(DOC),lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english='{SPEAKER:FE}Rafael: Charm +1!'))",
        'fresh6_actor_names':'fresh2_actor_names','six_source_prices_match_six_exact_native_payment_amounts':'source8500_price_matches_exact_native_payment_amount',
        '    for flag in FLAGS:mutations.append':
        "    mutations += [\n        ('lost-postscene-difference-honesty',doc['postscene_native_state_proof'],lambda v:v.update(broad_postscene_equivalence_unproven_and_not_substituted_for_source_control_display_and_return_checks=False)),\n        ('lost-source-portrait-baseline',doc['postscene_native_state_proof'],lambda v:v.update(source_matched_blank_portrait_name_additional_records=[])),\n        ('lost-focused-visible-Pass-proof',doc['postscene_native_state_proof'],lambda v:v.update(initial_menu_sampling_failure_resolved_by16_new_complete_active_highlight_holds_without_retiming=False)),\n        ('lost-timing-difference',load_path,lambda v:v['command_timing_differences'].pop()),\n        ('lost-world-RGB-difference',load_path,lambda v:v['later_whole_RGB_differences'].pop()),\n        ('lost-47xx-mapped-stream-pointer-proof',doc['relocated_control_proof'],lambda v:v.update(original47xx_R3_is_exact_mapped_stream_instruction_pointer=False))]\n    for flag in FLAGS:mutations.append"})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_positive_and_negatives.json',dict(tool=tool,
        exact_typed_object_offsets_lengths_indices_source_commands_and_single_mutation_guards_tested=True,
        exact_R74_waiver_nontransfer_and_source_portrait_timing_RGB_scope_honesty_negatives_added=True,
        no_ROM_or_registry_or_ledger_change=True,full_goal_complete=False))
