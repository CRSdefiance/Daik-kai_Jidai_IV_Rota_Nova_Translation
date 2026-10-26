"""Derive the 29-object authoring receipt with exact B167 proof dependencies."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT = Path('work/analysis/lil_B167_author_tools_v4129')
if __name__=='__main__':
    assert not ROOT.exists()
    pair=derive('scripts/author_lil_B166_v4065.py','scripts/author_lil_B167_v4129.py',{
        'lil_B166_prose_v4064':'lil_B167_prose_v4128','lil_B166_author_v4065':'lil_B167_author_v4129',
        'lil_B166_comparison_v4063/all44_current_effective_comparison_packet':'lil_B167_comparison_v4127/all29_current_effective_comparison_packet',
        'lil_B166_clean_context_v4053/all44_complete_B166_exchange_and_fresh_glosses':'lil_B167_clean_context_v4117/all29_complete_B167_exchange_and_fresh_glosses',
        'lil_B166_editorial_manuscript_v1':'lil_B167_editorial_manuscript_v1','lil_B166_choice_manuscript_v1':'lil_B167_choice_manuscript_v1',
        'all44_clean_first_glosses_before_predecessor_English':'all29_clean_first_glosses_before_predecessor_English',
        'len(prose.REVISIONS)==24 and len(prose.RETAIN_NOTES)==18':'len(prose.REVISIONS)==16 and len(prose.RETAIN_NOTES)==11',
        'lil_B166_voices_v4056/current4_static_names_voices_and207_catalog_rebind':'lil_B167_voices_v4120/current5_static_names_voices_and207_catalog_rebind',
        'lil_B166_branches_v4058':'lil_B167_branches_v4122',
        'lil_B166_entry_v4059/source_EV2_B166_action_dependency_and_native_getter_binding':'lil_B167_entry_v4123/source_EV2_B167_action_dependency_and_native_getter_binding',
        'lil_B166_controls_v4061/Fernando_predicate_two_resources_advice_paths_and11_leaves':'lil_B167_controls_v4125/two_Cesare_queries_two_resources_four_paths_and6_leaves',
        'lil_B166_names_v4060/six_original_Manuel_Fernando_Camille_name_consumers':'lil_B167_names_v4124b/ten_original_names_owned_scratch_and_readonly_paths',
        'Player choice about hearing advice;not employment':'Player choice about hearing a sail lecture;not employment or payment',
        "{2:'Lil',9:'Camille',20:'Fernando Dias',23:'Manuel Almeida'}":"{2:'Lil',4:'Janus Pasar',13:'Cesare Tony',23:'Manuel Almeida',109:'Shipwright'}",
        "len(allrows)==44 and counts=={'revise':24,'retain-wording':20}":"len(allrows)==29 and counts=={'revise':16,'retain-wording':13}",
        'all44_clean_first_contextual_decisions':'all29_clean_first_contextual_decisions',
        'all44_clean_then_current_complete_exchange_and_branches_read':'all29_clean_then_current_complete_exchange_and_branches_read',
        'source_FI3_preserved':'source_no_FI_FA_FO_preserved',
        'all20_retentions_individually_justified':'all13_retentions_individually_justified',
        'source_ship_care_metaphor_and_all_room_role_condition_resource_and_location_facts_preserved':'source_lecture_orientation_wind_types_positions_compatibility_size_mast_and_angle_facts_preserved',
        'spoken_acceptance_before_menu_both_advice_outcomes_and_later_effect_distinguished':'both_lecture_choices_separate_ends_and_later_Cesare_predicate_result_state_distinguished',
        'objects=44,speeches=42,choices=2':'objects=29,speeches=27,choices=2','FI=3':'FI=0',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=pair,expected_revisions=16,expected_retentions=13,
        all29_remain_uncredited_and_formatting_native_release_pending=True,no_ROM_registry_ledger_change=True))
    print('B167 29-object authoring successor created.')
