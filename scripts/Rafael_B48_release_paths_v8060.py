"""Immutable complete B48 proofs for registered speech-only production."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v8013_candidate.nds')
ROM=Path('out/Rafael_B48_reference_v8046_RESEARCH_ONLY.nds')
DRAFT=Path('translations/rafael_B48_editorial_manuscript_v4.json')
APPROVED=Path('translations/rafael_B48_editorial_manuscript_v5.json')
MAP=Path('translations/rafael_B48_editorial_relocation_map_v1.json')
SEAL=Path('work/analysis/Rafael_B48_reference_seal_v8060/all91_five_gates_exact_references_approved.json')
RELOCATION=Path('work/analysis/Rafael_B48_relocation_v8041/one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json')
FLAGS=[
    'external_references_complete','all91_sixbyte_preambles_source00_4B71_oneFI_preserved',
    'all163_commands28_relative_sites140_native_cases_source_bound',
    'complete_clean_predecessor_blocks_andwhole_archive_inverse_exact',
    'all343_native_loads686_parent_modes_shipped_callers_bound',
    'all91_final_source_current_stored_native_andscoped_actual_refs_bound',
    'seventyeight_actual_speeches_each_language_thirteen_native_only_explicit',
    'R347_only_two_pages_ordinary_turn_andfollowing_return_verified',
    'four_FE_bodies_andabsent_headers_complete_actual_masks_verified',
    'two_exact_warning_exceptions_preserve_original_QA_diagnostics',
    'all_measured_timing_RNG_component_calendar_RGB_andactivation_limits_preserved',
    'full207_names_broader_editorial_graphics_andlater_technical_reaudit_open',
]
def proofs():
    return {
        'source_context':'work/analysis/Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
        'native_contract':'translations/rafael_B48_native_contract_v1.json',
        'native_font_proof':'work/analysis/Rafael_B48_pages_refined_v8038/91_final_native_paragraphs92_pages4_fresh360_reused_alignments.json',
        'native_stored_proof':'work/analysis/Rafael_B48_stored_v8042/all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json',
        'relocated_control_proof':'work/analysis/Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json',
        'actual_proof':'work/analysis/Rafael_B48_actual_v8053/paired_source_English_observed_path_complete_pages_names_andR347_transition.json',
        'later_scope_proof':'work/analysis/Rafael_B48_actual_comparison_v8054/78_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'actual_approval':'work/analysis/Rafael_B48_actual_approval_v8057/91_source_context_native_representative_actual_approved_policy_release_pending.json',
        'RNG_scope_proof':'work/analysis/Rafael_B48_waits_v8056/original_wait_code_measured_R347_page_RNG_phases_andlater_limits.json',
        'native_policy_validation':'work/analysis/Rafael_B48_policy_validation_v8059/91_speech92_page_positives_actual_changing_expected_guard_rejections.json',
        'speaker_name_review':'translations/rafael_B48_speaker_name_review_v3.json',
        'source_branch_proof':'work/analysis/Rafael_B48_archive_tools_v8041/28_exact_source_current_relative_operands_bound_to140_native_cases.json',
        'native_loader_proof':'work/analysis/Rafael_B48_loaders_v8047/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'native_caller_proof':'work/analysis/Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json',
        'source_font_proof':'work/analysis/Rafael_B48_source_rightcell_v8052/91_source_native_pages9_name_planes_R129_actual_rightcell_bound.json',
        'source_path_proof':'work/analysis/Rafael_B48_source_paths_v8025/500_source_result_compositions32_text_paths_two_exclusive_pairs.json',
        'focused_page_turn':'work/analysis/Rafael_B48_actual_focus_v8055b/focused_actual_page_turn_sheet.json',
        'source_rightcell_proof':'work/analysis/Rafael_B48_source_rightcell_v8052/source_question_mark_actual_position_binding.json',
    }
