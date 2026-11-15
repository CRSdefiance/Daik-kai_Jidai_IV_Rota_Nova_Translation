"""Prepare the exact inverse-preserving twenty-review completion from the proven loop."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_completion_tools_v6165')
if __name__=='__main__':
    assert not ROOT.exists();s=Path('scripts/complete_lil_B203_v6055b.py').read_text('utf-8');a=s.index('def gates():');b=s.index('def restore(',a)
    gates='''def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all593_manifest_batches_and114_accepted_layers_present'] and release['all18_registered_release_checks_pass'] and release['whole_ROM_reconstruction_byte_exact'] and release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V6110']
    assert start['all_current_requested_and_final_framebuffers_equal_V6110'] and start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==78 and reg['all_negatives_reject_before_mutation'] and read(PIN)['all_prior_pins_preserved']
    assert (actual['actual_unique_speech_panels'],actual['complete_matching_observations'],actual['complete_matching_holds'])==(20,20,77) and not actual['failures'] and not actual['offline_only_display_IDs']
    assert actual['all35_commands26_source_plus9_initializers_and_four_FE_parts_observed'] and actual['original_command_paths_results_and_complete_end_preserved']
    assert transitions['no_open_translation_specific_display_control_or_return_finding'] and not transitions['visual_review_pending'] and len(transitions['viewed_sheets'])==6 and transitions['current_Shachihoko_notice5530_whole_frame_equal_to_current_source']
    state=read(transitions['measured_state_proof']);assert sha(Path(transitions['measured_state_proof']).read_bytes())==transitions['measured_state_proof_sha256']
    assert state['source_exit_frames']==[7894,7895] and state['English_exit_frame']==7896 and state['all16_later_differences_bounded_to_advance_prompt']
    assert all(state['native_final_component_equality'].values()) and state['whole_actor_and_captain_equal'] and not state['final_PRNG_equal'] and state['no_whole_state_equivalence_claim_from_cross_build_getter_comparison']
    tests=read('work/analysis/lil_B204_regressions_v6160/terminal.json');assert tests['terminal'] and tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text('utf-8')
    for key in ['candidate','patch']:assert sha(Path(release[key]).read_bytes())==release[key+'_sha256']
    assert release['candidate_sha256']==start['candidate_sha256']==sha(Path(release['exact_patch_reconstruction']).read_bytes())==sha(Path('out/lil_B204_reference_v6138_RESEARCH_ONLY.nds').read_bytes())
    registry=read('translations/release_stack.json');manifest=read(release['manifest']);assert len(manifest['batches'])==593 and len(manifest['checks'])==18 and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return release
'''
    ia=s.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v6032']['path']))");ib=s.index("        inv=ROOT/",ia)
    inventory='''        inventory=deepcopy(read(old['unfinished_editorial_scope_v6133']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B204_completed_v6165']=dict(final_review=str(FINAL),completed_objects=20,registered_candidate=release['candidate'],actual_speeches=20,complete_native_holds=77,all26_source_commands_and9_initializers_observed=True,natural_event204_not_selected=True,old_pending_native_flags_preserved_as_history_and_superseded_here=True,measured_timing_RNG_state_and_RGB_limits_preserved=True)
        inventory['next_Lil_B205_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=205,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B204_actor_macro_letter_count_effect_or_end_assumptions_inherited=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=4770,completed_route_records=4770,next=NEXT)
'''
    changes={s[a:b]:gates,s[ia:ib]:inventory,
        "FAMILY='Lil-B203-cordyceps-medicinal-book-offer-companion-interest-and1000-to100-negotiation22'":"FAMILY='Lil-B204-castle-Shachihoko-gift-claim-thief-search-and-four-part-letter20'",
        'B203':'B204','completion_v6055':'completion_v6165','completion_text_v6055':'completion_text_v6165','V6055':'V6165','v6055':'v6165','verification_v6056':'verification_v6166','verification_v6033':'verification_v6134','manuscript_v5':'manuscript_v8','release_v6051':'release_v6161','startup_v6053':'startup_v6163','actual_v6044':'actual_v6146','actual_review_v6045':'actual_review_v6147','registration_v6049':'registration_v6151','retention_v6054':'retention_v6164',
        'twenty_two_actual_panels_source_matched_controls_and_complete_native_holds':'all20_actual_English_panels_complete_native_holds_two_source_scopes_and_return','viewed22_panels_complete_return_and_honest_measured_scope':'viewed20_panels_four_letters_complete_return_and_honest_scope',
        "{'revise':9,'retain-wording':13}":"{'revise':12,'retain-wording':8}",'[203]':'[204]','block=203':'block=204','[-22:]':'[-20:]','==22':'==20','=22':'=20','records=22':'records=20','reviews=22':'reviews=20','completion_credit_added=22':'completion_credit_added=20','22 new':'20 new','22 disjoint':'20 disjoint','22 reviews':'20 reviews','22 complete':'20 complete','22 newly':'20 newly','22_new':'20_new','22_new_':'20_new_',
        'revised=9,retained=13':'revised=12,retained=8','revised_count=9,retained_count=13':'revised_count=12,retained_count=8','fresh_revisions=9,fresh_retentions=13':'fresh_revisions=12,fresh_retentions=8','new_revisions=9,justified_retentions=13':'new_revisions=12,justified_retentions=8',
        '6327':'6350','6349':'6370','6352':'6373','3968':'3981','2381':'2389','4442':'4464','4464':'4484','4728':'4750','4750':'4770',
        'all31_commands22_preambles9_leaves_and_original_results_preserved':'all26_commands20_preambles6_leaves_and_original_results_preserved','actual_B22_content_speeches=22':'actual_B22_content_speeches=20','actual_speech_observations=22':'actual_speech_observations=20','complete_native_holds=86':'complete_native_holds=77','actual_matching_holds=86':'actual_matching_holds=77','reused_prior_Japanese_frames=13001':'reused_prior_Japanese_frames=13001,current_same_code_prefix_from8420_frame_menu_run=True',
        'regressions_v6050':'regressions_v6160','V6050':'V6160','all591_manifest_batches114_accepted18_checks_verified':'all593_manifest_batches114_accepted18_checks_verified','match_V5998':'match_V6110','source203_natural_activation':'source204_natural_activation','next_Lil_B204_clean_review_pending':'next_Lil_B205_clean_review_pending',
    }
    optional={k:v for k,v in changes.items() if k in s};skipped=[k for k in changes if k not in s]
    tool=derive('scripts/complete_lil_B203_v6055b.py','scripts/complete_lil_B204_v6165.py',optional);ROOT.mkdir(parents=True);save(ROOT/'source_locked_completion_derivation.json',dict(tool=tool,optional_cosmetic_source_patterns_not_present=skipped,required_counts=dict(completed=6370,source_prose=6373,revised=3981,retained=2389,SC2=4484,routes=4770,new_records=20),all_original_history_requires_deep_inverse_audit_before_mutation=True,full_goal_complete=False));print('Twenty-review completion loop prepared;6370/6373 totals require staged inverse audit before applying.')
