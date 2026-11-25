"""Prepare all33 individual natural-dialogue-v2 decisions from the completed comparison."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_author_tools_v4271')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/author_lil_B169_v4222.py','scripts/author_lil_B170_v4271.py',{
        'all36':'all33','len(prose.REVISIONS) == 19 and len(prose.RETAIN_NOTES) == 17':'len(prose.REVISIONS) == 21 and len(prose.RETAIN_NOTES) == 12',
        'lil_B169_prose_v4221':'lil_B170_prose_v4270','lil_B169_author_v4222':'lil_B170_author_v4271',
        'lil_B169_comparison_v4220':'lil_B170_comparison_v4269',
        'lil_B169_clean_context_v4210/all36_complete_B169_exchange':'lil_B170_clean_context_v4257/all33_complete_B170_exchange',
        'lil_B169_editorial_manuscript_v1':'lil_B170_editorial_manuscript_v1',
        'lil_B169_voices_v4213/current6_static_names_voices':'lil_B170_voices_v4262/current2_static_names_voices',
        'lil_B169_branches_v4215':'lil_B170_branches_v4264',
        'lil_B169_entry_v4216/source_EV2_B169':'lil_B170_entry_v4265/source_EV2_B170',
        'lil_B169_controls_v4218/three_predicates_five_leaves_and_eight_source_paths':'lil_B170_controls_v4267/two_resources_C200_pause_two_ends_and12_source_leaves',
        'lil_B169_names_v4217/twelve_original_name_consumers':'lil_B170_names_v4266/four_original_name_consumers',
        "{2:'Lil',6:'Julio Erneco',9:'Camille',20:'Fernando Dias',21:'Ian Dukov',76:'Mikhail'}":"{2:'Lil',25:'Yifa'}",
        "{'revise':19,'retain-wording':17}":"{'revise':21,'retain-wording':12}",
        'revised=19,retained=17':'revised=21,retained=12',
        'source_FI5_FA0_FO2_preserved':'source_FI1_FA0_FO1_preserved',
        'all17_retentions_individually_justified':'all12_retentions_individually_justified',
        'two_registered_current_replacements_retained_with_exact_provenance':'no_registered_current_replacements_in_this_source_exchange',
        'source_seven_treasures_sages_locations_map_shapes_legend_and_future_map_conditions_complete':'source_collision_argument_apology_flattery_Admiral_fleet_and_training_sequence_complete',
        'source_influential_people_often_have_clues_conditional_evil_holder_and_sealed_Proofs_distinctions_preserved':'source_teacher_scolding_continued_training_self_vindication_and_resolve_conditions_preserved',
        'source_unwanted_touch_threat_expert_flattery_and_tavern_information_give_and_take_sequence_preserved':'source_request_for_advice_ship_passage_agreement_names_and_final_encouragement_preserved',
        'current_HELP_Proof_of_Conquest_title_used_older_variant_consistency_lead_stays_open':'current_reviewed_Taoist_arts_term_and_native_Yifa_name_spelling_used',
        'no_Professor_degree_rank_kinship_specific_blow_price_gift_or_military_only_rule_invented':'no_teacher_gender_sister_relationship_degree_nationality_named_spell_price_reward_or_skill_threshold_invented',
        'objects=36,progressive=36':'objects=33,progressive=33',
        'FI=5,FA=0,FO=2':'FI=1,FA=0,FO=1',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('B170 author producer prepared:21 revisions/12 individual retentions;formatting remains pending.')
