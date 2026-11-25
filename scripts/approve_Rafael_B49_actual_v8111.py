"""Approve exact B49 formatting after complete native/stored checks and directly viewed representative actual scenes."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_actual_approval_v8111')
OLD=Path('translations/rafael_B49_editorial_manuscript_v2.json')
OUT=Path('translations/rafael_B49_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/rafael_B49_speaker_name_review_v2.json')
NAMES=Path('translations/rafael_B49_speaker_name_review_v3.json')
ACTUAL=Path('work/analysis/Rafael_B49_actual_v8107/paired_source_English_observed_path_complete_pages_names_C281_andreturn.json')
COMPARE=Path('work/analysis/Rafael_B49_actual_comparison_v8108/all_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
RNG=Path('work/analysis/Rafael_B49_waits_v8109/original_wait_code_measured_C281_RNG_phases_andlater_limits.json')
FOCUS=Path('work/analysis/Rafael_B49_actual_focus_v8110/focused_actual_C281_names_return_sheet.json')
RELOC=Path('work/analysis/Rafael_B49_relocation_v8096/one_block61_speeches56_relative_fixups280_cases_exact_full_inverse.json')
STORED=Path('work/analysis/Rafael_B49_stored_v8097/all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json')
CONTROL=Path('work/analysis/Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json')
CALLERS=Path('work/analysis/Rafael_B49_reference_census_v8104/all154_commands56_relative_sites61_speeches_C281_EV0_entry_shipped_callers.json')
PLAN=Path('work/analysis/Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json')
REVIEW=Path('work/analysis/Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json')
UNVISITED=['DK4_MES_B49_R0032','DK4_MES_B49_R0067','DK4_MES_B49_R0112','DK4_MES_B49_R0225','DK4_MES_B49_R0244','DK4_MES_B49_R0296','DK4_MES_B49_R0311','DK4_MES_B49_R0356','DK4_MES_B49_R0381','DK4_MES_B49_R0405','DK4_MES_B49_R0409']
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES.exists()
    old,names,actual,comparison,rng,focus,reloc,stored,control,callers,plan,native_review=map(read,[OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW])
    assert not actual['unresolved'] and actual['actual_total_frames']==48002 and actual['native_only_unvisited_speech_IDs']==UNVISITED
    assert sum(g['complete_body_holds'] for g in actual['groups'])==318
    assert len(actual['groups'])==2 and [g['actual_complete_native_pages'] for g in actual['groups']]==[50,50]
    sheets=[]
    for g in actual['groups']:
        assert g['actual_unique_speeches']==50 and g['observed_original_exchange_commands']==119 and len(g['command_pairs'])==129
        assert g['native_terminal_result']==[0,0] and not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows']
        assert not g['unreturned_following_dialogues'] and not g['later_fixture_reentry_frames']
        assert sorted({s['source_selector'] for s in g['speech_observations']})==[0,2,5,9]
        assert g['complete_first_exchange_distinguished_from_later_fixture_reentry']
        terminal=read(f"work/analysis/Rafael_B49_scene_runs_v8106/route0_{g['version']}/terminal.json")
        assert terminal['terminal'] and terminal['frames']==24001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        for key in ['capture_report','observer_report']:assert sha(Path(g[key]).read_bytes())==g[key+'_sha256']
        sheets.extend(g['review_sheets']+[g['transition_sheet']])
    assert comparison['actual_proof_sha256']==rng['actual_proof_sha256']==focus['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert rng['comparison_sha256']==sha(COMPARE.read_bytes())
    sheets.extend([dict(path=comparison['review_sheet'],sha256=comparison['review_sheet_sha256']),dict(path=focus['sheet'],sha256=focus['sheet_sha256'])])
    assert len(sheets)==22
    for s in sheets:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        s.update(directly_viewed=True,finding='Complete actual Japanese/English exchange, four full speaker names, C281 scene transition, Lil/Camille portraits and normal return inspected. Eleven speeches and three headers remain native-only. Unmasked later differences retained.')
    assert stored['relocation_sha256']==control['relocation_sha256']==sha(RELOC.read_bytes())
    assert stored['all61_native_ink_planes_exact_to_already_viewed'] and len(control['final_dispatches'])==61 and len(control['normal_seeded_ends'])==25
    assert len(callers['all_command_maps'])==154 and len(callers['relative_operand_maps'])==56
    cg=comparison['groups'][0];rg=rng['groups'][0]
    assert cg['source_English_exits']==[16013,16016] and len(cg['later_RGB_differences'])==19 and cg['later_sample_count']==134
    assert cg['all_original_initializer_andexchange_results_equal'] and cg['all_UI_request_words_equal'] and cg['all_observed_whole_upper_scene_portrait_andheader_RGB_equal']
    assert all(cg['five_native_component_equality'].values()) and cg['whole_actors_equal']
    assert cg['final_PRNG_seeds']==[int('3456469704'),int('204362374')]
    assert rg['exit_English_phase']==3 and rg['final_English_phase']==2
    assert rg['C281_original_command_measurement']['source_duration']==rg['C281_original_command_measurement']['English_duration']==1
    assert rg['C281_original_command_measurement']['after_English_phase']==0
    assert rng['exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified']
    updated=deepcopy(old)
    for row,p in zip(updated['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['compiled_hex']==p['encoded_hex'] and row['source_hex']==p['source_hex']
        assert row['planned_English_markup']==p['planning_record']['english']=='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['logical_English']
        observations=[dict(version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        observed=row['id'] not in UNVISITED;assert bool(observations)==observed
        if observed:assert {o['version'] for o in observations}=={'clean_Japanese','English'} and all(o['speech']['complete_body_holds'] for o in observations)
        row.update(english=row['planned_English_markup'],actual_record_observed=observed,actual_source_andEnglish_observations=observations,
            native_only_unvisited_conditional=not observed,source_presentation_consumer_not_yet_approved=False,
            native_font_wrapping_stored_reference_actual_policy_andregistered_release_pending=False,
            stored_relocation_actual_transition_policy_andregistered_release_pending=False,
            frozen_policy_atomic_production_andregistered_release_still_pending=True)
        row['review']['formatting']=True
    assert Counter(r['decision'] for r in updated['records'])=={'revision':31,'retention':30}
    assert sum(bool(r['qa_waivers']) for r in updated['records'])==3
    for a,b in zip(old['records'],updated['records'],strict=True):
        assert a['logical_English']==b['logical_English'] and a['compiled_hex']==b['compiled_hex'] and a['qa_waiver_scope']==b['qa_waiver_scope'] and all(b['review'].values())
    for r in names['records']:
        r['review']['formatting']=True
        r.update(actual_B49_progressive_nameplate_verified=r['actor_ID'] in [0,2,5,9],native_only_unvisited_B49_header=r['actor_ID'] in [4,6,8],
            actual_B49_headers_andcatalogue_UI_still_pending=False,
            full207_catalogue_UI_custom_names_actual_headers_andnative_font_bounds_pending=False,
            full_catalogue_UI_custom_names_andother_contexts_still_pending=True)
    names.update(prior_review=str(OLD_NAMES),prior_review_sha256=sha(OLD_NAMES.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_headers_verified_actors=[0,2,5,9],native_only_header_actors=[4,6,8],actual_headers_catalogue_UI_custom_names_andfull207_review_pending=False,
        full207_catalogue_UI_custom_names_other_contexts_andthree_unvisited_headers_pending=True)
    evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW,Path(__file__)]}
    ROOT.mkdir(parents=True);save(NAMES,names)
    updated.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),
        all61_four_prose_gates_true_all_formatting_gates_false=False,all61_five_review_gates_true=True,
        english_is_logical_body_only_formatter_owns_source_selector_breaks_guards_andparity=False,
        english_is_canonical_source_selector_plus_logical_body_formatter_owns_breaks_guards_andparity=True,
        no_scene_captures_new_ROM_registered_layer_orcompletion_credit=False,
        actual_scene_proof=str(ACTUAL),actual_scene_proof_sha256=sha(ACTUAL.read_bytes()),
        source_English_comparison=str(COMPARE),source_English_comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurements_andlimits=str(RNG),RNG_measurements_andlimits_sha256=sha(RNG.read_bytes()),
        actual_review_sheets=sheets,all22_actual_review_sheets_directly_viewed=True,native_only_unvisited_speech_IDs=UNVISITED,
        actual_unique_speeches_each_language=50,source_whole_exchange_situation_voice_andindividual_retentions_rechecked_against_actual_panes=True,
        no_new_logical_prose_orcompiled_bytes_from_canonical_speaker_markup=True,
        actual_later_state_models_persistent_tasks_calendar_andwhole_actor_equal_RNG_and19_RGB_differences_retained=True,
        frozen_policy_atomic_production_andregistered_cumulative_integration_still_required=True,
        status='source-context-prose-native-stored-representative-actual-approved-policy-atomic-registered-release-pending')
    updated['evidence']=dict(updated['evidence'])|evidence|{str(NAMES):sha(NAMES.read_bytes())};save(OUT,updated)
    save(ROOT/'61_source_context_native_representative_actual_approved_policy_release_pending.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurement=str(RNG),RNG_measurement_sha256=sha(RNG.read_bytes()),focused_C281_transition=str(FOCUS),focused_C281_transition_sha256=sha(FOCUS.read_bytes()),
        directly_viewed_sheets=sheets,all61_individual_source_context_prose_andformat_gates_true=True,revisions=31,retentions=30,
        actual_two_runs_frames=48002,actual_speech_occurrences=100,actual_unique_speeches_eachlanguage=50,actual_complete_pages_eachlanguage=[50,50],actual_complete_holds=318,
        native_only_unvisited_speech_IDs=UNVISITED,native_all61_paragraphs61_pages_andseven_names_approved=True,
        observed119_of154_original_commands_eachlanguage=True,all154_structural_commands_retained=True,
        C281_original_effect_body_andtransition_complete_Lil_Camille_headers_andnormal_return_verified=True,
        no_FE_or_extra_page_no_invented_page_turn_claim=True,exact_three_QA_waivers22_infos_all_original_diagnostics_preserved=True,
        actual_exits=[16013,16016],normal_results=[[0,0],[0,0]],command_comparison_difference_rows=111,duration_difference_rows=18,
        later_RGB_differences=19,later_RGB_sample_count=134,final_PRNG_seeds=cg['final_PRNG_seeds'],English_exit_LCG_phase=3,English_final_LCG_phase=2,
        actual_later_five_components_andwhole_actor_equal_RNG_andRGB_differences_preserved=True,
        no_causal_every_call_future_state_orbroad_simulation_equivalence_claim=True,
        disclosed_opening_ROM_entry_fixture_not_natural_B49_activation_original_location_fullroute_orhardware=True,
        eleven_conditional_speeches_andthree_headers_not_claimed_as_actual_coverage=True,
        incidental_following_Trader_andtrade_UI_captures_not_new_editorial_credit=True,
        no_ROM_registry_orcompletion_credit_change=True,policy_atomic_registered_integration_pending=True,evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B49 formatting approved:61 decisions,50 actual speeches/language,318 complete holds,22 directly viewed sheets. Eleven conditional speeches native-only. Policy/atomic/integration pending;zero credit.')
