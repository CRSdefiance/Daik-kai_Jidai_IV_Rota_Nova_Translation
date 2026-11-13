"""Immutable B51 production paths and exact representative actual/technical scope."""
from pathlib import Path

PARENT = Path('out/all_routes_combined_v8543_candidate.nds')
ROM = Path('out/Hodram_B51_reference_v8570_RESEARCH_ONLY.nds')
DOC = Path('translations/hodram_B51_editorial_manuscript_v5.json')
NAMES = Path('translations/hodram_B51_speaker_name_review_v2.json')
SEAL = Path('work/analysis/Hodram_B51_release_seal_v8598/reference_seal.json')
CONFIG = Path('translations/hodram_B51_editorial_release_v1.json')
PROOFS = {
    'manuscript': str(DOC), 'names': str(NAMES),
    'native_contract': 'translations/hodram_B51_native_contract_v1.json',
    'current': 'work/analysis/Hodram_B51_current_v8559/current_effective.json',
    'source_controls': 'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json',
    'source_display': 'work/analysis/Hodram_B51_source_display_v8556/source_display.json',
    'result_flow': 'work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json',
    'relocation': 'work/analysis/Hodram_B51_references_v8572/source_current_final_map.json',
    'stored': 'work/analysis/Hodram_B51_stored_v8566/stored_native_controls_andrefs.json',
    'models': 'work/analysis/Hodram_B51_models_v8575/native_models.json',
    'pages': 'work/analysis/Hodram_B51_pages_v8563/compiled_native_pages.json',
    'fixtures': 'work/analysis/Hodram_B51_fixtures_v8573/two_whole_scripts.json',
    'actual': 'work/analysis/Hodram_B51_actual_v8576/B51/paired_actual_dialogue_headers_flow_returns.json',
    'actual_review': 'work/analysis/Hodram_B51_actual_review_v8579/whole_exchange_review.json',
    'comparison': 'work/analysis/Hodram_B51_comparison_v8577/paired_selected_path_comparison.json',
    'loaders': 'work/analysis/Hodram_B51_loaders_v8571/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
    'callers': 'work/analysis/Hodram_B51_references_v8572/references.json',
    'reference': 'work/analysis/Hodram_B51_reference_v8570b/research_image_receipt.json',
    'reference_qualification': 'work/analysis/Hodram_B51_reference_v8570b/qualification.json',
    'format_approval': 'work/analysis/Hodram_B51_format_v8582b/formatting_approval.json',
    'policy_validation': 'work/analysis/Hodram_B51_policy_validation_v8584/policy_validation.json',
    'independent_reconstruction': 'work/analysis/Hodram_B51_reconstruction_v8585/independent_reconstruction_validation.json',
    'independent_references': 'work/analysis/Hodram_B51_reference_binding_v8586/production_reference_binding.json',
    'independent_native': 'work/analysis/Hodram_B51_native_production_v8587/native_production_validation.json',
    'independent_loaders': 'work/analysis/Hodram_B51_loaders_production_v8588/loader_production_validation.json',
    'independent_comparison': 'work/analysis/Hodram_B51_comparison_production_v8589/comparison_production_validation.json',
    'independent_controls': 'work/analysis/Hodram_B51_controls_production_v8592/control_production_validation.json',
    'independent_actual': 'work/analysis/Hodram_B51_actual_production_v8593/actual_production_validation.json',
    'builder_inspection': 'work/analysis/Hodram_B51_builder_inspection_v8594/builder_inspection.json',
    'builder_support': 'work/analysis/Hodram_B51_builder_support_v8596/source_equivalence.json',
    'builder_validation': 'work/analysis/Hodram_B51_builder_validation_v8596/exact_builder_inverse_cases.json',
    'predecessor_compatibility': 'work/analysis/Hodram_B51_predecessor_positive_v8597/whole_V8543_byte_exact.json',
    'Gerhard_reference': 'work/analysis/Gerhard_reference_v8215/research_image_receipt.json',
    'Gerhard_release': 'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',
    'predecessor_release': 'work/analysis/Hodram_B50_release_v8544/registered_release_verification.json',
}

def proofs():
    return {key: str(Path(value)) for key, value in PROOFS.items()}

def observed_scope(data):
    groups = data['actual']['groups']
    comparison = data['comparison']['groups'][0]
    return dict(editorial_units=5, speeches=5, typed_choices=0, revisions=4, justified_retentions=1,
        scoped_static_actors=[1, 16, 18, 113], source_macro_counts=dict(FI=0, FA=0, FO=0), source_FE_panels=0,
        native_source_andEnglish_pages=10, actual_scene_runs=2, actual_scene_frames=20002, total_actual_frames=20002,
        complete_page_occurrences=sum(len(g['speeches']) for g in groups),
        complete_body_name_holds=sum(len(s['complete_holds']) for g in groups for s in g['speeches']),
        actual_unique_speech_IDs=[s['id'] for s in groups[0]['speeches']],
        unvisited_conditional_text_IDs=groups[0]['unvisited_conditional_text_IDs'],
        actual_name_header_actor_IDs=[1, 16, 113], offline_only_B51_name_header_actor_IDs=[18],
        normal_returns=[dict(scope='whole', version=g['version'], **g['normal_return']) for g in groups],
        measured_comparisons=[dict(scope='whole', duration_differences=comparison['duration_differences'], UI_request_differences=comparison['UI_request_differences'],
            command_comparison_differences=comparison['command_comparison_differences'], normal_returns=comparison['normal_returns'],
            later_RGB_pairs=len(comparison['later_RGB_comparisons']), later_RGB_difference_count=comparison['later_RGB_difference_count'],
            final_PRNG_seeds=comparison['final_PRNG_seeds'], five_native_component_equality=comparison['five_native_component_equality'],
            whole_actors_equal=comparison['whole_actors_equal'], raw_calendars_uninterpreted=comparison['raw_calendars_uninterpreted'],
            following_commands_equal=comparison['following_commands_equal'])],
        initialized_whole_script_fixtures_not_natural_activation_original_location_earned_inventory=True,
        unvisited_Charles_focused_native_checks_not_an_actual_conditional_visit=True,
        no_everyframe_causality_future_PRNG_outcome_broad_simulation_fullroute_hardware_orcustomname_claim=True,
        source_opaque_effects_structurally_preserved_not_invented_gameplay_semantics=True,
        all_measured_timing_PRNG_RGB_andcalendar_limits_retained=True)
