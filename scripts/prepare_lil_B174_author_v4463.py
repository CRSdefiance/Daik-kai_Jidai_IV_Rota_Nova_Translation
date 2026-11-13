"""Derive the B174 v2 manuscript producer with all33 explicit contextual decisions."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_author_tools_v4463')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/author_lil_B173_v4421.py','scripts/author_lil_B174_v4463.py',{
        'Record11 complete-exchange decisions':'Record33 complete-exchange decisions',
        'lil_B173_prose_v4420':'lil_B174_prose_v4462','lil_B173_author_v4421':'lil_B174_author_v4463',
        'lil_B173_comparison_v4419/all11_current_effective_comparison_packet':'lil_B174_comparison_v4461/all33_current_effective_comparison_packet',
        'lil_B173_clean_context_v4410/all11_complete_B173_exchange':'lil_B174_clean_context_v4451/all33_complete_B174_exchange',
        'lil_B173_editorial_manuscript_v1':'lil_B174_editorial_manuscript_v1',
        'all11_clean_source':'all33_clean_source',
        'len(prose.REVISIONS) == 8 and len(prose.RETAIN_NOTES) == 3':'len(prose.REVISIONS) == 23 and len(prose.RETAIN_NOTES) == 10',
        'lil_B173_voices_v4412/current2_static_names':'lil_B174_voices_v4454/current4_static_names',
        'lil_B173_branches_v4414':'lil_B174_branches_v4456',
        'lil_B173_entry_v4415/source_EV2_B173':'lil_B174_entry_v4457/source_EV2_B174',
        'lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end':
            'lil_B174_controls_v4459/one_resource_conditional_Emilio_four_spans_two_A000s_C200_and_single_end',
        'lil_B173_names_v4416/four_original_name_consumers':'lil_B174_names_v4458/eight_original_name_consumers',
        "speakers = {2:'Lil',202:'Reika'}":"speakers = {2:'Lil',14:'Emilio',26:'Julian',201:'Mihwa'}",
        "{'revise':8,'retain-wording':3}":"{'revise':23,'retain-wording':10}",
        'revised=8, retained=3':'revised=23, retained=10',
        'all11_clean_first_contextual_decisions':'all33_clean_first_contextual_decisions',
        'all11_clean_then_current_whole_exchange_read':'all33_clean_then_current_whole_exchange_read',
        'all3_retentions_individually_justified':'all10_retentions_individually_justified',
        'native_Lil_Reika_spoken_Julian_current_crown_and_tomb_title_bindings_used=True':
            'native_Lil_Emilio_Julian_Mihwa_crown_tomb_and_Seoul_bindings_used=True',
        'guarded_recognition_reported_beauty_and_recent_other_question_preserved=True':
            'Lil_first_crown_discovery_transfer_and_actual_new_employment_preserved=True',
        'uncertain_name_recollection_smooth_talker_and_apparent_tomb_departure_preserved=True':
            'extraordinary_running_claim_collapse_rest_and_optional_Emilio_hunger_preserved=True',
        'Lil_tentative_inquiry_surprise_named_echo_and_competitive_inference_preserved=True':
            'gratitude_gift_banter_earnest_aspiration_flattery_jealousy_placation_and_closing_aside_preserved=True',
        'no_established_romance_kinship_rank_precise_location_item_power_or_earned_state_invented=True':
            'actual_grandfather_kinship_and_conditional_better_item_date_preserved_without_romance_status_rank_or_earned_state=True',
        'objects=11, progressive=11':'objects=33, progressive=33',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,revisions=23,retentions=10,
        no_formatting_approval_orledger_credit=True,full_goal_complete=False))
    print('Prepared33 complete-context B174 decisions,23 revisions and10 justified retentions; formatting remains open.')
