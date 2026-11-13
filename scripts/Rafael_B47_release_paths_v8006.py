"""Immutable B47 speech/reference proofs for the registered production stage."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v7964_candidate.nds')
ROM=Path('out/Rafael_B47_reference_v7994_RESEARCH_ONLY.nds')
DRAFT=Path('translations/rafael_B47_editorial_manuscript_v3.json')
APPROVED=Path('translations/rafael_B47_editorial_manuscript_v4.json')
MAP=Path('translations/rafael_B47_editorial_relocation_map_v1.json')
SEAL=Path('work/analysis/Rafael_B47_reference_seal_v8006/all15_five_gates_exact_references_approved.json')
RELOCATION=Path('work/analysis/Rafael_B47_relocation_v7989/one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json')
FLAGS=[
    'external_references_complete','all15_sixbyte_preambles_source00_zero_macros_preserved',
    'all48_commands24_relative_sites120_native_cases_source_bound',
    'complete_clean_predecessor_blocks_andwhole_archive_inverse_exact',
    'all343_native_loads686_parent_modes_shipped_callers_bound',
    'all15_final_source_current_stored_native_andscoped_actual_refs_bound',
    'eleven_actual_speeches_each_language_four_native_only_explicit',
    'R53_only_two_pages_ordinary_turn_andfollowing_return_verified',
    'two_exact_warning_exceptions_preserve_original_QA_diagnostics',
    'all_measured_timing_RNG_component_calendar_RGB_andactivation_limits_preserved',
    'full207_names_broader_editorial_graphics_andlater_technical_reaudit_open',
]

def proofs():
    return {
        'source_context':'work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json',
        'native_contract':'translations/rafael_B47_native_contract_v1.json',
        'native_font_proof':'work/analysis/Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json',
        'native_stored_proof':'work/analysis/Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json',
        'relocated_control_proof':'work/analysis/Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json',
        'actual_proof':'work/analysis/Rafael_B47_actual_v7999/paired_source_English_observed_path_complete_pages_names_andR53_transition.json',
        'later_scope_proof':'work/analysis/Rafael_B47_actual_comparison_v8000/11_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'actual_approval':'work/analysis/Rafael_B47_actual_approval_v8003/15_source_context_native_representative_actual_approved_policy_release_pending.json',
        'RNG_scope_proof':'work/analysis/Rafael_B47_waits_v8001/original_wait_code_measured_R53_page_RNG_phases_andlater_limits.json',
        'native_policy_validation':'work/analysis/Rafael_B47_policy_validation_v8005/15_speech16_page_positives_actual_changing_expected_guard_rejections.json',
        'speaker_name_review':'translations/rafael_B47_speaker_name_review_v3.json',
        'source_branch_proof':'work/analysis/Rafael_B47_archive_tools_v7989/24_exact_source_current_relative_operands_bound_to120_native_cases.json',
        'native_loader_proof':'work/analysis/Rafael_B47_loaders_v7995/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'native_caller_proof':'work/analysis/Rafael_B47_reference_census_v7996/all48_commands24_relative_sites15_speeches_EV0_entry_shipped_callers.json',
        'source_font_proof':'work/analysis/Rafael_B47_source_name_planes_v7986/15_complete_source_pages4_names16_literal_alignments_all_progressive.json',
        'source_path_proof':'work/analysis/Rafael_B47_source_paths_v7978/625_source_result_compositions_six_text_paths_two_exclusive_alternatives.json',
        'focused_page_turn':'work/analysis/Rafael_B47_actual_focus_v8002/focused_actual_page_turn_sheet.json',
    }
