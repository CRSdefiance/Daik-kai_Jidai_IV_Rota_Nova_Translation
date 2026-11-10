"""Approve scoped B47 formatting after native/stored checks and eight actual sheets."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/Rafael_B47_actual_approval_v8003')
OLD=Path('translations/rafael_B47_editorial_manuscript_v2.json')
OUT=Path('translations/rafael_B47_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/rafael_B47_speaker_name_review_v2.json')
NAMES=Path('translations/rafael_B47_speaker_name_review_v3.json')
ACTUAL=Path('work/analysis/Rafael_B47_actual_v7999/paired_source_English_observed_path_complete_pages_names_andR53_transition.json')
COMPARE=Path('work/analysis/Rafael_B47_actual_comparison_v8000/11_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
RNG=Path('work/analysis/Rafael_B47_waits_v8001/original_wait_code_measured_R53_page_RNG_phases_andlater_limits.json')
FOCUS=Path('work/analysis/Rafael_B47_actual_focus_v8002/focused_actual_page_turn_sheet.json')
RELOC=Path('work/analysis/Rafael_B47_relocation_v7989/one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json')
STORED=Path('work/analysis/Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json')
CONTROL=Path('work/analysis/Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json')
CALLERS=Path('work/analysis/Rafael_B47_reference_census_v7996/all48_commands24_relative_sites15_speeches_EV0_entry_shipped_callers.json')
PLAN=Path('work/analysis/Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json')
REVIEW=Path('work/analysis/Rafael_B47_native_review_v7988/15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json')

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES.exists()
    old,names,actual,comparison,rng,focus,reloc,stored,control,callers,plan,native_review=map(
        read,[OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW])
    assert not actual['unresolved'] and len(actual['groups'])==2 and actual['actual_total_frames']==32002
    assert sum(g['complete_body_holds'] for g in actual['groups'])==88
    assert sum(len(g['speech_observations']) for g in actual['groups'])==22
    assert [g['actual_complete_native_pages'] for g in actual['groups']]==[11,12]
    unvisited=['DK4_MES_B47_R0017','DK4_MES_B47_R0063','DK4_MES_B47_R0092','DK4_MES_B47_R0122']
    assert actual['native_only_unvisited_speech_IDs']==unvisited
    sheets=[]
    for g in actual['groups']:
        assert g['actual_unique_speeches']==11 and g['observed_original_exchange_commands']==35
        assert len(g['command_pairs'])==45 and g['native_terminal_result']==[0,0]
        assert not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows'] and not g['unreturned_following_dialogues']
        terminal=read(f"work/analysis/Rafael_B47_scene_runs_v7998/route0_{g['version']}/terminal.json")
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        for k in ['capture_report','observer_report']:
            assert sha(Path(g[k]).read_bytes())==g[k+'_sha256']
        sheets.extend(g['review_sheets']+[g['transition_sheet']])
    assert comparison['actual_proof_sha256']==rng['actual_proof_sha256']==focus['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert rng['comparison_sha256']==sha(COMPARE.read_bytes())
    sheets.extend([dict(path=comparison['review_sheet'],sha256=comparison['review_sheet_sha256']),
                   dict(path=focus['sheet'],sha256=focus['sheet_sha256'])])
    assert len(sheets)==8
    for s in sheets:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        s.update(directly_viewed=True,finding='Full actual Japanese/English exchange, complete displayed names, R53 page turn and following return inspected. Preserve unmasked later differences. Four conditional speeches remain native-only.')
    assert focus['ordinary_page_transition']['ordinary_A_input']==dict(start=4720,duration=5,buttons=['A'])
    assert focus['ordinary_page_transition']['same_original_command_active_across_page_turn']
    assert stored['relocation_sha256']==control['relocation_sha256']==sha(RELOC.read_bytes())
    assert stored['all15_native_ink_planes_exact_to_already_viewed']
    assert stored['R53_both_complete_stored_pages_exact_to_viewed_sentence_boundary_pages']
    assert len(control['final_dispatches'])==15 and len(control['normal_seeded_ends'])==25
    assert len(callers['all_command_maps'])==48 and len(callers['relative_operand_maps'])==24
    cg=comparison['groups'][0];rg=rng['groups'][0]
    assert cg['source_English_exits']==[6416,6655] and len(cg['later_RGB_differences'])==cg['later_sample_count']==157
    assert cg['all_original_initializer_andexchange_results_equal'] and cg['all_UI_request_words_equal']
    assert cg['all11_whole_upper_scene_portrait_andheader_RGB_equal']
    assert cg['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=False)
    assert not cg['whole_actors_equal'] and cg['final_PRNG_seeds']==[19668379,4016462114]
    assert rg['exit_English_phase']==58 and rg['final_English_phase']==-7833
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
    assert Counter(r['decision'] for r in updated['records'])=={'revision':8,'retention':7}
    assert sum(bool(r['qa_waivers']) for r in updated['records'])==2
    for before,after in zip(old['records'],updated['records'],strict=True):
        assert before['logical_English']==after['logical_English'] and before['compiled_hex']==after['compiled_hex']
        assert before['qa_waiver_scope']==after['qa_waiver_scope'] and all(after['review'].values())
    for r in names['records']:
        observed=r['actor_ID']!=4
        r['review']['formatting']=True
        r.update(actual_B47_progressive_nameplate_verified=observed,native_only_unvisited_B47_header=not observed,
            native_font_bounds_complete_names_actual_B47_headers_andcatalogue_UI_pending=False,
            actual_B47_headers_andcatalogue_UI_still_pending=False,
            full_catalogue_UI_custom_names_andother_contexts_still_pending=True)
    names.update(prior_review=str(OLD_NAMES),prior_review_sha256=sha(OLD_NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_headers_verified_actors=[0,5,6],native_only_header_actors=[4],
        full207_name_role_alias_review_active=True,new_credit=0)
    evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW,Path(__file__)]}
    ROOT.mkdir(parents=True)
    save(NAMES,names)
    updated.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),
        all15_five_review_gates_true=True,all15_formatting_gates_false=False,formatting_review_pending=False,
        native_pages_complete_characters_bounds_pagination_actual_scene_policy_atomic_andrelease_pending=False,
        R53_sentence_boundary_two_pages_requires_actual_transition=False,
        actual_scene_proof=str(ACTUAL),actual_scene_proof_sha256=sha(ACTUAL.read_bytes()),
        source_English_comparison=str(COMPARE),source_English_comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurements_andlimits=str(RNG),RNG_measurements_andlimits_sha256=sha(RNG.read_bytes()),
        actual_review_sheets=sheets,all_eight_actual_review_sheets_directly_viewed=True,
        native_only_unvisited_speech_IDs=unvisited,actual_unique_speeches_each_language=11,
        no_new_prose_orcompiled_bytes_from_canonical_speaker_markup=True,
        all_two_narrow_QA_exceptions_andsix_infos_unchanged=True,
        source_whole_exchange_situation_voice_andindividual_retentions_rechecked_against_actual_panes=True,
        source_relief_caution_explanation_qualified_advice_preparation_overwhelm_andresolve_preserved=True,
        actual_later_models_persistent_objects_actors_calendar_RGB_andRNG_differences_retained=True,
        full_RNG_future_outcome_orbroad_simulation_equality_not_claimed=True,
        status='source-context-prose-native-stored-representative-actual-approved-policy-atomic-registered-release-pending',
        frozen_policy_atomic_production_andregistered_cumulative_integration_still_required=True)
    updated['evidence']=dict(updated['evidence'])|evidence|{str(NAMES):sha(NAMES.read_bytes())}
    save(OUT,updated)
    save(ROOT/'15_source_context_native_representative_actual_approved_policy_release_pending.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurement=str(RNG),RNG_measurement_sha256=sha(RNG.read_bytes()),
        focused_page_turn=str(FOCUS),focused_page_turn_sha256=sha(FOCUS.read_bytes()),
        directly_viewed_sheets=sheets,all15_individual_source_context_prose_andformat_gates_true=True,
        revisions=8,retentions=7,actual_two_runs_frames=32002,actual_speech_occurrences=22,
        actual_unique_speeches_eachlanguage=11,actual_complete_pages_eachlanguage=[11,12],
        actual_complete_holds=88,native_only_unvisited_speech_IDs=unvisited,
        native_all15_paragraphs16_pages_andfour_names_approved=True,
        observed35_of48_original_commands_eachlanguage=True,all48_structural_commands_retained=True,
        R53_two_pages_complete_ordinary_A4720_same_command_andfollowing_R70_return_verified=True,
        exact_two_QA_waivers_with_all_original_diagnostics_preserved=True,
        actual_exits=[6416,6655],normal_results=[[0,0],[0,0]],
        command_comparison_difference_rows=24,duration_difference_rows=4,
        later_RGB_differences=157,later_RGB_sample_count=157,final_PRNG_seeds=[19668379,4016462114],
        English_exit_LCG_phase=58,English_final_LCG_phase=-7833,
        actual_later_models_persistent_objects_actors_calendar_andRGB_differences_preserved=True,
        no_causal_every_call_future_state_orbroad_simulation_equivalence_claim=True,
        disclosed_opening_ROM_entry_fixture_not_natural_B47_activation_original_location_fullroute_orhardware=True,
        four_conditional_speeches_andJanus_header_not_claimed_as_actual_coverage=True,
        incidental_B127_andSailor_sailing_prose_captures_not_new_editorial_credit=True,
        no_ROM_registry_orcompletion_credit_change=True,policy_atomic_registered_integration_pending=True,
        evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B47 formatting approved:15 records/8 revisions7 retentions;11 actual speeches per language,88 holds,eight viewed sheets. Four conditional speeches native-only. Policy/atomic/integration pending;no credit.')
