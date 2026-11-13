"""Approve scoped body/name presentation after direct review; policy/release remain pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_display_review_v8284')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v3.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v3.json')
OUT=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v4.json')
NOUT=Path('translations/hodram_B137_B45_B46_speaker_name_review_v4.json')
STORED=Path('work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json')
COMPARE=Path('work/analysis/Hodram_actual_comparison_v8283/three_paired_whole_exchanges_controls_scenes_returns_bounded_later_state.json')
SOURCE_PICTURE=Path('work/analysis/Hodram_B46_pigment_v8190b/original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json')
PATHS=[Path(f'work/analysis/Hodram_actual_v8282/B{b}/paired_actual_dialogue_headers_flow_returns.json') for b in [137,45,46]]
SCOPE='Complete native216x64/four-row/one-page body andstyle11 name masks plus actual holds in whole-script initialized Hodram opening fixtures;not natural optional activation,original event location,earned progress,full route orhardware.'

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not NOUT.exists()
    original,names,stored,comparison=map(read,[DOC,NAMES,STORED,COMPARE]);actual=[read(p) for p in PATHS]
    assert all(not p['unresolved'] and p['all_observed_complete_body_name_holds_andnative_flow_pass'] for p in actual)
    groups=[g for p in actual for g in p['groups']];assert sum(g['actual_frames'] for g in groups)==100006
    assert all(g['normal_return'] and not g['unvisited_conditional_text_IDs'] for g in groups)
    assert sum(len(g['speeches']) for g in groups)==56
    sheets=[s for p in actual for s in p['review_sheets']]+comparison['review_sheets'];assert len(sheets)==12
    for sheet in sheets:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert len(comparison['groups'])==3
    for g in comparison['groups']:
        assert all(g['five_native_component_equality'].values()) and g['whole_actors_equal'] and len(set(g['final_PRNG_seeds']))==1
        assert not g['UI_request_differences'] and g['later_RGB_difference_count']==0 and g['following_commands_equal']
        assert not g['no_common_complete_hold'] and all(s['upper_scene_portrait_RGB_equal'] and s['complete_header_region_RGB_equal'] for s in g['scene_pairs'])
    assert sum(len(g['later_RGB_comparisons']) for g in comparison['groups'])==532
    assert [g['final_native_values'][0]['captain_ID'] for g in comparison['groups']]==[0,1,1]
    resource=comparison['groups'][2]['original4800_4700_actual'];assert resource['descriptor']==[0,181,1,5] and resource['layout']==[0,0,0]
    doc=deepcopy(original);name_doc=deepcopy(names);ROOT.mkdir(parents=True)
    for row in doc['records']:
        old=next(r for r in original['records'] if r['id']==row['id']);assert all(old['review'][k] for k in ['source','context','localization','naturalness']) and not old['review']['formatting']
        observations=[dict(version=g['version'],proof=str(p),proof_sha256=sha(p.read_bytes()),speech=next(s for s in g['speeches'] if s['id']==row['id'])) for p,a in zip(PATHS,actual,strict=True) for g in a['groups'] if g['block']==row['block']]
        assert len(observations)==2 and all(o['speech']['complete_holds'] and o['speech']['nameholds'] for o in observations)
        font=next(r for r in stored['records'] if r['id']==row['id'])
        row['historical_pending_flags_superseded_v8284']={k:row.pop(k) for k in ['formatting_actual_andregistered_release_pending','native_font_wrapping_stored_reference_actual_policy_andregistered_release_pending']}
        row['review']['formatting']=True;row.update(actual_display_observations=observations,formatting_scope=SCOPE,
            integrated_reference_pending=font['target_reference'],final_stored_hex=font['stored_hex'],
            complete_native_stored_proof=str(STORED),complete_native_stored_proof_sha256=sha(STORED.read_bytes()),
            all_five_per_record_editorial_andformatting_gates_true=True,
            frozen_policy_atomic_production_registered_integration_andcompletion_credit_pending=True,
            individually_activated_in_registered_current_build=False,source_prose_orcompletion_credit_added=False)
        assert all(row[k]==old[k] for k in ['english','logical_English','source_hex','current_hex','source_reference','current_reference','localization_note','retention_reason','decision','compiled_hex','qa_waivers'])
    doc['historical_pending_flags_superseded_v8284']={k:doc.pop(k) for k in ['all28_four_prose_gates_true_all_formatting_gates_false','no_scene_captures_new_ROM_registered_layer_orcompletion_credit']}
    doc.update(prior_manuscript=str(DOC),prior_manuscript_sha256=sha(DOC.read_bytes()),
        status='source-context-prose-native-stored-actual-display-approved-pending-frozen-policy-atomic-registered-integration',
        all28_five_review_gates_true=True,all16_revisions12_justified_retentions_andtwo_warning_waivers_unchanged=True,
        native_wrapping_andactual_display_review=str(ROOT/'display_review_receipt.json'),formatting_scope=SCOPE,
        actual_scene_comparison=str(COMPARE),actual_scene_comparison_sha256=sha(COMPARE.read_bytes()),new_emulator_runs=6,new_actual_frames=100006,
        new_credit=0,no_registered_release_orcompletion_credit_added=True)
    for row in name_doc['records']:
        actor=row['actor_ID'];observations=[dict(block=g['block'],version=g['version'],id=s['id'],name=s['name'],holds=s['nameholds']) for g in groups for s in g['speeches'] if s['source_selector']==actor]
        assert observations and all(o['name']==row['name'] and o['holds'] for o in observations)
        row['historical_pending_flags_superseded_v8284']={k:row.pop(k) for k in ['actual_new_scene_headers_not_yet_observed','native_full_glyph_planes_bounds_andactual_headers_pending','actual_Hodram_B137_B45_B46_headers_still_pending']}
        row['review']['formatting']=True;row.update(actual_header_observations=observations,actual_headers_approved_in_disclosed_Hodram_fixtures=True,
            formatting_scope=SCOPE,individually_activated_in_registered_current_build=False,new_name_asset_change=False,new_name_or_dialogue_credit=0)
        if actor==16:
            historical=['current_name','current_surname','possible_minimal_order_correction','finding','required_followup','name_asset_andfive_SC2_mentions_still_pending']
            row['historical_pre_registration_surname_findings_superseded_v8284']={k:row.pop(k) for k in historical if k in row}
            row.update(current_name='Gerhard Adernkatz',current_surname='Adernkatz',
                finding='The registered V8259 correction is retained;fresh current getters andactual Hodram headers show Gerhard Adernkatz.',
                required_registered_dependency_fulfilled=True,name_asset_andfive_SC2_mentions_still_pending=False)
    name_doc['historical_pending_flags_superseded_v8284']={k:name_doc.pop(k) for k in ['surname_asset_registered_in_V8259_actual_Hodram_headers_pending','six_current_individual_retentions_no_new_asset_all_Hodram_formatting_gates_pending']}
    name_doc.update(prior_review=str(NAMES),prior_review_sha256=sha(NAMES.read_bytes()),
        six_current_individual_retentions_all_five_scoped_review_gates_true=True,
        actual_Hodram_headers_directly_viewed_andcomplete_native_masks_pass=True,
        full207_names_roles_aliases_catalogue_customnames_andwider_PortWorker_consumers_still_open=True,
        no_name_asset_ROM_registry_orcompletion_credit_change=True,display_review=str(ROOT/'display_review_receipt.json'))
    save(OUT,doc);save(NOUT,name_doc)
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,NAMES,STORED,COMPARE,SOURCE_PICTURE,*PATHS,Path(__file__)]}
    save(ROOT/'display_review_receipt.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),name_review=str(NOUT),name_review_sha256=sha(NOUT.read_bytes()),
        all28_original_source_current_logical_prose_reasons_compiled_bodies_andwaivers_unchanged=True,
        revised=16,retained=12,all28_five_per_record_gates_true=True,six_names_retained_all_scoped_formatting_gates_true=True,
        actual_complete_speech_observations_both_versions=56,actual_complete_body_andname_holds_both_versions=262,
        all28_source_andrevised_pages_andsix_speaker_headers_directly_viewed=True,all12_actual_review_sheets=sheets,
        Red_Dye_item181_card_icon_full_label_andMystery_Item_panel_show_then_clear_directly_viewed=True,
        source_original4800_layout0_and4700_hide_not_Rafael4821_4720=True,resource_observation=resource,
        all_original_return_words_preserved_B137_B45_zero_B46_one=True,
        final_five_component_sets_wholeactors_andPRNG_equal_for_each_pair=True,all532_later_full_RGB_pairs_equal=True,
        all28_sameframe_upper_scene_portrait_andheaders_equal=True,
        source_Japanese_toEnglish_command_differences_by_block=[17,1,5],duration_differences_by_block=[4,0,0],
        B137_timing_differences_retained_even_with_equal_final_return8815=True,
        B137_fixture_later_captain0_andparty0_not_normal_Hodram_route_continuity=True,
        initialized_opening_not_original_event_activation_location_eligibility_orall_attainable_effect_paths=True,
        no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim=True,
        all207_name_review_full_catalogue_customnames_andwider_PortWorker_lead_still_open=True,
        frozen_policy_atomic_production_registered_release_exact_clean_patch_andcompletion_credit_pending=True,
        new_credit=0,new_emulator_runs=6,new_actual_frames=100006,full_goal_complete=False,evidence=evidence))
    print('Hodram28 display approved:all five scoped gates,56actual pages/262complete body-name holds/six names/12viewed sheets. Policy/atomic/registered release pending;zero credit.')
