"""Final confrontation proof paths; declarations grant no approval orcredit."""
from pathlib import Path
from scripts.freeze_Maria_confrontation_policy_v7814 import MANUSCRIPT,PLAN,CURRENT,NATIVE,STORED,VIEW,NAMES,CONTRACT
from scripts.create_Maria_confrontation_reference_v7805 import PARENT,ROM,PLAN as RELOCATION
DRAFT=MANUSCRIPT
APPROVED=Path('translations/maria_B36_editorial_manuscript_v3.json')
SEALED=Path('translations/maria_B36_editorial_manuscript_v4.json')
MAP=Path('translations/maria_B36_editorial_relocation_map_v1.json')
APPROVAL=Path('work/analysis/maria_B36_native_approval_v7816/approval.json')
SEAL=Path('work/analysis/maria_B36_reference_approval_v7817/approval_receipt.json')
POLICY=Path('work/analysis/maria_confrontation_policy_validation_v7815b/16_positives81_actual_changing_guard_rejections.json')
ACTUAL=Path('work/analysis/maria_confrontation_actual_v7811/two_scene_captures_actual_pages_headers_branches_returns.json')
LATER=Path('work/analysis/maria_confrontation_actual_comparison_v7812/one_actual_pair_measured_portraits_timing_RNG_states_RGB_limits.json')
SOURCE=Path('work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json')
def proofs():
    return dict(source_context=str(CURRENT),clean_source_exchanges=str(SOURCE),
        source_glosses='work/analysis/maria_confrontation_gloss_v7787/sixteen_clean_whole_exchange_glosses_before_current_English.json',
        current_consumer_proof='work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json',
        source_entry_proof='work/analysis/maria_confrontation_entry_v7795/one_original_EV3_getter_no_inblock_predicates.json',
        native_name_macro_proof='work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json',
        source_branch_proof='work/analysis/maria_confrontation_archive_tools_v7802/source_current_no_relative_orpredicate_commands.json',
        source_control_proof='work/analysis/maria_confrontation_controls_v7804/16_final_dispatches_six_numeric_leaves_623D_resources_setup_ends.json',
        relocated_control_proof=str(STORED),native_font_proof=str(NATIVE),native_stored_proof=str(STORED),
        native_policy_validation=str(POLICY),actual_proof=str(ACTUAL),later_scope_proof=str(LATER),actual_view=str(VIEW),
        speaker_name_review=str(NAMES),
        broader_role_census='work/analysis/retainer_speaker_uses_v7740/all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json',
        broader_role_triage='work/analysis/retainer_name_triage_v7744/nine_roles18_getters147_source_blocks484_uses_nine_context_samples.json',
        native_loader_proof='work/analysis/maria_confrontation_loaders_v7806/303_whole_native_loads_cache_hits606_initial_parent_modes.json',
        native_caller_proof='work/analysis/maria_confrontation_reference_census_v7807/all22_commands_original_B36_entry_no_relative_sites_shipped_callers.json',
        native_policy_contract=str(CONTRACT))
