"""Approve B50 formatting after all28 actual pages,original controls andbounded risk samples."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_actual_approval_v8161')
OLD=Path('translations/rafael_B50_editorial_manuscript_v2.json')
OUT=Path('translations/rafael_B50_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/rafael_B50_speaker_name_review_v2.json')
NAMES=Path('translations/rafael_B50_speaker_name_review_v3.json')
ACTUAL=Path('work/analysis/Rafael_B50_actual_v8156/paired_source_English_all28_pages_three_names_4821_departure_andreturn.json')
COMPARE=Path('work/analysis/Rafael_B50_actual_comparison_v8157/all_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
RNG=Path('work/analysis/Rafael_B50_waits_v8158/original_wait_code_measured_4821_departure_RNG_phases_andlater_limits.json')
FOCUS=Path('work/analysis/Rafael_B50_actual_focus_v8160/focused_actual_picture_return_andbounded_later_state_risk.json')
RELOC=Path('work/analysis/Rafael_B50_relocation_v8146/one_block28_speeches_zero_relative_cases_exact_full_inverse.json')
STORED=Path('work/analysis/Rafael_B50_stored_v8147/all28_stored_bodies_full_native_alignment_and28_exact_viewed_pages.json')
CONTROL=Path('work/analysis/Rafael_B50_relocated_controls_v8148/28_stored_dispatches_nine_controls_zero_relatives_relocated4821_25_seeded_ends.json')
CALLERS=Path('work/analysis/Rafael_B50_reference_census_v8153/all37_commands_zero_relative_sites28_speeches_4821_EV0_entry_shipped_callers.json')
PLAN=Path('work/analysis/Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json')
REVIEW=Path('work/analysis/Rafael_B50_native_review_v8145/28_native_pages3_names_two_scoped_warnings18_infos_wrap_review.json')
ASSESSMENT=(
    'All28 complete source/English single pages,184 body/name holds,three names,FA2/FI1,all37 original commands plus10 original initializers,Red Dye card appearance/hide,departure andnormal type0/value0 return pass. '
    'Both original effect bodies execute in the core;4821 lasts60frames,A000240,4720zero,468188 in both. No opaque effect bridge,state forcing,controller retiming or altered control bytes. '
    'First phase difference is sourceoffset350:237/241frames and57/58LCGsteps. Exits10822/10824,exitEnglishphase+2,finalphase-10,seeds3888306843/2225786845,35comparison rows and11duration differences remain. '
    'All28 upper-scene/portrait/header RGB pairs and47 original command results/UIrequests match. Seventeen of87 later fullRGB samples differ. '
    'Eight focused phase samples reproduce every earlier observer row except output paths,all eight framebuffers andfinal wholeRAM exactly for each language. '
    'The first seven samples3970/5170/5770/10930/11890/15310/15550 have equal sampled state,models,persistentobjects,tasks,calendar andwholeactors;these include scene return andsubsequent tutorial/departure. '
    'At16000 underway,models andpersistentobjects differ:two fleetbytes,one shipbyte,105actorbytes andtwo townbytes. Company/items/goods,state/tasks/calendar remain equal. '
    'This bounds an observed later divergence after the reviewed scene rather than proving its complete cause or future simulation equivalence. Rawcalendar185/[0,3,41] remains uninterpreted. '
    'Retain all timing/RNG/component/byte/RGB data for the later older-record technical re-audit;do not manipulate input orseed to erase it. No concrete B50 clipping,missing-name,picture/control/return defect remains. '
    'Formatting may proceed to frozen policy andindependent atomic registered integration. This disclosed initialized Lisbon fixture is not natural event50 eligibility,earned item/progress,original scene location,full route orhardware coverage;incidental B127/tutorial/resource prose gets no newcredit.'
)

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES.exists()
    old,names,actual,comparison,rng,focus,reloc,stored,control,callers,plan,review=map(read,[OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW])
    assert not actual['unresolved'] and actual['actual_total_frames']==32002 and actual['native_only_unvisited_speech_IDs']==[]
    assert len(actual['groups'])==2 and sum(g['complete_body_holds'] for g in actual['groups'])==184
    sheets=[]
    for g in actual['groups']:
        assert g['actual_unique_speeches']==g['actual_complete_native_pages']==28 and g['observed_original_exchange_commands']==37 and len(g['command_pairs'])==47
        assert not g['original_structural_commands_not_selected'] and not g['native_only_unvisited_speech_IDs']
        assert g['native_terminal_result']==[0,0] and not g['incomplete_sampled_holds'] and not g['unidentified_trace_rows']
        assert not g['unreturned_following_dialogues'] and not g['later_fixture_reentry_frames']
        assert sorted({s['source_selector'] for s in g['speech_observations']})==[0,2,9]
        assert all(s['native_page_count']==1 and not s['ordinary_page_transitions'] for s in g['speech_observations'])
        terminal=read(f"work/analysis/Rafael_B50_scene_runs_v8155/route0_{g['version']}/terminal.json")
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        for key in ['capture_report','observer_report']:assert sha(Path(g[key]).read_bytes())==g[key+'_sha256']
        sheets.extend(g['review_sheets']+[g['transition_sheet']])
    assert comparison['actual_proof_sha256']==rng['actual_proof_sha256']==focus['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert rng['comparison_sha256']==focus['comparison_sha256']==sha(COMPARE.read_bytes())
    sheets.extend([dict(path=comparison['review_sheet'],sha256=comparison['review_sheet_sha256']),dict(path=focus['sheet'],sha256=focus['sheet_sha256'])])
    assert len(sheets)==14
    for s in sheets:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        s.update(directly_viewed=True,finding='Complete exchange,three full names,surname/given substitutions,Red Dye card appearance/hide,departure andnormal return viewed. Later tutorial/sailing differences preserved;no inferred unnamed celebration ornew relationship.')
    assert stored['relocation_sha256']==control['relocation_sha256']==sha(RELOC.read_bytes())
    assert stored['all28_native_ink_planes_exact_to_already_viewed'] and len(control['final_dispatches'])==28 and len(control['normal_seeded_ends'])==25
    assert len(callers['all_command_maps'])==37 and not callers['relative_operand_maps'] and not callers['relocated_relative_cases']
    assert len(review['all_original_infos'])==18 and len(review['narrow_warning_exceptions'])==2
    cg,rg=comparison['groups'][0],rng['groups'][0]
    assert cg['source_English_exits']==[10822,10824] and len(cg['later_RGB_differences'])==17 and cg['later_sample_count']==87
    assert len(cg['command_comparison_differences'])==35 and len(cg['duration_differences'])==11
    assert cg['all_original_initializer_andexchange_results_equal'] and cg['all_UI_request_words_equal'] and cg['all_observed_whole_upper_scene_portrait_andheader_RGB_equal']
    assert cg['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True) and not cg['whole_actors_equal']
    assert cg['final_PRNG_seeds']==[int('3888306843'),int('2225786845')] and rg['exit_English_phase']==2 and rg['final_English_phase']==-10
    assert rng['exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified']
    assert focus['total_B50_actual_frames']==64004 and len(focus['sampled_phase_comparisons'])==8
    assert all(all(r['component_equality'].values()) for r in focus['sampled_phase_comparisons'][:-1])
    assert focus['sampled_phase_comparisons'][-1]['frame']==16000 and not focus['sampled_phase_comparisons'][-1]['component_equality']['models']
    for g in focus['groups']:
        assert g['original_andrepeat_all_observer_rows_exact_except_output_paths'] and g['all_eight_capture_PNGs_framebuffers_andfinal_whole_RAM_exact_to_first_run']
        assert [c['returned']-c['start'] for c in g['controls']]==[60,240,0,88]
    updated=deepcopy(old)
    for row,p in zip(updated['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['compiled_hex']==p['encoded_hex'] and row['source_hex']==p['source_hex']
        assert row['planned_English_markup']==p['planning_record']['english']=='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['logical_English']
        observations=[dict(version=g['version'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        assert {o['version'] for o in observations}=={'clean_Japanese','English'} and len(observations)==2
        assert all(o['speech']['complete_body_holds'] for o in observations)
        row.update(english=row['planned_English_markup'],actual_record_observed=True,actual_source_andEnglish_observations=observations,
            native_only_unvisited_conditional=False,source_presentation_consumer_not_yet_approved=False,
            native_font_wrapping_stored_reference_actual_policy_andregistered_release_pending=False,
            stored_relocation_actual_transition_policy_andregistered_release_pending=False,
            frozen_policy_atomic_production_andregistered_release_still_pending=True)
        row['review']['formatting']=True
    assert Counter(r['decision'] for r in updated['records'])=={'revision':13,'retention':15}
    assert sum(bool(r['qa_waivers']) for r in updated['records'])==2
    for a,b in zip(old['records'],updated['records'],strict=True):
        assert a['logical_English']==b['logical_English'] and a['compiled_hex']==b['compiled_hex'] and a['qa_waiver_scope']==b['qa_waiver_scope'] and all(b['review'].values())
    for r in names['records']:
        assert r['actor_ID'] in [0,2,9];r['review']['formatting']=True
        r.update(actual_B50_progressive_nameplate_verified=True,native_only_unvisited_B50_header=False,
            actual_B50_headers_andcatalogue_UI_still_pending=False,
            full207_catalogue_UI_custom_names_actual_headers_andnative_font_bounds_pending=False,
            full_catalogue_UI_custom_names_andother_contexts_still_pending=True)
    names.update(prior_review=str(OLD_NAMES),prior_review_sha256=sha(OLD_NAMES.read_bytes()),actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_headers_verified_actors=[0,2,9],native_only_header_actors=[],actual_headers_catalogue_UI_custom_names_andfull207_review_pending=False,
        full207_catalogue_UI_custom_names_andother_contexts_pending=True)
    evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,ACTUAL,COMPARE,RNG,FOCUS,RELOC,STORED,CONTROL,CALLERS,PLAN,REVIEW,Path(__file__)]}
    ROOT.mkdir(parents=True);save(NAMES,names)
    updated.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),
        all28_four_prose_gates_true_all_formatting_gates_false=False,all28_five_review_gates_true=True,
        english_is_logical_body_only_formatter_owns_source_selector_breaks_guards_andparity=False,
        english_is_canonical_source_selector_plus_logical_body_formatter_owns_breaks_guards_andparity=True,
        no_scene_captures_new_ROM_registered_layer_orcompletion_credit=False,
        actual_scene_proof=str(ACTUAL),actual_scene_proof_sha256=sha(ACTUAL.read_bytes()),
        source_English_comparison=str(COMPARE),source_English_comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurements_andlimits=str(RNG),RNG_measurements_andlimits_sha256=sha(RNG.read_bytes()),
        actual_review_sheets=sheets,all14_actual_review_sheets_directly_viewed=True,native_only_unvisited_speech_IDs=[],
        actual_unique_speeches_each_language=28,source_whole_exchange_situation_voice_andindividual_retentions_rechecked_against_actual_panes=True,
        no_new_logical_prose_orcompiled_bytes_from_canonical_speaker_markup=True,
        actual_bounded_risk_assessment=ASSESSMENT,focused_risk_proof=str(FOCUS),focused_risk_proof_sha256=sha(FOCUS.read_bytes()),
        frozen_policy_atomic_production_andregistered_cumulative_integration_still_required=True,
        status='source-context-prose-native-stored-all28-actual-approved-policy-atomic-registered-release-pending')
    updated['evidence']=dict(updated['evidence'])|evidence|{str(NAMES):sha(NAMES.read_bytes())};save(OUT,updated)
    save(ROOT/'28_source_context_native_all_actual_approved_policy_release_pending.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurement=str(RNG),RNG_measurement_sha256=sha(RNG.read_bytes()),focused_picture_transition_andrisk=str(FOCUS),focused_picture_transition_andrisk_sha256=sha(FOCUS.read_bytes()),
        directly_viewed_sheets=sheets,all28_individual_source_context_prose_andformat_gates_true=True,revisions=13,retentions=15,
        actual_initial_two_runs_frames=32002,focused_risk_two_runs_frames=32002,actual_total_frames=64004,
        actual_speech_occurrences_initial_runs=56,actual_unique_speeches_eachlanguage=28,actual_complete_pages_eachlanguage=[28,28],actual_complete_holds=184,
        native_only_unvisited_speech_IDs=[],native_all28_paragraphs28_pages_andthree_names_approved=True,
        observed_all37_original_commands_eachlanguage_and10_initializers=True,
        original_effect_bodies_4821_A000_4720_4681_picture_hide_departure_andnormal_return_verified=True,
        no_FE_or_extra_page_no_invented_page_turn_claim=True,exact_two_QA_waivers18_infos_all_original_diagnostics_preserved=True,
        actual_exits=[10822,10824],normal_results=[[0,0],[0,0]],command_comparison_difference_rows=35,duration_difference_rows=11,
        later_RGB_differences=17,later_RGB_sample_count=87,final_PRNG_seeds=cg['final_PRNG_seeds'],English_exit_LCG_phase=2,English_final_LCG_phase=-10,
        bounded_risk_assessment=ASSESSMENT,all_risk_measurements_preserved_for_later_technical_reaudit=True,
        no_causal_every_call_future_state_orbroad_simulation_equivalence_claim=True,
        disclosed_opening_ROM_entry_fixture_not_natural_B50_activation_original_location_fullroute_orhardware=True,
        incidental_following_B127_tutorial_resource_andtown_prose_not_new_editorial_credit=True,
        no_ROM_registry_orcompletion_credit_change=True,policy_atomic_registered_integration_pending=True,evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B50 formatting approved:28 decisions/all28 actual speeches/language,184complete holds,14viewed sheets. Bounded later differences retained. Policy/atomic/integration pending;zero credit.')
