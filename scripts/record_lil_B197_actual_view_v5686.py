"""Accept measured display/control scope;retain timing,RNG and later-world differences."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_actual_review_v5686')
INPUT=Path('work/analysis/lil_B197_actual_review_v5685/three_paths_final_state_full_screens_and_unmasked_differences.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(INPUT);actual=read(d['actual_proof'])
    assert sha(Path(d['actual_proof']).read_bytes())==d['actual_proof_sha256']
    assert not actual['failures'] and not actual['paired_nontext_region_differences'] and not actual['command_result_differences']
    assert actual['actual_unique_speech_panels']==21 and actual['actual_English_speech_observations']==35 and len(actual['actual_menu_cases'])==3
    assert actual['complete_native_holds']==128 and not actual['offline_only_display_IDs']
    assert all(h['shared_source_speech_hold'] and all(h['paired_region_equality'].values()) for r in actual['all_actual_speech_observations'] for h in r['holds'])
    assert all(any(h['selected_highlight_matches_return_when_visible'] for h in r['holds']) for r in actual['actual_menu_cases'])
    assert len(actual['command_timing_differences'])==59 and len(actual['later_whole_RGB_differences'])==82
    versions={(v['path'],v['case']):v for v in actual['versions']};witnesses=[]
    for path,jp_end,en_end in [('buy',5736,5735),('no_buy',5016,5019),('delegate',6696,6695)]:
        jp,en=[versions[path,c] for c in ['clean_Japanese','reviewed_English']]
        assert (jp['fixture_exit_frame'],en['fixture_exit_frame'])==(jp_end,en_end)
        pairs=[]
        for a,b in zip(jp['selected_B22_command_pairs'],en['selected_B22_command_pairs'],strict=True):
            assert (a.get('original_source_offset'),a['word'],a['result_words'])==(b.get('original_source_offset'),b['word'],b['result_words'])
            if (a['before_seed'],a['after_seed'])!=(b['before_seed'],b['after_seed']):pairs.append(dict(source_offset=a.get('original_source_offset'),word=a['word'],Japanese=[a['before_seed'],a['after_seed']],English=[b['before_seed'],b['after_seed']]))
        witnesses.append(dict(path=path,RNG_differences_within_original_command_intervals=pairs,end_RNG=[jp['selected_B22_command_pairs'][-1]['after_seed'],en['selected_B22_command_pairs'][-1]['after_seed']],
            all_original_command_words_paths_and_results_equal=True,no_seed_or_result_forced=True))
    for pair in d['paired_final_state_measurements']:
        assert pair['five_native_component_equality']['state'] and pair['five_native_component_equality']['tasks']
        if pair['path']=='no_buy':assert all(pair['five_native_component_equality'].values()) and pair['whole1A04_actor_and_captain2_equal'] and pair['PRNG_equal']
        else:assert not pair['whole1A04_actor_and_captain2_equal'] and not pair['PRNG_equal']
    views=[]
    for s in d['actual_consumer_menu_sheets']+[d['supplemental_menu_sheet']]:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        views.append({**s,'viewed':True,'viewed_after_image_return':True,'original_detail':True,
            'review':'Viewed all21 full English speech panels and all three visibly selected options. Purchase acceptance precedes the romantic rebuff;the personal inability/apology/gift/future wish/stammer/doubt sequence remains complete. All128 native-mask holds preserve every first/internal/final glyph and match paired upper/portrait/name/book regions. Ian Charm notice appears after all three choices. R74 ordinary two-row negative-verb wrap remains readable with all56 characters. No clipped glyph,overflow,unintended page,blank text page or authored premature break was found.'})
    full=[]
    for s in d['full_screen_sheets']+[d['later_full_screen_pairs']]:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        full.append({**s,'viewed':True,'viewed_after_image_return':True,'original_detail':True,
            'review':'Viewed complete paired Japanese/English purchase rebuff,refusal,gift surprise and three common Ian Charm notices. The R64 refusal and R89 surprise have blank portrait/name regions in BOTH exact-frame source and English panels;record source behavior rather than inventing an English-specific defect or asserting continuous speaker visibility. Buy/delegation clear the book card for FE;refusal keeps it. All six later12970 views show normal continuing Sea View,without a stuck changed-scene modal. Purchase/delegation water/weather/ship state differ;no complete postscene RGB or simulation equivalence is claimed. The existing Shakuntala card adds no spoken-title or widget fidelity credit.'})
    assert len(views)==5 and len(full)==4
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    sessions=[43857,45482,9879,76853,79039,18958]
    ROOT.mkdir(parents=True);save(ROOT/'viewed21_panels_three_options_returns_and_measured_scope.json',dict(
        actual_proof=d['actual_proof'],actual_proof_sha256=d['actual_proof_sha256'],previous_visual_analysis=str(INPUT),previous_visual_analysis_sha256=sha(INPUT.read_bytes()),
        all_actual_consumer_menu_sheets_viewed=views,paired_full_screen_views=full,
        actual_unique_speech_panels=21,actual_speech_observations=35,actual_menu_cases=3,complete_native_speech_holds=128,offline_only_display_IDs=[],
        all21_source_speeches_observed_across_three_choices_without_global_exhaustive_visit_requirement=True,
        all128_complete_native_holds_match_source_upper_portrait_name_and_picture_regions=True,
        all_three_actual_indices0_1_2_complete_labels_and_visible_highlights_verified=True,
        original39_source_commands_and9_identical_initializers_stored_without_omission_or_flattening=True,
        original_funds_roster_conditions_RNG_and_effect_results_unforced_and_ordinary_gamepad_only=True,
        all_original_command_paths_words_and_result_values_equal=True,
        source_matched_blank_portrait_name_additional_records=[64,89],
        source_R24_restoration_does_not_imply_every_later_panel_has_visible_portrait_or_name=True,
        initial_handoff0x0202A1EC_return_address_note_superseded_by_original0x02029FEC=True,
        exact_source_trace_correction='work/analysis/lil_B197_control_correction_v5681c/source_trace_address_correction_and_stopped_receipt_preserved.json',
        original_script_R3_pointer_moves_with_mapped_command_offset_not_a_control_mutation=True,
        paired_command_timing_differences=actual['command_timing_differences'],postscene_whole_RGB_differences=actual['later_whole_RGB_differences'],
        within_scene_RNG_witnesses=witnesses,paired_final_state_measurements=d['paired_final_state_measurements'],
        no_buy_five_native_groups_actor_captain_and_PRNG_equal=True,
        buy_delegate_models_persistent_objects_actor_and_PRNG_differ_buy_calendar_group_also_differs=True,
        broad_postscene_equivalence_unproven_and_not_substituted_for_source_control_display_and_return_checks=True,
        no_causal_explanation_of_timing_RNG_or_world_differences_certified=True,
        initial_menu_sampling_failure_resolved_by16_new_complete_active_highlight_holds_without_retiming=True,
        no_open_translation_specific_display_menu_control_or_return_finding=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,
        no_further_focus_run_required_by_current_distinct_display_findings=True,
        actual_event197_natural_selection_outer_eligibility_original_location_earned_affordability_not_claimed=True,
        no_complete_item_Charm_inventory_full_RAM_future_world_full_playthrough_or_hardware_claim=True,
        new_successful_English_runs=4,new_successful_English_frames=43604,reused_prior_source_runs=3,reused_prior_source_frames=39003,
        successful_complete_source_English_runs=6,successful_focus_runs=1,total_successful_frames=82607,
        two_failed_English_runs_not_counted_as_passes=True,terminal_reaped_tool_sessions=sessions,all_failed_partial_outputs_preserved=True,
        visual_review_pending=False,evidence={**d['evidence'],str(INPUT):sha(INPUT.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())},
        full_goal_complete=False))
    print('Viewed4 speech sheets,one all-option sheet,three paired scene sheets and six later screens.21 panels/35 observations/128 native holds/three options pass;59 timings and82 later RGB differences plus state/RNG differences retained. No broad simulation-equivalence claim.')
