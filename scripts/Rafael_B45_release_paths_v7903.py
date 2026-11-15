"""Exact immutable source/native/actual/policy paths for the pending Rafael B45 release."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v7857_candidate.nds')
ROM=Path('out/Rafael_B45_reference_v7887_RESEARCH_ONLY.nds')
DRAFT=Path('translations/rafael_B45_editorial_manuscript_v4.json')
APPROVED=Path('translations/rafael_B45_editorial_manuscript_v5.json')
MAP=Path('translations/rafael_B45_editorial_relocation_map_v1.json')
SEAL=Path('work/analysis/Rafael_B45_reference_seal_v7903/all12_five_gates_exact_references_approved.json')
RELOCATION=Path('work/analysis/Rafael_B45_relocation_v7884/one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json')
FLAGS=['external_references_complete','all12_sixbyte_preambles_source00_FE_macros_preserved',
    'all24_commands5_relative_sites25_native_cases_source_bound',
    'complete_clean_predecessor_blocks_andwhole_archive_inverse_exact',
    'all343_native_loads686_parent_modes_shipped_callers_bound',
    'all12_final_source_current_stored_actual_refs_bound',
    'all12_original_speeches_observed_in_both_languages',
    'all_measured_timing_RNG_component_RGB_andactivation_limits_preserved',
    'full207_names_broader_editorial_graphics_andlater_technical_reaudit_open']
def proofs():
    return {
        'source_context':'work/analysis/Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json',
        'native_contract':'translations/rafael_B45_native_contract_v1.json',
        'native_font_proof':'work/analysis/Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json',
        'native_stored_proof':'work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json',
        'relocated_control_proof':'work/analysis/Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json',
        'actual_proof':'work/analysis/Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json',
        'later_scope_proof':'work/analysis/Rafael_B45_actual_comparison_v7896b/12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'actual_approval':'work/analysis/Rafael_B45_actual_approval_v7898/12_source_context_native_actual_format_approved_policy_release_pending.json',
        'RNG_scope_proof':'work/analysis/Rafael_B45_random_waits_v7897/actual_one_step_RNG_phase_andunchanged_source_discarded_wait_contract.json',
        'native_policy_validation':'work/analysis/Rafael_B45_policy_validation_v7902b/12_positives_actual_changing_expected_guard_rejections.json',
        'speaker_name_review':'translations/rafael_B45_speaker_name_review_v2.json',
        'source_branch_proof':'work/analysis/Rafael_B45_archive_tools_v7884/five_exact_source_current_relative_operands_bound_to25_native_cases.json',
        'native_loader_proof':'work/analysis/Rafael_B45_loaders_v7888/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'native_caller_proof':'work/analysis/Rafael_B45_reference_census_v7889/all24_commands_five_relative_sites_EV0_entry_shipped_callers.json',
    }
