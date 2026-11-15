"""Approve scoped B48 formatting after native/stored checks and eight actual sheets."""
HISTORICAL_B47_FINAL_SEED_LITERALS=((19668379,4016462114),(19668379,4016462114))
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/Rafael_B48_actual_approval_v8057')
OLD=Path('translations/rafael_B48_editorial_manuscript_v3.json')
OUT=Path('translations/rafael_B48_editorial_manuscript_v4.json')
OLD_NAMES=Path('translations/rafael_B48_speaker_name_review_v2.json')
NAMES=Path('translations/rafael_B48_speaker_name_review_v3.json')
ACTUAL=Path('work/analysis/Rafael_B48_actual_v8053/paired_source_English_observed_path_complete_pages_names_andR347_transition.json')
COMPARE=Path('work/analysis/Rafael_B48_actual_comparison_v8054/78_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
RNG=Path('work/analysis/Rafael_B48_waits_v8056/original_wait_code_measured_R347_page_RNG_phases_andlater_limits.json')
FOCUS=Path('work/analysis/Rafael_B48_actual_focus_v8055b/focused_actual_page_turn_sheet.json')
RELOC=Path('work/analysis/Rafael_B48_relocation_v8041/one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json')
STORED=Path('work/analysis/Rafael_B48_stored_v8042/all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json')
CONTROL=Path('work/analysis/Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json')
CALLERS=Path('work/analysis/Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json')
PLAN=Path('work/analysis/Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json')
REVIEW=Path('work/analysis/Rafael_B48_native_review_v8040/91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES.exists()
    old,names,actual,comparison,rng,focus,reloc,stored,control,callers,plan,native_review=map(
        read,[OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW])
    assert not actual['unresolved'] and len(actual['groups'])==2 and actual['actual_total_frames']==80002
    assert sum(g['complete_body_holds'] for g in actual['groups'])==486
    assert sum(len(g['speech_observations']) for g in actual['groups'])==156
    assert [g['actual_complete_native_pages'] for g in actual['groups']]==[78,79]
    unvisited=['DK4_MES_B48_R0017','DK4_MES_B48_R0032','DK4_MES_B48_R0049','DK4_MES_B48_R0081','DK4_MES_B48_R0086','DK4_MES_B48_R0232','DK4_MES_B48_R0236','DK4_MES_B48_R0239','DK4_MES_B48_R0273','DK4_MES_B48_R0385','DK4_MES_B48_R0389','DK4_MES_B48_R0393','DK4_MES_B48_R0396']
    assert actual['native_only_unvisited_speech_IDs']==unvisited
    sheets=[]
    for g in actual['groups']:
        assert g['actual_unique_speeches']==78 and g['observed_original_exchange_commands']==136
        assert len(g['command_pairs'])==146 and g['native_terminal_result']==[0,0]
        assert not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows']
        assert len(g['unreturned_following_dialogues'])==1 and g['complete_first_exchange_distinguished_from_later_fixture_reentry']
        assert g['later_fixture_reentry_frames']==([35462] if g['version']=='clean_Japanese' else [35702])
        terminal=read(f"work/analysis/Rafael_B48_scene_runs_v8050/route0_{g['version']}/terminal.json")
        assert terminal['terminal'] and terminal['frames']==40001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        for k in ['capture_report','observer_report']:
            assert sha(Path(g[k]).read_bytes())==g[k+'_sha256']
        sheets.extend(g['review_sheets']+[g['transition_sheet']])
    assert comparison['actual_proof_sha256']==rng['actual_proof_sha256']==focus['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert rng['comparison_sha256']==sha(COMPARE.read_bytes())
    sheets.extend([dict(path=comparison['review_sheet'],sha256=comparison['review_sheet_sha256']),
                   dict(path=focus['sheet'],sha256=focus['sheet_sha256'])])
    assert len(sheets)==31
    for s in sheets:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        s.update(directly_viewed=True,finding='Full actual Japanese/English exchange, complete displayed names, R347 page turn and following return inspected. Preserve unmasked later differences. Thirteen conditional speeches remain native-only; six progressive names observed, three native-only. Later fixture re-entry is retained.')
    assert focus['ordinary_page_transition']['ordinary_A_input']==dict(start=18400,duration=5,buttons=['A'])
    assert focus['ordinary_page_transition']['same_original_command_active_across_page_turn']
    assert stored['relocation_sha256']==control['relocation_sha256']==sha(RELOC.read_bytes())
    assert stored['all91_native_ink_planes_exact_to_already_viewed']
    assert stored['R347_both_complete_stored_pages_exact_to_viewed']
    assert len(control['final_dispatches'])==91 and len(control['normal_seeded_ends'])==25
    assert len(callers['all_command_maps'])==163 and len(callers['relative_operand_maps'])==28
    cg=comparison['groups'][0];rg=rng['groups'][0]
    assert cg['source_English_exits']==[22735,22973] and len(cg['later_RGB_differences'])==cg['later_sample_count']==285
    assert cg['all_original_initializer_andexchange_results_equal'] and cg['all_UI_request_words_equal']
    assert cg['all78_whole_upper_scene_portrait_andheader_RGB_equal']
    assert cg['five_native_component_equality']==dict(state=True,models=True,persistent_objects=False,tasks=True,calendar=True)
    assert not cg['whole_actors_equal'] and cg['final_PRNG_seeds']==[int('1328542105'),int('448695880')]
    assert rg['exit_English_phase']==63 and rg['final_English_phase']==-393
    assert rng['exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified']
    updated=deepcopy(old)
    for row,p in zip(updated['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['compiled_hex']==p['encoded_hex'] and row['source_hex']==p['source_hex']
        observations=[dict(version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        observed=row['id'] not in unvisited
        assert bool(observations)==observed
        if observed:
            assert {o['version'] for o in observations}=={'clean_Japanese','English'}
            assert all(o['speech']['complete_body_holds'] for o in observations)
        assert row['planned_English_markup']==p['planning_record']['english']=='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['logical_English']
        row.update(english=row['planned_English_markup'],actual_record_observed=observed,
            actual_source_andEnglish_observations=observations,
            native_only_unvisited_conditional=not observed,
            source_presentation_consumer_not_yet_approved=False,
            source_native_names_roles_controls_display_andcurrent_comparison_pending=False,
            current_effective_body_dispatch_andcatalogue_pending=False,
            native_font_wrapping_reference_actual_policy_andregistered_release_pending=False,
            stored_relocation_actual_page_transition_policy_andregistered_release_pending=False,
            frozen_policy_atomic_production_andregistered_release_still_pending=True)
        row['review']['formatting']=True
    assert Counter(r['decision'] for r in updated['records'])=={'revision':42,'retention':49}
    assert sum(bool(r['qa_waivers']) for r in updated['records'])==2
    for before,after in zip(old['records'],updated['records'],strict=True):
        assert before['logical_English']==after['logical_English'] and before['compiled_hex']==after['compiled_hex']
        assert before['qa_waiver_scope']==after['qa_waiver_scope'] and all(after['review'].values())
    for r in names['records']:
        observed=r['actor_ID'] in [0,5,6,8,75,113]
        r['review']['formatting']=True
        r.update(actual_B48_progressive_nameplate_verified=observed,native_only_unvisited_B48_header=not observed,
            native_font_bounds_complete_names_actual_B48_headers_andcatalogue_UI_pending=False,
            actual_B48_headers_andcatalogue_UI_still_pending=False,
            full_catalogue_UI_custom_names_andother_contexts_still_pending=True)
    names.update(prior_review=str(OLD_NAMES),prior_review_sha256=sha(OLD_NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_headers_verified_actors=[0,5,6,8,75,113],native_only_header_actors=[4,7,13],
        full207_name_role_alias_review_active=True,new_credit=0)
    evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW,Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(NAMES,names)
    updated.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),
        all91_five_review_gates_true=True,all91_formatting_gates_false=False,formatting_review_pending=False,
        native_pages_complete_characters_bounds_pagination_actual_scene_policy_atomic_andrelease_pending=False,
        R347_sentence_boundary_two_pages_requires_actual_transition=False,
        actual_scene_proof=str(ACTUAL),actual_scene_proof_sha256=sha(ACTUAL.read_bytes()),
        source_English_comparison=str(COMPARE),source_English_comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurements_andlimits=str(RNG),RNG_measurements_andlimits_sha256=sha(RNG.read_bytes()),
        actual_review_sheets=sheets,all31_actual_review_sheets_directly_viewed=True,
        native_only_unvisited_speech_IDs=unvisited,actual_unique_speeches_each_language=78,
        no_new_prose_orcompiled_bytes_from_canonical_speaker_markup=True,
        all_two_narrow_QA_exceptions_and37_infos_unchanged=True,
        source_whole_exchange_situation_voice_andindividual_retentions_rechecked_against_actual_panes=True,
        source_learning_banter_naturalist_assistant_acquaintance_seven_treasures_uncertain_rumor_anditem_role_preserved=True,
        actual_later_persistent_objects_actors_RGB_andRNG_differences_retained_state_models_tasks_calendar_equal=True,
        full_RNG_future_outcome_orbroad_simulation_equality_not_claimed=True,
        status='source-context-prose-native-stored-representative-actual-approved-policy-atomic-registered-release-pending',
        frozen_policy_atomic_production_andregistered_cumulative_integration_still_required=True)
    updated['evidence']=dict(updated['evidence'])|evidence|{str(NAMES):sha(NAMES.read_bytes())}
    save(OUT,updated)
    save(ROOT/'91_source_context_native_representative_actual_approved_policy_release_pending.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurement=str(RNG),RNG_measurement_sha256=sha(RNG.read_bytes()),
        focused_page_turn=str(FOCUS),focused_page_turn_sha256=sha(FOCUS.read_bytes()),
        directly_viewed_sheets=sheets,all91_individual_source_context_prose_andformat_gates_true=True,
        revisions=42,retentions=49,actual_two_runs_frames=80002,actual_speech_occurrences=156,
        actual_unique_speeches_eachlanguage=78,actual_complete_pages_eachlanguage=[78,79],
        actual_complete_holds=486,native_only_unvisited_speech_IDs=unvisited,
        native_all91_paragraphs92_pages_andnine_names_approved=True,
        observed136_of163_original_commands_eachlanguage=True,all163_structural_commands_retained=True,
        R347_two_pages_complete_ordinary_A18400_same_command_andfollowing_R350_return_verified=True,
        exact_two_QA_waivers_with_all_original_diagnostics_preserved=True,
        actual_exits=[22735,22973],normal_results=[[0,0],[0,0]],
        command_comparison_difference_rows=129,duration_difference_rows=34,
        later_RGB_differences=285,later_RGB_sample_count=285,final_PRNG_seeds=[int('1328542105'),int('448695880')],
        English_exit_LCG_phase=63,English_final_LCG_phase=-393,
        actual_later_persistent_objects_actors_andRGB_differences_preserved_state_models_tasks_calendar_equal=True,
        no_causal_every_call_future_state_orbroad_simulation_equivalence_claim=True,
        disclosed_opening_ROM_entry_fixture_not_natural_B48_activation_original_location_fullroute_orhardware=True,
        thirteen_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage=True,
        incidental_B127_andSailor_sailing_prose_captures_not_new_editorial_credit=True,
        no_ROM_registry_orcompletion_credit_change=True,policy_atomic_registered_integration_pending=True,
        evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B48 formatting approved:91 records/42 revisions49 retentions;78 actual speeches per language,486 holds,31 viewed sheets. Thirteen conditional speeches native-only. Policy/atomic/integration pending;no credit.')
