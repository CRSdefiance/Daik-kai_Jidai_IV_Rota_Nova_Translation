"""Derive a history-preserving, once-only completion producer for B202."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

GATES='''def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all590_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V5947']
    assert start['all_current_requested_and_final_framebuffers_equal_V5947'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==69 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    assert (actual['actual_unique_speech_panels'],actual['complete_matching_observations'],actual['complete_matching_holds'])==(19,19,74) and not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_source_indices']
    assert actual['all26_source_commands_and9_initializers_stored'] and actual['same_observed_source_path_original_results_no_predicates_and_end582']
    assert transitions['no_open_translation_specific_display_control_or_return_finding'] and not transitions['visual_review_pending'] and len(transitions['viewed_sheets'])==6
    assert transitions['source_English_exit_frames']==[7657,7655] and transitions['command_timing_differences']==22 and transitions['later_prompt_differences']==21 and transitions['all_later_differences_bounded_to_advance_prompt']
    state=read(transitions['measured_state_proof']);assert sha(Path(transitions['measured_state_proof']).read_bytes())==transitions['measured_state_proof_sha256']
    assert len(state['actual_command_duration_changes'])==3 and len(state['within_scene_RNG_differences'])==5 and all(state['native_final_component_equality'].values()) and state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal']
    tests=read('work/analysis/lil_B202_regressions_v5998/terminal.json');assert tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B202_reference_v5985_RESEARCH_ONLY.nds').read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==590 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release
'''

if __name__=='__main__':
    source=Path('scripts/complete_lil_B201_v5952.py').read_text(encoding='utf-8')
    oldgate=source[source.index('def gates():'):source.index('\ndef restore(')]
    changes={
      oldgate:GATES.rstrip(),
      '"""Stage,audit,apply and verify26 disjoint reviews without dropping ledger history."""':'"""Stage,audit,apply and verify19 disjoint reviews without dropping ledger history."""',
      'scripts.lil_B201_completion_text_v5952':'scripts.lil_B202_completion_text_v6003',
      'lil_B201_completion_v5952':'lil_B202_completion_v6003',
      'editorial_handoff_verification_v5953':'editorial_handoff_verification_v6004',
      'translations/lil_B201_editorial_manuscript_v7.json':'translations/lil_B202_editorial_manuscript_v6.json',
      "MENU=Path('translations/lil_B201_choice_manuscript_v4.json')\n":'',
      'lil_B201_contextual_final_review_v1':'lil_B202_contextual_final_review_v1',
      'lil_B201_release_v5948':'lil_B202_release_v5999',
      'lil_B201_startup_v5950':'lil_B202_startup_v6001',
      'lil_B201_actual_v5942/two_paths_all24_complete_panels_two_options_and_source_comparisons.json':'lil_B202_actual_v5992/nineteen_actual_panels_source_matched_controls_and_complete_native_holds.json',
      'lil_B201_actual_review_v5943/viewed24_panels_both_options_returns_and_measured_state_scope.json':'lil_B202_actual_review_v5993/viewed19_panels_complete_return_and_honest_measured_scope.json',
      "LATER=Path('work/analysis/lil_B201_later_differences_v5943b/all_broad_later_pairs_viewed.json')\n":'',
      'editorial_handoff_verification_v5927':'editorial_handoff_verification_v5981',
      'lil_B201_registration_v5946':'lil_B202_registration_v5997',
      'lil_B201_retention_v5951':'lil_B202_retention_v6002',
      'Lil-B201-rigging-price-negotiation-buy-pass-three-stat-notices26':'Lil-B202-unsolicited-book-handoff-pursuit-glassmaking-and-self-interest19',
      'Lil_B201_completion_v5952':'Lil_B202_completion_v6003',
      'unfinished_editorial_scope_v5952':'unfinished_editorial_scope_v6003',
      'Lil_B201_v5952':'Lil_B202_v6003',
      '[-26:]':'[-19:]',
      '[DOC,MENU]':'[DOC]',
      'doc,menu=read(DOC),read(MENU)':'doc=read(DOC)',
      "doc['records']+menu['records']":"doc['records']",
      "{'revise':12,'retain-wording':14}":"{'revise':6,'retain-wording':13}",
      '.blocks[201]':'.blocks[202]',
      'dict(block=201,':'dict(block=202,',
      'len(oldkeys)==6282 and len(keys)==26':'len(oldkeys)==6308 and len(keys)==19',
      "fresh['fresh_pass_records_integrated']==6282":"fresh['fresh_pass_records_integrated']==6308",
      'paths=[DOC,MENU,RELEASE,START,VIEW,REG,PIN,ACTUAL,TRANSITIONS,LATER,PRIOR,':'paths=[DOC,RELEASE,START,VIEW,REG,PIN,ACTUAL,TRANSITIONS,PRIOR,',
      'scripts/lil_B201_completion_text_v5952.py':'scripts/lil_B202_completion_text_v6003.py',
      'lil_B201_regressions_v5947':'lil_B202_regressions_v5998',
      'revised=12,retained=14,source_prose_and_completion_credit_added_once=26':'revised=6,retained=13,source_prose_and_completion_credit_added_once=19',
      'previous_B201_objects_uncredited=True,all26_exact':'previous_B202_objects_uncredited=True,all19_exact',
      'actual_unique_speeches=24,actual_speech_observations=37,offline_only_speeches=0,actual_menu_cases=2,actual_matching_holds=144,natural_event201_not_selected':'actual_unique_speeches=19,actual_speech_observations=19,offline_only_speeches=0,actual_menu_cases=0,actual_matching_holds=74,natural_event202_not_selected',
      'blocks=[201]':'blocks=[202]',
      'revised_count=12,retained_count=14,fresh_revisions=12,fresh_retentions=14':'revised_count=6,retained_count=13,fresh_revisions=6,fresh_retentions=13',
      'records_editorially_completed=6308,records_with_source_and_prose_pass=6311,records_with_source_prose_drafts=6311,records_revised_and_integrated=3953,retained_wordings_editorially_completed=2355':'records_editorially_completed=6327,records_with_source_and_prose_pass=6330,records_with_source_prose_drafts=6330,records_revised_and_integrated=3959,retained_wordings_editorially_completed=2368',
      "==4397;new[key]['/data/SC2.DK4']=4423":"==4423;new[key]['/data/SC2.DK4']=4442",
      '6308 contextual rereads integrated;source/prose6311. B201 counted once.':'6327 contextual rereads integrated;source/prose6330. B202 counted once.',
      'fresh_pass_records_explicitly_reread=6308,fresh_pass_records_integrated=6308':'fresh_pass_records_explicitly_reread=6327,fresh_pass_records_integrated=6327',
      'records=26,final_review=str(FINAL),new_revisions=12,justified_retentions=14,new_completed_records=26':'records=19,final_review=str(FINAL),new_revisions=6,justified_retentions=13,new_completed_records=19',
      'actual_selected_source201_events=[],actual_B22_content_speeches=24,actual_speech_observations=37,offline_only_speeches=0,actual_menu_cases=2':'actual_selected_source202_events=[],actual_B22_content_speeches=19,actual_speech_observations=19,offline_only_speeches=0,actual_menu_cases=0',
      'new_English_content_fixture_runs=2,goal_turn_new_frames=47404,reused_prior_Japanese_frames=26002':'new_English_content_fixture_runs=1,goal_turn_new_frames=34403,reused_prior_Japanese_frames=13001',
      'reviewed_route_records=4709,completed_route_records=4709':'reviewed_route_records=4728,completed_route_records=4728',
      'completion_credit_added=26':'completion_credit_added=19',
      'actual_source_event201_selected=False,goal_turn_new_emulator_runs=4':'actual_source_event202_selected=False,goal_turn_new_emulator_runs=3',
      "status='all26-source-native-reference-actual-registered-release-pass'":"status='all19-source-native-reference-actual-registered-release-pass'",
      'two_FI_three_FE_and_both_original_choice_results_preserved=True':'all26_commands19_preambles7_leaves_and_original_results_preserved=True',
      "old['unfinished_editorial_scope_v5926']":"old['unfinished_editorial_scope_v5980']",
      "inventory['historical_Lil_B201_native_review_before_v5952']=inventory.pop('Lil_B201_native_review_v5926');inventory['Lil_B201_completed_v5952']=dict(final_review=str(FINAL),completed_objects=26,registered_candidate=release['candidate'],actual_speeches=24,actual_speech_observations=37,offline_only_speeches=0,actual_menu_cases=2,complete_native_holds=144,natural_event201_not_selected=True,timing_RNG_later_state_and_RGB_differences_preserved=True)":"inventory['historical_Lil_B202_native_review_before_v6003']=inventory.pop('Lil_B202_native_review_v5980');inventory['Lil_B202_completed_v6003']=dict(final_review=str(FINAL),completed_objects=19,registered_candidate=release['candidate'],actual_speeches=19,actual_speech_observations=19,offline_only_speeches=0,actual_menu_cases=0,complete_native_holds=74,natural_event202_not_selected=True,timing_RNG_later_state_and_RGB_differences_preserved=True)",
      "inventory['next_Lil_B202_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=202,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B201_actor_voice_menu_macro_effect_or_end_assumptions_inherited=True)":"inventory['next_Lil_B203_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=203,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B202_actor_voice_menu_macro_effect_or_end_assumptions_inherited=True)",
      'Lil_B201_previously_uncredited_objects_completed=26,next_Lil_B202_clean_review_pending=True':'Lil_B202_previously_uncredited_objects_completed=19,next_Lil_B203_clean_review_pending=True',
      'new_source_prose_reviews=26,new_completed_records=26,revised=12,retained=14':'new_source_prose_reviews=19,new_completed_records=19,revised=6,retained=13',
      'goal_turn_new_emulator_runs=4,goal_turn_new_frames=47404,reused_prior_source_frames=26002':'goal_turn_new_emulator_runs=3,goal_turn_new_frames=34403,reused_prior_source_frames=13001',
      '## V5952: B201 complete exchange integrated once in cumulative V5947':'## V6003: B202 complete exchange integrated once in cumulative V5998',
      '# Current editorial handoff - V5952':'# Current editorial handoff - V6003',
      'new_completed_records=26,evidence=evidence':'new_completed_records=19,evidence=evidence',
      'Six targets staged;26 reviews':'Six targets staged;19 reviews',
      '(6308,6311,3953,2355)':'(6327,6330,3959,2368)',
      'exactly26_new_disjoint_completed_keys':'exactly19_new_disjoint_completed_keys',
      'values and26 disjoint':'values and19 disjoint',
      "len(read(FINAL)['records'])==26":"len(read(FINAL)['records'])==19",
      'len(allkeys)==6308':'len(allkeys)==6327',
      'exactly26_new_disjoint_source_prose_and_completed_records':'exactly19_new_disjoint_source_prose_and_completed_records',
      'completed=6308,source_prose=6311,revised=3953,retained=2355,SC2=4423,SC3=96,reviewed_routes=4709,completed_routes=4709':'completed=6327,source_prose=6330,revised=3959,retained=2368,SC2=4442,SC3=96,reviewed_routes=4728,completed_routes=4728',
      'all589_manifest_batches114_accepted18_checks_verified':'all590_manifest_batches114_accepted18_checks_verified',
      'actual_unique_B201_speeches=24,actual_speech_observations=37,offline_only_B201_speeches=0,actual_matching_holds=144,actual_menu_cases=2':'actual_unique_B202_speeches=19,actual_speech_observations=19,offline_only_B202_speeches=0,actual_matching_holds=74,actual_menu_cases=0',
      'startup31_frames_and_five_actor_controls_match_V5891':'startup31_frames_and_five_actor_controls_match_V5947',
      'source201_natural_eligibility_earned_affordability_and_full_effect_semantics_not_claimed':'source202_natural_activation_original_location_earned_inventory_and_full_effect_semantics_not_claimed',
      'next_Lil_B202_clean_review_pending=True,retrospective207_name_queue':'next_Lil_B203_clean_review_pending=True,retrospective207_name_queue',
      'V5947 verified:6308 completed/6311 source-prose. B202':'V5998 verified:6327 completed/6330 source-prose. B203',
    }
    proof=derive('scripts/complete_lil_B201_v5952.py','scripts/complete_lil_B202_v6003.py',changes)
    root=Path('work/analysis/lil_B202_completion_preparation_v6003');root.mkdir(parents=True,exist_ok=False);save(root/'derivation.json',proof)
    print('Frozen B202 completion producer prepared; shared coverage unchanged.')
