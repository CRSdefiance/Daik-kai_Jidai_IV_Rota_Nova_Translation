"""Approve source/context/prose/native/stored/actual formatting; production and integration remain pending."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_actual_approval_v7953')
OLD=Path('translations/rafael_B46_editorial_manuscript_v2.json')
OUT=Path('translations/rafael_B46_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/rafael_B46_speaker_name_review_v1.json')
NAMES=Path('translations/rafael_B46_speaker_name_review_v2.json')
ACTUAL=Path('work/analysis/Rafael_B46_actual_v7948/four_runs24_unique_speeches58_occurrences_two_choices_actual_body_name_FE_return_audit.json')
MENU=Path('work/analysis/Rafael_B46_menu_actual_v7950c/four_actual_menus12_full_owned_backing_andhighlight_samples.json')
COMPARE=Path('work/analysis/Rafael_B46_actual_comparison_v7949/both_choices29_scene_pairs_full_measured_timing_RNG_components_RGB_limits.json')
RNG=Path('work/analysis/Rafael_B46_waits_v7951/both_choices_original_wait_code_measured_RNG_phases_andlater_limits.json')
VIEW=Path('work/analysis/Rafael_B46_actual_view_v7952/48_unique_actual_panes14_review_sheets_58_occurrences_preserved.json')
RELOC=Path('work/analysis/Rafael_B46_relocation_v7938/one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json')
STORED=Path('work/analysis/Rafael_B46_stored_v7939/all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json')
CONTROL=Path('work/analysis/Rafael_B46_relocated_controls_v7940/24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json')
CALLERS=Path('work/analysis/Rafael_B46_reference_census_v7943/all37_commands_four_relative_sites_two_choices_EV0_entry_shipped_callers.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NAMES.exists()
    old,names,actual,menu,comparison,rng,view,reloc,stored,control,callers=map(read,[OLD,OLD_NAMES,ACTUAL,MENU,COMPARE,RNG,VIEW,RELOC,STORED,CONTROL,CALLERS])
    assert not actual['unresolved'] and not menu['unresolved'] and len(actual['groups'])==4
    assert sum(len(g['speech_observations']) for g in actual['groups'])==58 and sum(g['complete_body_holds'] for g in actual['groups'])==214
    assert sum(g['incomplete_sampled_holds'] for g in actual['groups'])==0
    assert len(view['unique_actual_page_references'])==48 and len(view['sheets'])==14
    sheets=[]
    for s in view['sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append(dict(**s,directly_viewed=True,finding='Complete original source/English text, full names and selected native displays reviewed. Keep source highlight-off and later simulation differences; no natural event or full-route claim.'))
    assert stored['relocation_sha256']==control['relocation_sha256']==sha(RELOC.read_bytes())
    assert len(control['final_dispatches'])==24 and len(control['normal_seeded_ends'])==25
    assert len(callers['all_command_maps'])==37 and len(callers['typed_choice_records'][0]['label_references'])==2
    assert rng['exact_RNG_state_future_random_outcomes_orfull_simulation_equality_NOT_verified']
    assert [(g['choice'],g['later_RGB_differences'],g['later_samples']) for g in rng['groups']]==[('accept',41,113),('decline',96,173)]
    assert menu['source_highlight_off_samples']==[dict(version='clean_Japanese',choice='accept',frame=4930,logical_selected_option=0)]
    for g in actual['groups']:
        selected=0 if g['choice']=='accept' else 1
        assert g['actual_unique_speeches']==(22 if selected==0 else 7) and g['native_terminal_result']==[0,selected]
        assert g['actual_menu_pair']['native_result']==[2,selected]
        terminal=read(f"work/analysis/Rafael_B46_scene_runs_v7945/route0_{g['version']}_{g['choice']}/terminal.json")
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        assert sha(Path(g['capture_report']).read_bytes())==g['capture_report_sha256']
        assert sha(Path(g['observer_report']).read_bytes())==g['observer_report_sha256']
    updated=deepcopy(old)
    for row in updated['records']:
        observations=[dict(version=g['version'],choice=g['choice'],speech=s) for g in actual['groups'] for s in g['speech_observations'] if s['id']==row['id']]
        assert {r['version'] for r in observations}=={'clean_Japanese','English'}
        assert all(s['speech']['complete_body_holds'] for s in observations)
        canonical=row['planned_English_markup']
        assert canonical=='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+row['logical_English']
        row.update(english=canonical,actual_record_observed=True,actual_source_andEnglish_observations=observations,
            source_presentation_consumer_not_yet_approved=False,current_effective_body_dispatch_andcatalogue_pending=False,
            source_native_names_roles_controls_display_andcurrent_comparison_pending=False)
        row['review']['formatting']=True
    for row in updated['typed_choice_records']:
        observations=[dict(version=g['version'],choice=g['choice'],sample=s,label=l)
            for g in menu['groups'] for s in g['samples'] for l in s['labels'] if l['option_index']==row['option_index']]
        assert len(observations)==12 and all(o['label']['full_visible_black_glyph_mask_andblank_guards_equal'] for o in observations)
        row.update(actual_record_observed=True,actual_source_andEnglish_menu_observations=observations,
            current_native_menu_getters_geometry_outcome_andactual_pending=False,
            source_native_menu_owner_returns_branches_geometry_andcurrent_comparison_pending=False,
            actual_view_backing_highlights_ordinary_input_selection_andbranch_return_pending=False,
            actual_menu_highlight_phase_limit=menu['source_highlight_off_samples'])
        row['review']['formatting']=True
    assert Counter(r['decision'] for r in updated['records']+updated['typed_choice_records'])=={'revision':7,'retention':19}
    for before,after in zip(old['records']+old['typed_choice_records'],updated['records']+updated['typed_choice_records'],strict=True):
        assert before['logical_English']==after['logical_English'] and before['compiled_hex']==after['compiled_hex']
        assert all(after['review'].values()) and after['source_hex']==before['source_hex']
    for r in names['records']:
        r.update(actual_B46_progressive_nameplate_verified=True,actual_B46_headers_andother_consumer_UI_pending=False,
            full_catalogue_UI_andother_contexts_still_pending=True)
    names.update(prior_review=str(OLD_NAMES),prior_review_sha256=sha(OLD_NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),actual_three_progressive_names_verified=True,
        full207_name_role_alias_review_active=True,actual_full_catalogue_UI_not_newly_verified=True)
    evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,ACTUAL,MENU,COMPARE,RNG,VIEW,RELOC,STORED,CONTROL,CALLERS,Path(__file__)]}
    ROOT.mkdir(parents=True);save(NAMES,names)
    updated.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),names_packet=str(NAMES),
        all26_five_review_gates_true=True,all26_formatting_gates_false=False,formatting_review_pending=False,
        actual_scene_proof=str(ACTUAL),actual_scene_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_menu_proof=str(MENU),actual_menu_proof_sha256=sha(MENU.read_bytes()),
        source_English_comparison=str(COMPARE),source_English_comparison_sha256=sha(COMPARE.read_bytes()),
        RNG_measurements_andlimits=str(RNG),RNG_measurements_andlimits_sha256=sha(RNG.read_bytes()),
        actual_review_sheets=sheets,all48_unique_actual_panes14_sheets_directly_viewed=True,
        no_new_prose_orcompiled_bytes_from_canonical_speaker_markup=True,
        accept22_decline7_now_actual_not_only_native_compositions=True,
        historical_pending_flags_superseded_by_source_native_stored_actual_approval=True,
        source_menu_off_sample_andall_later_simulation_differences_retained=True,
        full_RNG_future_outcome_orbroad_simulation_equality_not_claimed=True,
        status='source-context-prose-native-stored-actual-approved-policy-atomic-registered-release-pending',
        frozen_policy_atomic_production_andregistered_cumulative_integration_still_required=True)
    updated['evidence']=dict(updated['evidence'])|evidence|{str(NAMES):sha(NAMES.read_bytes())}
    save(OUT,updated)
    save(ROOT/'26_source_context_native_actual_approved_policy_release_pending.json',dict(
        manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),actual_menu_proof=str(MENU),actual_menu_proof_sha256=sha(MENU.read_bytes()),
        comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),RNG_measurement=str(RNG),RNG_measurement_sha256=sha(RNG.read_bytes()),
        directly_viewed_sheets=sheets,all26_individual_source_context_prose_andformat_gates_true=True,revisions=7,retentions=19,
        actual_four_runs_frames=64004,actual_speech_occurrences=58,actual_unique_speeches_eachlanguage=24,actual_complete_holds=214,
        actual_accept_exits=[9295,9294],actual_decline_exits=[5695,5696],
        actual_menu_results_accept=[2,0],actual_menu_results_decline=[2,1],normal_results_accept=[0,0],normal_results_decline=[0,1],
        all37_original_commands_observed_across_both_paths_each_language=True,
        source_only_menu4930_highlight_off_andcrosslanguage_phase_limit_retained=True,
        later_RGB_difference_counts=[41,96],later_RGB_sample_counts=[113,173],
        final_PRNG_seeds=[[1622437796,3229979821],[3730749937,3562773357]],
        actual_later_models_persistent_objects_actors_andaccept_calendar_differences_preserved=True,
        no_causal_every_call_future_state_orbroad_simulation_equivalence_claim=True,
        disclosed_opening_ROM_entry_fixture_not_natural_B46_activation_original_location_fullroute_orhardware=True,
        unused_native_result2_3_FFFFFFFF_cases_not_individual_gameplay_coverage=True,
        incidental_B127_andSailor_sailing_prose_captures_not_new_editorial_credit=True,
        no_ROM_registry_orcompletion_credit_change=True,policy_atomic_registered_integration_pending=True,
        evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('B46 source/native/stored/actual formatting approved:26 records/7 revisions19 retentions,58 occurrences214 holds,14 sheets. All measured limits retained. Policy/atomic/integration pending;no credit.')
