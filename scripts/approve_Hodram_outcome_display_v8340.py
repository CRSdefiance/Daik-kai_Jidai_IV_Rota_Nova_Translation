"""Approve six scoped display gates after direct native/actual review; preserve all later-state limits."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_display_review_v8340')
OLD=Path('translations/hodram_B47_B48_editorial_manuscript_v2.json')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/hodram_B47_B48_speaker_name_review_v1.json')
NAMES=Path('translations/hodram_B47_B48_speaker_name_review_v2.json')
ACTUAL={47:Path('work/analysis/Hodram_outcome_actual_v8335/B47/paired_actual_dialogue_headers_FE_flow_returns.json'),48:Path('work/analysis/Hodram_outcome_actual_v8335b/B48/paired_actual_dialogue_headers_FE_flow_returns.json')}
GEOMETRY=Path('work/analysis/Hodram_outcome_FE_geometry_v8338b/two_original_FE_paint_snapshots_four_exact_bitmap_palette_RGB_holds.json')
COMPARE=Path('work/analysis/Hodram_outcome_actual_comparison_v8337/two_paired_whole_outcomes_controls_scenes_returns_bounded_later_state.json')
LATER=Path('work/analysis/Hodram_outcome_later_differences_v8339/observed_later_RGB_andPRNG_differences_not_everyframe_causality.json')
STORED=Path('work/analysis/Hodram_outcome_stored_v8327/six_stored_bodies8_fresh16_reused_alignments_six_exact_native_pages.json')
REFERENCE=Path('work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists();old,names,geometry,compare,later,stored,reference=map(read,[OLD,OLD_NAMES,GEOMETRY,COMPARE,LATER,STORED,REFERENCE]);actual={k:read(p) for k,p in ACTUAL.items()}
    assert stored['manuscript_sha256']==sha(OLD.read_bytes()) and all(p['all_observed_complete_body_name_orFE_absent_header_holds_andnative_flow_pass'] and not p['unresolved'] for p in actual.values())
    assert geometry['all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model'] and geometry['focused_actual_frames']==8002
    assert compare['total_actual_frames']==40004 and [g['later_RGB_difference_count'] for g in compare['groups']]==[0,13]
    assert all(g['all_observed_script_entry_andreturn_PRNG_pairs_equal'] for g in later['groups']) and [g['final_PRNG_equal'] for g in later['groups']]==[True,False]
    assert all(all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] and [n['captain_ID'] for n in g['final_native_values']]==[1,1] for g in compare['groups'])
    sheets=[]
    for p in actual.values():
        sheets.extend(p['review_sheets'])
        for group in p['groups']:sheets.extend(group['transition_sheets'])
    sheets.extend(compare['review_sheets']);sheets.extend(later['review_sheets']);assert len(sheets)==10
    for sheet in sheets:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    rows=[];totalholds=0
    for original in old['records']:
        row=deepcopy(original);observations=[]
        for group in actual[row['block']]['groups']:
            speech=next(s for s in group['speeches'] if s['id']==row['id']);assert speech['complete_holds'] and speech['pages']==1 and speech['source_selector']==row['source_selector']
            for hold in speech['complete_holds']:assert sha(Path(hold['capture']).read_bytes())==hold['sha256']
            observations.append(dict(version=group['version'],speech=deepcopy(speech),actual_proof=str(ACTUAL[row['block']]),actual_proof_sha256=sha(ACTUAL[row['block']].read_bytes()),scope='Complete initialized original-opening whole-script fixture;not natural optional activation ororiginal location.'))
            totalholds+=len(speech['complete_holds'])
        row['review']['formatting']=True;row.update(actual_display_observations=observations,scoped_native_stored_andactual_display_approved=True,display_approval=str(ROOT/'display_review_receipt.json'),actual_individually_observed_in_disclosed_whole_script_fixtures=True,
            actual_original_optional_activation=False,actual_original_event_location_orouter_eligibility_not_claimed=True,source_complete_controls_andtwo_normal_returns_bound=True,
            all_stored_controls_actual_effects_headers_FE_geometry_policy_andregistered_release_pending=False,frozen_policy_atomic_production_registered_integration_andcompletion_credit_pending=True,
            previous_pending_flags_historical_when_superseded_by_current_five_review_gates=True,source_prose_orcompletion_credit_added=False)
        assert row['english']==original['english'] and all(row['review'].values());rows.append(row)
    assert totalholds==100 and len(rows)==6
    ROOT.mkdir(parents=True);names=deepcopy(names)
    for row in names['records']:
        assert row['actor_ID']==2;row['review']['formatting']=True;row.update(actual_new_scene_headers_pending=False,actual_Lil_Argot_headers_observed_in_both_versions_both_outcomes=True,display_review=str(ROOT/'display_review_receipt.json'),
            no_new_name_asset_full_catalogue_UI_orcustomnames_approval=True)
    names.update(predecessor_name_review=str(OLD_NAMES),predecessor_name_review_sha256=sha(OLD_NAMES.read_bytes()),scope='Lil Argot in B47/B48 only;FE notice has no personal speaker header.',all_scoped_name_five_gates_true=True)
    save(NAMES,names);doc=deepcopy(old);doc.update(records=rows,names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        all_six_four_prose_gates_true_all_formatting_gates_false=False,all_six_formatting_gates_still_false=False,all_six_five_perrecord_review_gates_true=True,
        display_review=str(ROOT/'display_review_receipt.json'),actual_whole_scene_frames=40004,actual_focused_FE_boundary_frames=8002,total_new_actual_frames=48006,actual_complete_body_header_orFE_absent_header_holds=100,
        native_FE_source_note_andFI_display_complete_andreviewed=True,later_actual_scope_limits=dict(proof=str(LATER),proof_sha256=sha(LATER.read_bytes()),
            B47_later_RGB_equal93of93_andfinal_PRNG_equal=True,B48_later_RGB_equal80of93_andfinal_PRNG_different=True,all_original_script_command_boundary_PRNG_pairs_equal=True,
            all_five_checked_final_native_components_andwhole_actors_equal_withcaptain1=True,source_B48_end4495_English4494_both_type0_value0=True,
            actual_B48_later_differences_prompt_blink_menu_highlight_and_sailing_clouds_directly_viewed=True,no_everyframe_cause_orfuture_outcome_broad_simulation_fullroute_orhardware_claim=True),
        frozen_policy_atomic_production_registered_integration_andcompletion_credit_pending=True,status='all-six-scoped-five-gate-review-pass-frozen-policy-atomic-registered-integration-pending')
    save(DOC,doc)
    evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,GEOMETRY,COMPARE,LATER,STORED,REFERENCE,*ACTUAL.values(),Path(__file__)]}
    save(ROOT/'display_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),name_review=str(NAMES),name_review_sha256=sha(NAMES.read_bytes()),all_six_five_perrecord_review_gates_true=True,revisions=3,individually_justified_retentions=3,
        all10_actual_comparison_andlater_difference_sheets_directly_viewed=sheets,all_six_original_native_English_body_previews_previously_viewed=True,actual_complete_body_header_orFE_absent_header_holds=100,
        six_source_and_six_revised_actual_single_pages=True,all15_original_exchange_commands_observed_perversion=True,complete_both_normal_ends_andall_original_effect_bodies_preserved=True,
        original_FE_two_paint_snapshots_four_actual_VRAM_palette_RGB_holds_bound=True,scoped_Lil_Argot_actual_headers_approved_no_new_name_asset=True,
        later_difference_characterization='B48 frame4870 differs in the A prompt;5410 and7030 in menu highlight;9550through10001 in lower-screen sailing clouds. All script-boundary seeds match,but final B48 seeds differ. This is measured scope,not a causal explanation orfuture-outcome equivalence.',
        full_measured_command_UI_duration_native_components_actor_captain_rawcalendar_PRNG_andRGB_scope=compare['groups'],
        six_fullruns_orfour_whole_scene_plus_two_focused_counts=dict(whole_scene_runs=4,whole_scene_frames=40004,focused_boundary_runs=2,focused_boundary_frames=8002,total_actual_frames=48006),
        reference_ROM_is_research_only_not_registered_orpromoted=True,frozen_policy_independent_atomic_registered_integration_andcompletion_credit_pending=True,
        all_prior_ROMs_drafts_translations_executed_producers_failures_andproofs_preserved=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    print('Hodram6:v3/namesv2 allfive scopedgates true;100actualcompleteholds/48006frames/10viewedsheets/originalFE VRAM+palette bound.LaterB48timing/RNG/13RGBdifferences preserved.Policy/atomic/integration pending;zero credit.')
