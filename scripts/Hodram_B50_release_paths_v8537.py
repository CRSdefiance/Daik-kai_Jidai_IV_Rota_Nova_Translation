"""Immutable B50 production paths; complete initialized scene and measured limits stay explicit."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v8475_candidate.nds')
ROM=Path('out/Hodram_B50_reference_v8502_RESEARCH_ONLY.nds')
DOC=Path('translations/hodram_B50_editorial_manuscript_v5.json')
NAMES=Path('translations/hodram_B50_speaker_name_review_v2.json')
SEAL=Path('work/analysis/Hodram_B50_release_seal_v8538/reference_seal.json')
CONFIG=Path('translations/hodram_B50_editorial_release_v1.json')
PROOFS={
 'manuscript':str(DOC),'names':str(NAMES),
 'native_contract':'translations/hodram_B50_native_contract_v2.json',
 'current':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
 'source_controls':'work/analysis/Hodram_B50_source_controls_v8486/source_controls.json',
 'source_display':'work/analysis/Hodram_B50_source_display_v8487/source_display.json',
 'relocation':'work/analysis/Hodram_B50_references_v8503/source_current_final_map.json',
 'stored':'work/analysis/Hodram_B50_stored_v8496/stored_bodies.json',
 'models':'work/analysis/Hodram_B50_models_v8506/native_models.json',
 'pages':'work/analysis/Hodram_B50_pages_v8492b/compiled_native_pages.json',
 'fixtures':'work/analysis/Hodram_B50_fixtures_v8504/two_whole_scripts.json',
 'actual':'work/analysis/Hodram_B50_actual_v8507/B50/paired_actual_dialogue_headers_flow_returns.json',
 'FE_geometry':'work/analysis/Hodram_B50_FE_binding_v8508/two_original_FE_paint_snapshots_six_exact_bitmap_palette_RGB_holds.json',
 'comparison':'work/analysis/Hodram_B50_comparison_v8509/paired_selected_path_comparison.json',
 'controls':'work/analysis/Hodram_B50_controls_v8497/stored_controls.json',
 'loaders':'work/analysis/Hodram_B50_loaders_v8503/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
 'callers':'work/analysis/Hodram_B50_references_v8503/references.json',
 'reference':'work/analysis/Hodram_B50_reference_v8502/research_image_receipt.json',
 'format_approval':'work/analysis/Hodram_B50_format_v8511/formatting_approval.json',
 'gate_metadata_approval':'work/analysis/Hodram_B50_gate_metadata_v8516/metadata_approval.json',
 'policy_validation':'work/analysis/Hodram_B50_policy_validation_v8515b/policy_validation.json',
 'independent_native':'work/analysis/Hodram_B50_independent_native_v8520/independent_native_models.json',
 'independent_actual_FE':'work/analysis/Hodram_B50_independent_actual_FE_v8524/independent_actual_FE.json',
 'independent_comparison':'work/analysis/Hodram_B50_independent_compare_v8526/independent_comparison.json',
 'independent_controls':'work/analysis/Hodram_B50_independent_controls_v8530/independent_controls.json',
 'independent_references':'work/analysis/Hodram_B50_independent_refs_v8528/independent_references.json',
 'predecessor_compatibility':'work/analysis/Hodram_B50_predecessor_positive_v8536/whole_V8475_byte_exact.json',
 'builder_support':'work/analysis/Hodram_B50_builder_support_v8534/source_equivalence.json',
 'builder_validation':'work/analysis/Hodram_B50_builder_validation_v8535/exact_builder_inverse_cases.json',
 'Gerhard_reference':'work/analysis/Gerhard_reference_v8215/research_image_receipt.json',
 'Gerhard_release':'work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json',
 'predecessor_release':'work/analysis/Hodram_B49_release_v8476/registered_release_verification.json',
}

def proofs():return {k:str(Path(v)) for k,v in PROOFS.items()}

def observed_scope(data):
    pairs=[('whole',data['comparison']['groups'][0])]
    groups=[dict(scope='whole',**g) for g in data['actual']['groups']]
    return dict(editorial_units=3,speeches=3,typed_choices=0,revisions=2,justified_retentions=1,scoped_static_actors=[2],source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_panels=1,
        actual_scene_runs=2,actual_scene_frames=20002,focused_FE_runs=0,focused_FE_frames=0,total_actual_frames=20002,complete_page_occurrences=sum(len(g['speeches']) for g in groups),complete_body_name_orabsent_FE_header_holds=sum(len(s['complete_holds']) for g in groups for s in g['speeches']),actual_menu_backing_samples=0,actual_visible_choice_label_samples=0,FE_paint_snapshots=2,FE_held_VRAM_palette_RGB_samples=6,
        normal_returns=[dict(scope=g['scope'],version=g['version'],choice=g.get('choice'),**g['normal_return']) for g in groups],
        measured_comparisons=[dict(scope=choice,duration_differences=c['duration_differences'],UI_request_differences=c['UI_request_differences'],command_comparison_differences=c['command_comparison_differences'],normal_returns=c['normal_returns'],later_RGB_pairs=len(c['later_RGB_comparisons']),later_RGB_difference_count=c['later_RGB_difference_count'],final_PRNG_seeds=c['final_PRNG_seeds'],five_native_component_equality=c['five_native_component_equality'],whole_actors_equal=c['whole_actors_equal'],raw_calendars_uninterpreted=c['raw_calendars_uninterpreted'],following_commands_equal=c['following_commands_equal']) for choice,c in pairs],
        initialized_whole_scripts_not_natural_event_activation_original_location_earned_inventory_ortrade_eligibility=True,no_everyframe_causality_future_PRNG_outcome_broad_simulation_fullroute_hardware_orcustomname_claim=True,source_opaque_effects_structurally_preserved_not_invented_gameplay_semantics=True,all_measured_timing_PRNG_RGB_andcalendar_limits_retained=True)
