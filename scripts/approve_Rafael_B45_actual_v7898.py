"""Record all directly viewed complete actual panes and native formatting; production/release remain pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_actual_approval_v7898')
SOURCE=Path('translations/rafael_B45_editorial_manuscript_v3.json')
OUTPUT=Path('translations/rafael_B45_editorial_manuscript_v4.json')
NAME_SOURCE=Path('translations/rafael_B45_speaker_name_review_v1.json')
NAME_OUTPUT=Path('translations/rafael_B45_speaker_name_review_v2.json')
ACTUAL=Path('work/analysis/Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json')
COMPARISON=Path('work/analysis/Rafael_B45_actual_comparison_v7896b/12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
RNG=Path('work/analysis/Rafael_B45_random_waits_v7897/actual_one_step_RNG_phase_andunchanged_source_discarded_wait_contract.json')
PLAN=Path('work/analysis/Rafael_B45_layout_v7881b/12_automatic_plans_full_native_width_zero_preamble_separate_body.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not NAME_OUTPUT.exists()
    doc,names,actual,comparison,rng,plan=map(read,[SOURCE,NAME_SOURCE,ACTUAL,COMPARISON,RNG,PLAN])
    assert not actual['unresolved'] and actual['all24_pages_complete']
    assert comparison['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and rng['comparison_sha256']==sha(COMPARISON.read_bytes())
    assert len(actual['groups'])==2 and sum(g['complete_body_holds'] for g in actual['groups'])==90
    assert all(g['actual_unique_speeches']==12 and g['native_terminal_result']==[0,1] and g['exit_frame']==6653 and not g['incomplete_sampled_holds'] for g in actual['groups'])
    assert comparison['groups'][0]['later_sample_count']==157 and not comparison['groups'][0]['later_RGB_differences']
    assert all(comparison['groups'][0]['five_native_component_equality'].values()) and comparison['groups'][0]['whole_actors_equal']
    assert rng['English_exactly_one_LCG_step_ahead_at_end_andfinal'] and rng['exact_random_state_andfuture_random_outcome_equality_NOT_verified']
    viewed=[]
    for g in actual['groups']:
        for s in g['review_sheets']+[g['transition_sheet']]:
            assert sha(Path(s['path']).read_bytes())==s['sha256']
            viewed.append(dict(**s,directly_viewed=True,
                scope='All twelve complete panes per language across two sheets,plus first/FE/normal-return/final transition sheet',
                finding='Complete leading/internal/trailing glyphs andpunctuation;both proper-name headers andportraits;FE blank nameplate,FO20percent,buying explanation andsingle-page bounds;natural contextual English andsource qualifiers preserved. Fixture atLisbon,not natural Ceuta activation.'))
    late=dict(path=comparison['review_sheet'],sha256=comparison['review_sheet_sha256'])
    assert sha(Path(late['path']).read_bytes())==late['sha256']
    viewed.append(dict(**late,directly_viewed=True,
        scope='Three paired full unmasked later screens atreturn,middle andfinal',
        finding='Lisbon Trader andtrade UI match;incidental UI doesnot receive new editorial credit. All157 later pairs checked offline.'))
    assert len(viewed)==7
    after=deepcopy(doc);approved=[]
    for row in after['records']:
        p=next(r for r in plan['records'] if r['id']==row['id'])
        observations=[next(s for s in g['speech_observations'] if s['id']==row['id']) for g in actual['groups']]
        assert all(s['complete_body_holds'] and not s['incomplete_sampled_holds'] for s in observations)
        assert not row['review']['formatting'] and all(row['review'][g] for g in ['source','context','localization','naturalness'])
        markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['english']
        for token in ['FI','FA','FO']:markup=markup.replace(token,'{MACRO:'+token+'}')
        assert markup==p['planning_record']['english'] and row['compiled_hex']==p['encoded_hex']
        row.update(logical_English=row['english'],english=markup,
            approved_formatting_consumer='FE-paper' if row['source_selector']==254 else 'progressive',
            actual_source_andEnglish_observations=observations,
            actual_scene_andstored_parity_tail_display_not_yet_approved=False,
            native_font_wrapping_reference_actual_policy_andregistered_release_pending=False,
            policy_atomic_production_andregistered_release_pending=True,
            status='source-context-prose-native-stored-actual-format-approved;frozen-policy-atomic-registered-integration-pending')
        row['review']['formatting']=True;approved.append(row['id'])
    historical_flags={}
    for k in ['all12_formatting_gates_false','all12_formatting_gates_false_until_stored_source_controls_policy_actual_andrelease_checks',
              'one_FE_market_share_panel_needs_distinct_native_consumer_percent_macro_bounds_andactual_checks']:
        if k in after:historical_flags[k]=after.pop(k)
    after.update(prior_manuscript=dict(path=str(SOURCE),sha256=sha(SOURCE.read_bytes())),
        historical_pending_flags_superseded_by_native_actual_approval=historical_flags,
        formatting_review_pending=False,all12_five_review_gates_true=True,
        actual_scene_proof=str(ACTUAL),actual_scene_proof_sha256=sha(ACTUAL.read_bytes()),
        source_English_comparison=str(COMPARISON),source_English_comparison_sha256=sha(COMPARISON.read_bytes()),
        RNG_measurement_andlimits=str(RNG),RNG_measurement_andlimits_sha256=sha(RNG.read_bytes()),
        actual_review_sheets=viewed,all24_complete_actual_panes_seven_sheets_directly_viewed=True,
        source_English_one_step_RNG_difference_documented_not_claimed_equal=True,
        no_new_prose_orcompiled_bytes_from_canonical_speaker_macro_markup_conversion=True,
        exact_whole_block_relocation_registered_production_policy_andrelease_still_required=True,
        names_packet=str(NAME_OUTPUT),new_credit=0,registered_candidate=False)
    name_after=deepcopy(names)
    for row in name_after['records']:
        actor=row['actor_ID'];observed=[s for g in actual['groups'] for s in g['speech_observations'] if s['source_selector']==actor]
        assert observed and all(s['actual_name']==row['name'] and s['complete_body_holds'] for s in observed)
        row['historical_pending_flags']=dict(actual_B45_headers_andother_consumer_UI_pending=row.pop('actual_B45_headers_andother_consumer_UI_pending'))
        row.update(actual_B45_progressive_headers_verified=True,actual_observations=observed,
            full_name_catalogue_UI_andother_contexts_not_newly_observed=True,source_bound_spelling_retained_no_name_asset_change=True)
    name_after.update(prior_review=dict(path=str(NAME_SOURCE),sha256=sha(NAME_SOURCE.read_bytes())),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),two_scoped_name_retentions_actual_headers_verified=True,
        full207_name_role_alias_review_active=True,new_credit=0,full_goal_complete=False)
    save(NAME_OUTPUT,name_after);save(OUTPUT,after)
    ROOT.mkdir(parents=True);save(ROOT/'12_source_context_native_actual_format_approved_policy_release_pending.json',dict(
        manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),names=str(NAME_OUTPUT),names_sha256=sha(NAME_OUTPUT.read_bytes()),
        prior_manuscript=str(SOURCE),prior_manuscript_sha256=sha(SOURCE.read_bytes()),approved_ids=approved,revisions=7,retentions=5,
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        comparison=str(COMPARISON),comparison_sha256=sha(COMPARISON.read_bytes()),
        RNG_measurement=str(RNG),RNG_measurement_sha256=sha(RNG.read_bytes()),directly_viewed_sheets=viewed,
        all24_complete_actual_pages90_complete_holds84_progressive_headers6_FE_absent_headers=True,
        actual32_commands_each_including10_prelude22_selected_B45_commands=True,
        unselected0400_outer0100_have_all_five_native_case_coverage_not_individual_gameplay=True,
        both_actual_normal_end_type0_value1_exit6653=True,
        full_names_andFE_panel_native_consumers_kept_distinct=True,
        all_five_component_andwhole_actor_match157_later_RGB_pairs_match_butRNG_one_step_differs=True,
        exact_random_state_future_outcomes_full_route_original_Ceuta_activation_andhardware_NOT_verified=True,
        source_whole_exchange_situation_voice_andall_individual_retentions_rechecked_against_actual_panes=True,
        canonical_markup_conversion_not_new_prose_orlayout_change=True,
        all12_per_record_five_gates_true_but_frozen_policy_atomic_production_registered_release_pending=True,
        no_new_emulator_runs_orcompletion_credit_from_this_approval=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAME_SOURCE,ACTUAL,COMPARISON,RNG,PLAN,Path(__file__)]},full_goal_complete=False))
    print('All24 actual panes/seven sheets viewed;90complete holds,84headers/six FE absent headers. Twelve source-first records havefive gates;canonical speaker/macro markup preserves exact prose/bytes. Frozen policy/atomic/registered integration pending;no credit.')
