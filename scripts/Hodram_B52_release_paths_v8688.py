"""Immutable B52 production paths and honest complete actual/technical scope."""
from pathlib import Path

PARENT=Path('out/all_routes_combined_v8609_candidate.nds')
ROM=Path('out/Hodram_B52_reference_v8645_RESEARCH_ONLY.nds')
DOC=Path('translations/hodram_B52_editorial_manuscript_v6.json')
NAMES=Path('translations/hodram_B52_speaker_name_review_v4.json')
SEAL=Path('work/analysis/Hodram_B52_release_seal_v8689/reference_seal.json')
CONFIG=Path('translations/hodram_B52_editorial_release_v1.json')
PROOFS={
    'manuscript':str(DOC),'names':str(NAMES),
    'native_contract':'translations/hodram_B52_native_contract_v1.json',
    'current':'work/analysis/Hodram_B52_current_v8631/current_effective.json',
    'source_controls':'work/analysis/Hodram_B52_source_controls_v8620/source_controls.json',
    'source_display':'work/analysis/Hodram_B52_source_display_v8626/source_display.json',
    'source_menu_VM':'work/analysis/Hodram_B52_source_choice_VM_v8628b/source_menu_provider_andresponse_paths.json',
    'result_flow':'work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    'relocation':'work/analysis/Hodram_B52_references_v8647/source_current_final_map.json',
    'stored':'work/analysis/Hodram_B52_stored_v8643/stored_native_controls_andrefs.json',
    'models':'work/analysis/Hodram_B52_models_v8650/native_models.json',
    'pages':'work/analysis/Hodram_B52_pages_v8635/compiled_native_pages.json',
    'fixtures':'work/analysis/Hodram_B52_fixtures_v8648/two_whole_scripts.json',
    'actual':'work/analysis/Hodram_B52_actual_v8651/B52/paired_actual_dialogue_headers_flow_returns.json',
    'opposition_actual':'work/analysis/Hodram_B52_opposition_actual_v8653/B52/paired_actual_dialogue_headers_flow_returns.json',
    'focus_actual':'work/analysis/Hodram_B52_focus_actual_v8657/B52/paired_actual_dialogue_headers_flow_returns.json',
    'actual_review':'work/analysis/Hodram_B52_actual_review_v8659/qualified_actual_review.json',
    'menu_provider':'work/analysis/Hodram_B52_menu_v8636/menu_provider_and_planes.json',
    'menu_actual':'work/analysis/Hodram_B52_actual_menu_RGB_v8654/actual_menu_RGB_glyph_geometry_highlight.json',
    'comparison':'work/analysis/Hodram_B52_comparison_v8655/paired_selected_path_comparison.json',
    'focus_comparison':'work/analysis/Hodram_B52_focus_comparison_v8658/paired_selected_path_comparison.json',
    'loaders':'work/analysis/Hodram_B52_loaders_v8646/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
    'callers':'work/analysis/Hodram_B52_references_v8647/references.json',
    'reference':'work/analysis/Hodram_B52_reference_v8645/research_image_receipt.json',
    'format_approval':'work/analysis/Hodram_B52_format_v8662b/formatting_approval.json',
    'policy_validation':'work/analysis/Hodram_B52_policy_validation_v8664b/policy_validation.json',
    'independent_reconstruction':'work/analysis/Hodram_B52_reconstruction_production_v8666/production_reconstruction.json',
    'independent_references':'work/analysis/Hodram_B52_references_production_v8677/references_production_validation.json',
    'independent_native':'work/analysis/Hodram_B52_native_production_v8667/native_production_validation.json',
    'independent_menu':'work/analysis/Hodram_B52_menu_production_v8672/menu_production_validation.json',
    'independent_controls':'work/analysis/Hodram_B52_controls_production_v8679b/control_production_validation.json',
    'independent_loaders':'work/analysis/Hodram_B52_loaders_production_v8681/loader_production_validation.json',
    'independent_actual':'work/analysis/Hodram_B52_actual_production_v8683/actual_production_validation.json',
    'independent_comparison':'work/analysis/Hodram_B52_comparison_production_v8685/comparison_production_validation.json',
    'predecessor_release':'work/analysis/Hodram_B51_release_v8610/registered_release_verification.json',
    'own_input':'work/analysis/current_V8609_Hodram_native_v8612/current_native_input.json',
    'own_startup':'work/analysis/Hodram_B51_registered_startup_view_v8613/own_registered_startup6_RGBpairs_actor_equal_unchanged_names_direct_view.json',
    'Gerhard_reference':'work/analysis/Gerhard_reference_v8215/research_image_receipt.json',
}


def proofs():
    return {key:str(Path(value)) for key,value in PROOFS.items()}


def observed_scope(data):
    groups=[(scope,g) for scope,key in [('withdrawal','actual'),('opposition','opposition_actual'),('focus','focus_actual')] for g in data[key]['groups']]
    comparisons=data['comparison']['groups']+data['focus_comparison']['groups']
    return dict(editorial_units=5,speeches=3,typed_choices=2,revisions=2,justified_retentions=3,
        scoped_static_actors=[113],mentioned_surname_components=[34],source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_panels=0,
        native_source_andEnglish_pages=6,actual_scene_runs=6,total_actual_frames=50406,main_frames=40004,focused_frames=10402,
        complete_page_occurrences=sum(len(g['speeches']) for _,g in groups),
        complete_body_name_holds=sum(len(s['complete_holds']) for _,g in groups for s in g['speeches']),
        actual_unique_speech_IDs=sorted({s['id'] for _,g in groups for s in g['speeches']}),
        case_specific_unvisited=[dict(scope=scope,version=g['version'],IDs=g['unvisited_conditional_text_IDs']) for scope,g in groups],
        original_returns=[dict(scope=scope,version=g['version'],**g['script_return' if scope=='opposition' else 'normal_return']) for scope,g in groups],
        measured_comparisons=[{key:g[key] for key in ['case','duration_differences','UI_request_differences','command_comparison_differences','script_returns','later_RGB_difference_count','final_PRNG_seeds','five_native_component_equality','whole_actors_equal','raw_calendars_uninterpreted','following_commands_equal']} for g in comparisons],
        later_RGB_pairs=[len(g['later_RGB_comparisons']) for g in comparisons],
        actual_menu_RGB_samples=12,actual_complete_caption_checks=24,
        source_context_qualification=data['independent_controls']['summary']['source_context_qualification'],
        source_8620_used_V8543_ownV8609_consumers_rebound_without_RAM_overlay=True,
        initialized_whole_script_fixtures_not_original_optional_event_activation_location_earned_progress=True,
        actual_visible_menu_RGB_not_live_owner_RAM_VRAM_palette_orbacking_byte_identity=True,
        original_native_backing_bounds_are_offline_checks_actual_cancel_availability_unobserved=True,
        long_withdrawal_divergence_andfocused_immediate_agreement_preserved_without_causal_explanation=True,
        no_everyframe_future_PRNG_outcome_simulation_fullroute_hardware_orcustomname_equivalence_claim=True,
        source_opaque_effects_structurally_preserved_not_invented_gameplay_semantics=True)
