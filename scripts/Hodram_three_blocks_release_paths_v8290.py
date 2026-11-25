"""Immutable proof set for the three reviewed Hodram whole exchanges."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v8259_candidate.nds')
ROM=Path('out/Hodram_B137_B45_B46_reference_v8276_RESEARCH_ONLY.nds')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v4.json')
MAP=Path('translations/hodram_three_blocks_editorial_relocation_map_v1.json')
SEAL=Path('work/analysis/Hodram_reference_seal_v8290/28_records60_commands8_relatives_three_source_inverses_approved_reference.json')

def proofs():
    return dict(
        current='work/analysis/Hodram_current_review_binding_v8272/28_exact_current_refs_registered_name_dependency_andnative_reuse.json',
        relocation='work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json',
        native_stored='work/analysis/Hodram_three_block_stored_v8274/28_stored_bodies44_fresh68_reused_alignments28_exact_native_pages.json',
        native_controls='work/analysis/Hodram_final_controls_v8275/28_final_dispatches24_controls6_raw_evaluations_original4800_4700_requests.json',
        reference='work/analysis/Hodram_reference_v8276/research_image_receipt.json',
        native_loader='work/analysis/Hodram_loaders_v8277/325_whole_native_loads_cache_hits650_initial_parent_modes.json',
        native_caller='work/analysis/Hodram_reference_census_v8278/all60_commands8_relative_sites28_records_three_EV1_entries_shipped_callers.json',
        fixtures='work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json',
        native_models='work/analysis/Hodram_actual_models_v8281b/28_clean_native_bodies28_exact_revised_reuses_six_current_headers.json',
        native_names='work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json',
        actual_comparison='work/analysis/Hodram_actual_comparison_v8283/three_paired_whole_exchanges_controls_scenes_returns_bounded_later_state.json',
        display_approval='work/analysis/Hodram_display_review_v8284/display_review_receipt.json',
        policy_validation='work/analysis/Hodram_policy_validation_v8288/28_single_page_positives_changed_source_prose_gates_profiles_waivers_rejected.json',
        source_picture='work/analysis/Hodram_B46_pigment_v8190b/original4800_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json',
        source_controls='work/analysis/Hodram_B137_B45_B46_source_controls_v8188/three_EV1_entries60_commands28_speeches_native_relative_predicate_and75_seeded_ends.json',
        source_paths='work/analysis/Hodram_B137_B45_B46_source_paths_v8191/11_structural_compositions_all60_commands28_source_memberships.json',
        native_contract='translations/hodram_three_blocks_native_contract_v1.json',
        layout='work/analysis/Hodram_B137_B45_B46_layout_v8245/28_automatic_Hodram_plans_full_native_width.json',
        names=str(NAMES),
        **{f'actual_B{b}':f'work/analysis/Hodram_actual_v8282/B{b}/paired_actual_dialogue_headers_flow_returns.json' for b in [137,45,46]})

def observed_scope(data):
    return dict(blocks=[dict(block=g['block'],normal_returns=g['normal_returns'],source_English_command_differences=g['command_comparison_differences'],
        duration_differences=g['duration_differences'],UI_request_differences=g['UI_request_differences'],five_native_component_equality=g['five_native_component_equality'],
        whole_actors_equal=g['whole_actors_equal'],final_PRNG_seeds=g['final_PRNG_seeds'],raw_calendars_uninterpreted=g['raw_calendars_uninterpreted'],
        final_captain_IDs=[r['captain_ID'] for r in g['final_native_values']],later_RGB_samples=len(g['later_RGB_comparisons']),
        later_RGB_difference_count=g['later_RGB_difference_count'],following_commands=g['following_commands'],following_commands_equal=g['following_commands_equal'])
        for g in data['actual_comparison']['groups']],
        whole_exchange_fixtures_not_natural_optional_event_activation_original_locations_orall_attainable_paths=True,
        B137_later_captain0_SC0B44_not_normal_Hodram_continuity=True,
        no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim=True,
        wider207_names_catalogue_customnames_PortWorker_consumers_andfull_editorial_scope_open=True)
