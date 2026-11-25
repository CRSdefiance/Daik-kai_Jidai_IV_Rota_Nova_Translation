"""Immutable retrospective B218 proof declarations; no credit or promotion is granted."""
from pathlib import Path
PARENT=Path('out/all_routes_combined_v7821_candidate.nds')
ROM=Path('out/lil_B218_wrap_reference_v7841_RESEARCH_ONLY.nds')
DRAFT=Path('translations/lil_B218_retrospective_layout_manuscript_v1.json')
APPROVED=Path('translations/lil_B218_retrospective_layout_manuscript_v2.json')
SEALED=Path('translations/lil_B218_retrospective_layout_manuscript_v3.json')
MAP=Path('translations/lil_B218_retrospective_relocation_map_v1.json')
SEAL=Path('work/analysis/retrospective_B218_reference_seal_v7853/approval_receipt.json')
FLAGS=['external_references_complete','all13_sixbyte_preambles_zero_macros_andselectors_preserved',
    'all15_commands_no_relative_sites_bound','complete_clean_predecessor_block_andwhole_archive_inverse_exact',
    'all336_native_loads672_parent_modes_andbounded_callers_bound','all13_original_speeches_both_English_variants_observed',
    'one_automatic_wrap_only12_other_stored_bodies_exact','all_measured_late_andnatural_activation_limits_preserved',
    'no_duplicate_editorial_credit_full_scope_names_graphics_andlater_audit_preserved']
def proofs():
    return dict(
        source_context='work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json',
        source_gloss='work/analysis/retrospective_B218_wrap_gloss_v7832/thirteen_fresh_clean_exchange_glosses_before_full_current_layout_review.json',
        wording_review=str(DRAFT),
        original_final='translations/lil_B218_contextual_final_review_v1.json',
        native_font='work/analysis/retrospective_B218_native_v7838/one_changed_wrap12_alignments_two_complete_current_native_planes.json',
        stored_controls='work/analysis/retrospective_B218_stored_controls_v7840/one_changed_stored_plane13_dispatches_A00025_ends_andtwo_sheets_viewed.json',
        original_stored='work/analysis/lil_B218_stored_v6895/all13_final_stored_targets52_alignments13_complete_pages.json',
        loader='work/analysis/retrospective_B218_loader_v7842/whole_SC2_336_loads_cache_hits672_original_parent_modes.json',
        caller='work/analysis/retrospective_B218_caller_census_v7843/all15_commands_original_entry_andbounded_shipped_callers.json',
        actual='work/analysis/retrospective_B218_actual_v7846/two_English_scenes_complete_masks_commands_andall_measured_late_limits.json',
        actual_view='work/analysis/retrospective_B218_actual_view_v7847/26_actual_panes_eight_sheets_andall_measured_limits_viewed.json',
        fixtures='work/analysis/retrospective_B218_scene_fixtures_v7844/paired_previous_proposed_fixtures_andrunners.json',
        policy='work/analysis/retrospective_B218_policy_validation_v7849/13_positives221_actual_changing_policy_rejections.json',
        approval='work/analysis/retrospective_B218_approval_v7850/all13_five_gates_approved_one_wrap_no_duplicate_credit.json',
        frozen_contract='translations/lil_B218_retrospective_native_contract_v1.json',
        names='work/analysis/lil_B218_name_planes_v6883/two_actors_four_getters_six_name_component_planes24_alignments.json',
        name_consumers='work/analysis/lil_B218_consumers_v6876/thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers.json',
        own_Lil_input='work/analysis/current_V7821_Lil_native_v7837/current_native_input.json')
def measured_summary(actual):
    return dict(exits=[g['exit_frame'] for g in actual['groups']],complete_pages=actual['total_actual_pages'],
        complete_body_andheader_holds=actual['total_actual_complete_body_andheader_holds'],
        command_difference_rows=actual['command_difference_rows'],duration_difference_rows=actual['duration_difference_rows'],
        later_RGB_differences=actual['later_RGB_differences'],later_samples=len(actual['later_sampled_whole_frame_comparisons']),
        five_native_component_equality=actual['five_native_component_equality'],
        final_whole_actor_equal=actual['final_whole_actor_equal'],final_PRNG_seeds=actual['final_PRNG_seeds'])
