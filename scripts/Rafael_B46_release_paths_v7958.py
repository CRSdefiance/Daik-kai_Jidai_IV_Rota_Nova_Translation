"""Immutable B46 speech/menu/reference proofs for the registered production stage."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v7911_candidate.nds')
ROM=Path('out/Rafael_B46_reference_v7941_RESEARCH_ONLY.nds')
DRAFT=Path('translations/rafael_B46_editorial_manuscript_v3.json')
APPROVED=Path('translations/rafael_B46_editorial_manuscript_v4.json')
MENU=Path('translations/rafael_B46_choice_manuscript_v1.json')
MAP=Path('translations/rafael_B46_editorial_relocation_map_v1.json')
SEAL=Path('work/analysis/Rafael_B46_reference_seal_v7958/all26_five_gates_exact_references_approved.json')
RELOCATION=Path('work/analysis/Rafael_B46_relocation_v7938/one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json')
FLAGS=[
    'external_references_complete','all24_sixbyte_preambles_source00_FE_zero_macros_preserved',
    'all37_commands4_relative_sites20_native_cases_two_choices_source_bound',
    'complete_clean_predecessor_blocks_andwhole_archive_inverse_exact',
    'all343_native_loads686_parent_modes_shipped_callers_bound',
    'all26_final_source_current_stored_actual_refs_bound',
    'all24_original_speeches_andboth_choices_observed_in_both_languages',
    'all_measured_highlight_timing_RNG_component_calendar_RGB_andactivation_limits_preserved',
    'full207_names_broader_editorial_graphics_andlater_technical_reaudit_open',
]
def proofs():
    return {
        'source_context':'work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json',
        'native_contract':'translations/rafael_B46_native_contract_v1.json',
        'native_font_proof':'work/analysis/Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json',
        'native_stored_proof':'work/analysis/Rafael_B46_stored_v7939/all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json',
        'stored_menu_proof':'work/analysis/Rafael_B46_stored_v7939/two_stored_menu_labels_exact8_viewed_planes_two_header_alignments.json',
        'relocated_control_proof':'work/analysis/Rafael_B46_relocated_controls_v7940/24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json',
        'actual_proof':'work/analysis/Rafael_B46_actual_v7948/four_runs24_unique_speeches58_occurrences_two_choices_actual_body_name_FE_return_audit.json',
        'actual_menu_proof':'work/analysis/Rafael_B46_menu_actual_v7950c/four_actual_menus12_full_owned_backing_andhighlight_samples.json',
        'later_scope_proof':'work/analysis/Rafael_B46_actual_comparison_v7949/both_choices29_scene_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'actual_approval':'work/analysis/Rafael_B46_actual_approval_v7953/26_source_context_native_actual_approved_policy_release_pending.json',
        'RNG_scope_proof':'work/analysis/Rafael_B46_waits_v7951/both_choices_original_wait_code_measured_RNG_phases_andlater_limits.json',
        'native_policy_validation':'work/analysis/Rafael_B46_policy_validation_v7957/24_speech_two_choice_positives_actual_changing_expected_guard_rejections.json',
        'speaker_name_review':'translations/rafael_B46_speaker_name_review_v2.json',
        'source_branch_proof':'work/analysis/Rafael_B46_archive_tools_v7938/four_exact_source_current_relative_operands_bound_to20_native_cases.json',
        'native_loader_proof':'work/analysis/Rafael_B46_loaders_v7942/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'native_caller_proof':'work/analysis/Rafael_B46_reference_census_v7943/all37_commands_four_relative_sites_two_choices_EV0_entry_shipped_callers.json',
        'source_font_proof':'work/analysis/Rafael_B46_source_name_planes_v7946/24_complete_source_pages3_names12_literal_alignments12_FE.json',
    }
