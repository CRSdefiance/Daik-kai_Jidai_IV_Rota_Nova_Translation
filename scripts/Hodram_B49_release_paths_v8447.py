"""Immutable B49 production paths;original fixture and measured-limit scope stays explicit."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v8377_candidate.nds')
ROM=Path('out/Hodram_B49_reference_v8403_RESEARCH_ONLY.nds')
DOC=Path('translations/hodram_B49_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B49_speaker_name_review_v2.json')
SEAL=Path('work/analysis/Hodram_B49_release_seal_v8448/reference_seal.json')
CONFIG=Path('translations/hodram_B49_editorial_release_v1.json')
PROOFS={
 'manuscript':str(DOC),'names':str(NAMES),
 'native_contract':'translations/hodram_B49_native_contract_v2.json',
 'current':'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json',
 'source_controls':'work/analysis/Hodram_B49_source_controls_v8384/source_controls.json',
 'source_display':'work/analysis/Hodram_B49_source_display_v8386b/source_display.json',
 'relocation':'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json',
 'stored':'work/analysis/Hodram_B49_stored_v8399/stored_bodies.json',
 'models':'work/analysis/Hodram_B49_models_v8408/native_models.json',
 'pages':'work/analysis/Hodram_B49_pages_v8395/compiled_native_pages.json',
 'fixtures':'work/analysis/Hodram_B49_fixtures_v8406/two_whole_scripts.json',
 'tail_fixtures':'work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json',
 'actual':'work/analysis/Hodram_B49_actual_v8409/B49/paired_actual_dialogue_headers_flow_returns.json',
 'tail_actual':'work/analysis/Hodram_B49_tail_actual_v8417/bounded_tail_actual.json',
 'menu_provider':'work/analysis/Hodram_B49_menu_v8400/menu_provider_and_planes.json',
 'menu_actual':'work/analysis/Hodram_B49_menu_actual_v8418/four_actual_menus12_full_owned_backing_andhighlight_samples.json',
 'FE_geometry':'work/analysis/Hodram_B49_FE_binding_v8420/two_original_FE_paint_snapshots_four_exact_bitmap_palette_RGB_holds.json',
 'comparison':'work/analysis/Hodram_B49_comparison_v8410/paired_selected_path_comparison.json',
 'tail_comparison':'work/analysis/Hodram_B49_tail_comparison_v8421/both_bounded_tail_comparisons.json',
 'controls':'work/analysis/Hodram_B49_controls_v8401d/stored_controls.json',
 'loaders':'work/analysis/Hodram_B49_loaders_v8404/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
 'callers':'work/analysis/Hodram_B49_references_v8405b/references.json',
 'reference':'work/analysis/Hodram_B49_reference_v8403/research_image_receipt.json',
 'format_approval':'work/analysis/Hodram_B49_format_v8423/formatting_approval.json',
 'encoder_approval':'work/analysis/Hodram_B49_encoder_v8426/metadata_approval.json',
 'policy_validation':'work/analysis/Hodram_B49_policy_validation_v8425b/policy_validation.json',
 'independent_native':'work/analysis/Hodram_B49_independent_native_v8433/independent_native_models.json',
 'independent_actual':'work/analysis/Hodram_B49_independent_actual_v8434b/independent_actual.json',
 'independent_FE':'work/analysis/Hodram_B49_independent_FE_v8436/independent_FE.json',
 'independent_menu':'work/analysis/Hodram_B49_independent_menu_v8437/independent_menu.json',
 'independent_comparison':'work/analysis/Hodram_B49_independent_compare_v8439/independent_comparison.json',
 'independent_controls':'work/analysis/Hodram_B49_independent_controls_v8441b/independent_controls.json',
 'independent_references':'work/analysis/Hodram_B49_independent_refs_v8443/independent_references.json',
 'predecessor_compatibility':'work/analysis/Hodram_B49_predecessor_binding_v8446b/semantic_binding.json',
 'Gerhard_reference':'work/analysis/Gerhard_reference_v8215/research_image_receipt.json',
 'Gerhard_release':'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',
 'predecessor_release':'work/analysis/Hodram_outcomes_release_v8378/registered_release_verification.json',
}

def proofs():return {k:str(Path(v)) for k,v in PROOFS.items()}

def observed_scope(data):
    pairs=[('whole',data['comparison']['groups'][0]),*[(g['choice'],g) for g in data['tail_comparison']['groups']]]
    groups=[dict(scope='whole',**g) for g in data['actual']['groups']]+[dict(scope='bounded-tail',**g) for g in data['tail_actual']['groups']]
    return dict(editorial_units=16,speeches=14,typed_choices=2,revisions=7,justified_retentions=9,scoped_static_actors=[1,2],source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_panels=1,
        actual_scene_runs=6,actual_scene_frames=60006,focused_FE_runs=2,focused_FE_frames=9862,total_actual_frames=69868,complete_page_occurrences=sum(len(g['speeches']) for g in groups),complete_body_name_orabsent_FE_header_holds=sum(len(s['complete_holds']) for g in groups for s in g['speeches']),actual_menu_backing_samples=12,actual_visible_choice_label_samples=24,
        normal_returns=[dict(scope=g['scope'],version=g['version'],choice=g.get('choice'),**g['normal_return']) for g in groups],
        measured_comparisons=[dict(scope=choice,duration_differences=c['duration_differences'],UI_request_differences=c['UI_request_differences'],command_comparison_differences=c['command_comparison_differences'],normal_returns=c['normal_returns'],later_RGB_pairs=len(c['later_RGB_comparisons']),later_RGB_difference_count=c['later_RGB_difference_count'],final_PRNG_seeds=c['final_PRNG_seeds'],five_native_component_equality=c['five_native_component_equality'],whole_actors_equal=c['whole_actors_equal'],raw_calendars_uninterpreted=c['raw_calendars_uninterpreted'],following_commands_equal=c['following_commands_equal']) for choice,c in pairs],
        initialized_whole_scripts_andbounded_possession_dialogue_tails_not_natural_event_activation_original_location_earned_inventory_ortrade_eligibility=True,no_everyframe_causality_future_PRNG_outcome_broad_simulation_fullroute_hardware_orcustomname_claim=True,source_opaque_effects_structurally_preserved_not_invented_gameplay_semantics=True,all_measured_timing_PRNG_RGB_andcalendar_limits_retained=True)
