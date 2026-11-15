"""Derive a losslessly reversible B199 completion without changing native constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B199_completion_tools_v5821')
GATES='''def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all585_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact']
    assert release['every_other_file_font_graphic_route_ARM9_ARM7_and_component_exact_to_V5756']
    assert start['all_current_requested_and_final_framebuffers_equal_V5756'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed']
    assert view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==101 and reg['all_negatives_reject_before_mutation']
    assert actual['actual_unique_speech_panels']==actual['complete_matching_observations']==31 and actual['complete_matching_holds']==120
    assert not actual['failures'] and not actual['paired_region_differences'] and not actual['offline_only_source_indices']
    assert len(actual['actual_timing_differences'])==34 and len(actual['later_whole_RGB_differences'])==6
    assert [v['fixture_exit_frame'] for v in actual['versions']]==[10776,10778]
    assert transitions['all31_actual_native_panels120_complete_holds_and_all182_sampled_nontext_regions_match']
    assert transitions['original_pause_two_picture_layouts_short47xx_A000_and_complete_end_results_preserved']
    assert transitions['no_open_translation_specific_display_or_control_finding'] and transitions['representative_shared_rules_approved']
    assert transitions['sampled_nontext_frames']==182 and transitions['command_start_or_return_difference_count']==34
    assert transitions['speech_duration_difference_count']==6 and transitions['all_nonspeech_control_durations_equal']
    assert transitions['source_and_English_return_frames']==[10776,10778]
    assert transitions['later_sampled_whole_RGB_difference_count']==6 and transitions['six_later_differences_visually_confirmed_advance_prompt_blink']
    assert transitions['PRNG_seeds_differ'] and transitions['complete_RNG_timing_cause_not_traced']
    assert len(set(transitions['final_13001_PRNG_seeds']))==2 and all(transitions['final_native_component_equality'].values())
    assert transitions['no_broad_world_effect_full_RAM_future_random_sequence_or_simulation_equivalence_claim']
    assert transitions['no_natural_event_activation_original_location_full_route_or_hardware_claim']
    assert transitions['total_successful_frames']==26002 and actual['actual_source_and_English_cold_boots']==2
    for evidence in [actual['evidence'],transitions['evidence']]:
        for path,digest in evidence.items():assert sha(Path(path).read_bytes())==digest
    tests=read('work/analysis/lil_B199_regressions_v5816/terminal.json')
    assert tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256']==transitions['research_ROM_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(manifest['batches'])==585 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/lil_B199_retention_v5820/pin_receipt.json')['all_prior_pins_preserved']
    return release

'''
INVENTORY='''        inventory=deepcopy(read(old['unfinished_editorial_scope_v5810']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B199_completed_v5821']=dict(final_review=str(FINAL),completed_objects=31,registered_candidate=release['candidate'],natural_event199_not_selected=True,
            actual_speeches=31,offline_only_speeches=0,actual_matching_holds=120,all182_sampled_nontext_regions_match=True,
            speech_duration_changes=6,shifted_start_return_pairs=34,prompt_blink_sample_differences=6,final_PRNG_seeds_differ=True,
            complete_timing_cause_untraced=True,no_broad_postscene_simulation_equivalence_claim=True)
        inventory['historical_Lil_B199_reference_approved_before_v5821']=inventory.pop('next_Lil_B199_reference_approved_uncredited_v5810')
        inventory['next_Lil_B200_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=200,clean_inventory_and_full_exchange_gloss_before_prior_English=True,
            reviewed_objects=0,new_completion_credit=0,no_B200_command_actor_or_control_assumptions_inherited=True)
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory
'''
VERIFY='''            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],all_original_root_and_nested_history_preserved=True,exactly31_new_disjoint_source_prose_and_completed_records=True,
                completed=6263,source_prose=6266,revised=3928,retained=2335,SC2=4378,SC3=96,reviewed_routes=4664,completed_routes=4664,
                all585_manifest_batches114_accepted18_checks_verified=True,actual_unique_B199_speeches=31,offline_only_B199_speeches=0,actual_matching_holds=120,
                startup31_frames_and_five_actor_controls_match_V5756=True,source199_natural_eligibility_and_full_item_effect_semantics_not_claimed=True,
                speech_duration_changes=6,shifted_start_return_pairs=34,prompt_blink_differences=6,final_PRNG_seeds_differ=True,
                complete_timing_cause_untraced=True,no_broad_postscene_equivalence_or_causal_claim=True,next_Lil_B200_clean_review_pending=True,
                retrospective207_name_queue_and_paired164_165_role_labels_preserved=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5816 integration verified;6263 completed/6266 source-prose. Next B200 clean-source review and full name/broader editorial scope remain active.')
'''
if __name__=='__main__':
    assert not ROOT.exists();text=Path('scripts/complete_lil_B198_v5761.py').read_text(encoding='utf-8')
    g0=text.index('def gates():');g1=text.index('def restore(',g0)
    a=text.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v5750'");b=text.index("        for unit in inventory['broader_coverage_units']:",a)
    v=text.index('            VERIFY.mkdir(parents=True)')
    tools=[derive('scripts/pin_lil_B198_v5760.py','scripts/pin_lil_B199_v5820.py',{
        'B198':'B199','retention_v5760':'retention_v5820','release_v5757':'release_v5817','V5756':'V5816'})]
    changes={
        text[g0:g1]:GATES,text[a:b]:INVENTORY,text[v:]:VERIFY,
        'B198':'B199','completion_v5761':'completion_v5821','verification_v5762':'verification_v5822','verification_v5751':'verification_v5811',
        'release_v5757':'release_v5817','startup_v5759':'startup_v5819','registration_v5755':'registration_v5815',
        'work/analysis/lil_B198_actual_v5743/fifteen_actual_panels_source_matched_controls_and_complete_native_holds.json':
        'work/analysis/lil_B199_actual_v5807/thirty_one_actual_panels_source_matched_controls_and_complete_native_holds.json',
        'work/analysis/lil_B198_visual_approval_v5745/viewed17_native15_actual56_holds_three_paired_sheets_and_source_style11.json':
        'work/analysis/lil_B199_reference_approval_v5809/representative_display_control_and_transition_reconciliation.json',
        'completion_text_v5761':'completion_text_v5821','editorial_scope_v5761':'editorial_scope_v5821','B198_v5761':'B199_v5821',
        'Lil-B198-Namahage-refrain-dream-and-prospective-Admiral-handover17':'Lil-B199-portrait-chase-found-book-and-misunderstood-gift31',
        "{'revise':12,'retain-wording':5}":"{'revise':11,'retain-wording':20}",
        '6215':'6232','6232':'6263','6235':'6266','3917':'3928','2315':'2335','4330':'4347','4347':'4378','4633':'4664',
        '[-17:]':'[-31:]','all17':'all31','exactly17':'exactly31','==17':'==31','=17':'=31',
        'revised=12':'revised=11','revised_count=12':'revised_count=11','fresh_revisions=12':'fresh_revisions=11','new_revisions=12':'new_revisions=11',
        'retained=5':'retained=20','retained_count=5':'retained_count=20','fresh_retentions=5':'fresh_retentions=20','justified_retentions=5':'justified_retentions=20',
        'actual_unique_speeches=15,offline_only_speeches=2,actual_menu_cases=0,actual_matching_holds=56':
        'actual_unique_speeches=31,offline_only_speeches=0,actual_menu_cases=0,actual_matching_holds=120',
        'actual_B22_content_speeches=15,offline_only_speeches=2,actual_menu_cases=0':'actual_B22_content_speeches=31,offline_only_speeches=0,actual_menu_cases=0',
        'lil_B198_regressions_v5756':'lil_B199_regressions_v5816','lil_B198_retention_v5760':'lil_B199_retention_v5820',
        'blocks[198]':'blocks[199]','block=198':'block=199','blocks=[198]':'blocks=[199]',
        'natural_event198':'natural_event199','source198':'source199','actual_source_event197_selected':'actual_source_event199_selected',
        'Lil_B199_clean_review_pending=True':'Lil_B200_clean_review_pending=True',
        'source_story_style11_and_refrain_phrase_grouping_preserved':'one_FI_private_thoughts_complete_R95_and_quick_on_his_feet_phrase_grouping_preserved',
        "fields=['current_reference'":"fields=['registered_runtime_catalog_entry','current_effective_macro_template_English','current_effective_paragraph','current_raw_storage_English','current_reference'",
        '## V5761: Seventeen Lil B198 reviews integrated once in cumulative V5756':'## V5821: Thirty-one Lil B199 reviews integrated once in cumulative V5816',
        '# Current editorial handoff - V5761':'# Current editorial handoff - V5821',
        'twenty':'twenty',
        'seventeen':'thirty-one','Seventeen':'Thirty-one'}
    changes.pop('twenty')
    tools.append(derive('scripts/complete_lil_B198_v5761.py','scripts/complete_lil_B199_v5821.py',changes))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_lossless_once_only_completion.json',dict(tools=tools,new_objects=31,revised=11,retained=20,
        target_completed=6263,target_source_prose=6266,target_revisions=3928,target_retentions=2335,
        full_original_root_and_nested_ledger_inverse_required=True,predecessor_runtime_catalog_and_effective_wording_preserved=True,
        actual31_speeches120_holds_and_measured_timing_prompt_PRNG_differences_preserved=True,
        source_patch_startup_regression_pins_gates_required_before_application=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared lossless once-only B199 completion:31 objects,11 revisions/20 retentions;all release/startup gates required before stage.')
