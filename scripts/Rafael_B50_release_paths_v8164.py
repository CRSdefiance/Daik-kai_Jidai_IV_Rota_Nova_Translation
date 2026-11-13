"""Immutable B50 proof set for registered speech-only cumulative integration."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v8122_candidate.nds')
ROM=Path('out/Rafael_B50_reference_v8151_RESEARCH_ONLY.nds')
DRAFT=Path('translations/rafael_B50_editorial_manuscript_v3.json')
APPROVED=Path('translations/rafael_B50_editorial_manuscript_v4.json')
MAP=Path('translations/rafael_B50_editorial_relocation_map_v1.json')
SEAL=Path('work/analysis/Rafael_B50_reference_seal_v8164/all28_five_gates_exact_references_approved.json')
RELOCATION=Path('work/analysis/Rafael_B50_relocation_v8146/one_block28_speeches_zero_relative_cases_exact_full_inverse.json')
FLAGS=[
    'external_references_complete','all28_sixbyte_preambles_source00_02_09_FA2_FI1_preserved',
    'all37_commands_zero_relative_predicate_query_sites_source_bound',
    'complete_clean_predecessor_blocks_andwhole_archive_inverse_exact',
    'all343_native_loads686_parent_modes_shipped_callers_bound',
    'all28_final_source_current_stored_native_andactual_refs_bound',
    'all28_actual_speeches_each_language_three_headers_explicit',
    'all28_single_pages_no_FE_or_invented_page_turn',
    'actual_4821_A000_4720_4681_picture_hide_departure_andnormal_return_verified',
    'two_exact_warning_exceptions_and18_infos_preserve_original_QA_diagnostics',
    'all_measured_timing_RNG_component_byte_calendar_RGB_andactivation_limits_preserved',
    'full207_names_broader_editorial_graphics_andlater_technical_reaudit_open',
]

def proofs():
    return {
        'source_context':'work/analysis/Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json',
        'native_contract':'translations/rafael_B50_native_contract_v1.json',
        'native_font_proof':'work/analysis/Rafael_B50_pages_refined_v8143/28_final_native_pages20_fresh92_reused_alignments.json',
        'native_stored_proof':'work/analysis/Rafael_B50_stored_v8147/all28_stored_bodies_full_native_alignment_and28_exact_viewed_pages.json',
        'relocated_control_proof':'work/analysis/Rafael_B50_relocated_controls_v8148/28_stored_dispatches_nine_controls_zero_relatives_relocated4821_25_seeded_ends.json',
        'actual_proof':'work/analysis/Rafael_B50_actual_v8156/paired_source_English_all28_pages_three_names_4821_departure_andreturn.json',
        'later_scope_proof':'work/analysis/Rafael_B50_actual_comparison_v8157/all_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'actual_approval':'work/analysis/Rafael_B50_actual_approval_v8161/28_source_context_native_all_actual_approved_policy_release_pending.json',
        'RNG_scope_proof':'work/analysis/Rafael_B50_waits_v8158/original_wait_code_measured_4821_departure_RNG_phases_andlater_limits.json',
        'native_policy_validation':'work/analysis/Rafael_B50_policy_validation_v8163/28_speech28_page_positives_actual_changing_expected_guard_rejections.json',
        'speaker_name_review':'translations/rafael_B50_speaker_name_review_v3.json',
        'source_branch_proof':'work/analysis/Rafael_B50_archive_tools_v8146/zero_source_current_relative_operands37_commands_nine_nontext_pairs.json',
        'native_loader_proof':'work/analysis/Rafael_B50_loaders_v8152/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'native_caller_proof':'work/analysis/Rafael_B50_reference_census_v8153/all37_commands_zero_relative_sites28_speeches_4821_EV0_entry_shipped_callers.json',
        'source_font_proof':'work/analysis/Rafael_B50_source_name_planes_v8142/28_complete_source_pages3_names0_fresh12_reused_literal_alignments.json',
        'source_path_proof':'work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json',
        'focused_picture_transition_andrisk':'work/analysis/Rafael_B50_actual_focus_v8160/focused_actual_picture_return_andbounded_later_state_risk.json',
        'source_4821_item_proof':'work/analysis/Rafael_B50_pigment_v8134/original4821_descriptor181_clean_current_Red_Dye_andbounded_consumer_path.json',
    }
