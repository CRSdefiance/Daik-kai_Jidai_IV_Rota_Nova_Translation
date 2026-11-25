"""Linked Maria67 final proof paths; declarations grant no credit."""
from pathlib import Path
from scripts.freeze_Maria_story_policy_v7769 import MANUSCRIPT,PLAN,CURRENT,NATIVE,STORED,VIEW,NAMES,CONTRACT
from scripts.create_Maria_story_reference_v7760 import PARENT,ROM,PLAN as RELOCATION
DRAFT=MANUSCRIPT
APPROVED=Path('translations/maria_B34_B108_B35_editorial_manuscript_v4.json')
SEALED=Path('translations/maria_B34_B108_B35_editorial_manuscript_v5.json')
MAP=Path('translations/maria_story_editorial_relocation_map_v1.json')
APPROVAL=Path('work/analysis/maria_story_native_approval_v7771/approval.json')
SEAL=Path('work/analysis/maria_story_reference_approval_v7772/approval_receipt.json')
POLICY=Path('work/analysis/maria_story_policy_validation_v7770/67_positives200_actual_changing_guard_rejections.json')
ACTUAL=Path('work/analysis/maria_story_final_actual_binding_v7766/six_final_v3_actual_groups_two_fresh_four_exact_reused.json')
LATER=Path('work/analysis/maria_story_final_view_v7768/three_final_pairs_two_fresh_one_exact_reused.json')
SOURCE=Path('work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json')
def proofs():
    return dict(source_context=str(CURRENT),clean_source_exchanges=str(SOURCE),
        source_glosses='work/analysis/maria_story_chain_gloss_v7726/all67_clean_whole_exchange_glosses_before_current_English.json',
        current_consumer_proof='work/analysis/maria_story_effective_v7729/all67_effective_English_templates134_original_dispatches.json',
        source_entry_proof='work/analysis/maria_story_entries_predicates_v7731/three_original_EV3_getters_ten_source_current_predicates.json',
        native_name_macro_proof='work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json',
        source_branch_proof='work/analysis/maria_story_branches_v7741/20_relative_sites200_guarded_original_source_current_cases.json',
        source_control_proof='work/analysis/maria_story_final_controls_v7745/67_final_dispatches_numeric_leaves_opaque_controls_resources_pause_C200_ends.json',
        relocated_control_proof=str(STORED),native_font_proof=str(NATIVE),native_stored_proof=str(STORED),
        native_policy_validation=str(POLICY),actual_proof=str(ACTUAL),later_scope_proof=str(LATER),actual_view=str(VIEW),
        speaker_name_review=str(NAMES),
        broader_role_census='work/analysis/retainer_speaker_uses_v7740/all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json',
        broader_role_triage='work/analysis/retainer_name_triage_v7744/nine_roles18_getters147_source_blocks484_uses_nine_context_samples.json',
        native_loader_proof='work/analysis/maria_story_loaders_v7761/303_whole_native_loads_cache_hits606_initial_parent_modes.json',
        native_caller_proof='work/analysis/maria_story_reference_census_v7762/all116_commands20_relative_sites_original_entries_shipped_callers.json',
        native_policy_contract=str(CONTRACT))
