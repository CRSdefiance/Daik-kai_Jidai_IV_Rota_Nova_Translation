"""Derive reference approval for B167's complete source, two ends and scoped actual coverage."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_reference_seal_tools_v4153')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/seal_lil_B166_references_v4106.py','scripts/seal_lil_B167_references_v4154.py',{
        'Seal 44 reviews':'Seal 29 reviews','prepare_lil_B166_research_v4095':'prepare_lil_B167_research_v4141',
        'lil_B166_reference_approval_v4106':'lil_B167_reference_approval_v4154',
        'lil_B166_editorial_manuscript_v5':'lil_B167_editorial_manuscript_v12',
        'lil_B166_editorial_manuscript_v6':'lil_B167_editorial_manuscript_v13',
        'lil_B166_choice_manuscript_v2':'lil_B167_choice_manuscript_v2','lil_B166_choice_manuscript_v3':'lil_B167_choice_manuscript_v3',
        'lil_B166_editorial_relocation_map':'lil_B167_editorial_relocation_map',
        'lil_B166_reference_census_v4098/all62_commands8_relative_sites':'lil_B167_reference_census_v4144/all46_commands12_relative_sites',
        'lil_B166_relocated_controls_v4100/all42_dispatches_Fernando_predicate11_leaves':'lil_B167_relocated_controls_v4146/all27_dispatches_two_Cesare_predicates6_leaves',
        'lil_B166_stored_v4094/all42_final_stored_targets168':'lil_B167_stored_v4140/all27_final_stored_targets108',
        'lil_B166_ends_v4099/two_declared_end_decodes_and_all8':'lil_B167_ends_v4145/four_declared_end_decodes_and_all12',
        'lil_B166_actual_v4104/actual_both_choices_conditional_panels_and_single_return':'lil_B167_actual_v4151/actual_both_choices_conditional_panels_and_distinct_returns',
        'lil_B166_display_fixture_v4101':'lil_B167_display_fixture_v4147',
        'lil_B166_transition_review_v4105/both_choices_all7_sheets_Manuel_names_figures_and_paired_returns_review':'lil_B167_transition_review_v4152/both_choices_all5_sheets_static_names_and_distinct_returns_review',
        'lil_B166_choices_v4080/B166_C2152':'lil_B167_choices_v4133/B167_C152',
        'all62_clean_current_target_commands_and8_relative_sites_reexecuted':'all46_clean_current_target_commands_and12_relative_sites_reexecuted',
        "len(control['relocated_dispatch_cases']) == 42 and len(control['relocated_predicate_pairs']) == 1":"len(control['relocated_dispatch_cases']) == 27 and len(control['relocated_predicate_pairs']) == 2",
        "len(control['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves']) == 11":"len(control['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves']) == 6",
        'unforced_Fernando_result_matches_source_without_roster_fixture':'both_unforced_Cesare_results_match_source_without_roster_fixture',
        "stored['current_final_stored_macro_alignment_cases'] == 168 and len(stored['final_target_parity_cases']) == 42":"stored['current_final_stored_macro_alignment_cases'] == 108 and len(stored['final_target_parity_cases']) == 27",
        'all42_final_targets':'all27_final_targets',
        'all2_declared_end_decodes':'all4_declared_end_decodes',
        "ends['B166_single_end_is_declared_logical_tail'] and len(ends['cases']) == 2":"ends['B167_first_end_precedes_second_end_and_declared_logical_end'] and len(ends['cases']) == 4",
        "actual['fresh_actual_unique_speech_panels'] == 41 and actual['complete_matching_observations'] == 73":"actual['fresh_actual_unique_speech_panels'] == 25 and actual['complete_matching_observations'] == 28",
        'both_real_choice_values_and_same_single_tail_end_observed':'both_real_choice_values_and_distinct_source_endwords_observed',
        'all7_actual_sheets_viewed':'all5_actual_sheets_viewed',
        "== 7 and len(visual['English_full_screen_views']) == 11":"== 5 and len(visual['English_full_screen_views']) == 8",
        'all_original_choice_relative_containers_presentation_resources_and_single_end_preserved':'all_original_choice_relative_containers_resources_and_both_ends_preserved',
        'one_late_recruitment_effect_excluded_after_choice_without_changing_any_branch_span':'no_source_B167_A000_effect_to_omit',
        "native['all42_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 336":"native['all27_current_native_speech_planes_pass'] and native['current_original_macro_alignment_calls'] == 216",
        "['DK4_MES_B166_R0087']":"['DK4_MES_B167_R0045','DK4_MES_B167_R0131']",
        'actual_Manuel17_original_nameplate_portrait_and_full_figure_observed':'actual_Shipwright109_Lil2_Janus4_Manuel23_original_names_and_portraits_observed',
        'actual_selected_B166_source_events':'actual_selected_B167_source_events',
        'actual41_unique_panels73_observations_both_advice_results_and_normal_returns_pass':'actual25_unique_panels28_observations_both_choices_and_distinct_returns_pass',
        'source_Fernando_query8_relative_containers_choice_and_single_end_retained_not_flattened':'source_two_Cesare_queries12_relative_containers_choice_and_both_ends_retained_not_flattened',
        'Fernando_remark_not_actual_or_byte_identical_reuse':'both_Cesare_remarks_not_actual_or_byte_identical_reuse',
        'source_recruitment_effect_excluded':'no_B167_effect_or_source_command_omitted',
        "block['block'] == checked['block'] == 166":"block['block'] == checked['block'] == 167",
        "len(block['command_map']) == 62 and len(block['relative_skip_fixups']) == 8":"len(block['command_map']) == 46 and len(block['relative_skip_fixups']) == 12",
        "len(block['target_native_skip_cases']) == 40 and len(block['text_records']) == 42":"len(block['target_native_skip_cases']) == 60 and len(block['text_records']) == 27",
        "== [2948]":"== [430,2172]",'dk4-lil-B166-source-relocation-map-v1':'dk4-lil-B167-source-relocation-map-v1',
        'all62_commands8_relative_sites40_target_skips_verified':'all46_commands12_relative_sites60_target_skips_verified',
        'all42_active_speech_targets_preserved':'all27_active_speech_targets_preserved',
        'all11_opaque_leaves_one_predicate_one_effect_two_resources_six_presentations_and_end_exact':'all6_opaque_leaves_two_predicates_two_resources_and_two_ends_exact',
        'single_declared_tail_end_after_advice_rejoin_preserved':'two_separate_refusal_and_lecture_endwords_preserved',
        'all44_source_native_reference_and_representative_rules_approved':'all29_source_native_reference_and_representative_rules_approved',
        '44 approvals sealed:41 actual speeches/1 offline Fernando remark,both advice choices,62commands/8spans/40skips,168storedcases.':'29 approvals sealed:25 actual speeches/two offline Cesare remarks,both choices,46commands/12spans/60skips,108storedcases.'
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,scope=dict(speeches=27,labels=2,actual_speeches=25,offline_conditional_speeches=2,source_ends=[430,2172],commands=46,relative_sites=12),no_new_credit_ROM_or_registry_change=True))
