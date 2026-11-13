"""Derive whole-exchange B173 authorship with eight revisions/three retentions."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_author_tools_v4421')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/author_lil_B172_v4374.py','scripts/author_lil_B173_v4421.py',{
        'B172':'B173','all27':'all11','Record27':'Record11',
        'lil_B172_prose_v4373':'lil_B173_prose_v4420','lil_B172_author_v4374':'lil_B173_author_v4421',
        'lil_B172_comparison_v4372':'lil_B173_comparison_v4419','lil_B172_clean_context_v4361':'lil_B173_clean_context_v4410',
        'len(prose.REVISIONS) == 19 and len(prose.RETAIN_NOTES) == 8':'len(prose.REVISIONS) == 8 and len(prose.RETAIN_NOTES) == 3',
        'lil_B172_voices_v4365/current3_static_names':'lil_B173_voices_v4412/current2_static_names',
        'lil_B172_branches_v4367':'lil_B173_branches_v4414','lil_B172_entry_v4368':'lil_B173_entry_v4415',
        'lil_B172_controls_v4370/three_resources_C200_five_presentations_later_A000_one_end_and11_source_leaves':'lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end',
        'lil_B172_names_v4369/six_original_name_consumers':'lil_B173_names_v4416/four_original_name_consumers',
        "speakers = {2:'Lil',26:'Julian',201:'Mihwa'}":"speakers = {2:'Lil',202:'Reika'}",
        "{'revise':19,'retain-wording':8}":"{'revise':8,'retain-wording':3}",'revised=19, retained=8':'revised=8, retained=3',
        'all8_retentions_individually_justified':'all3_retentions_individually_justified',
        'native_Julian_Mihwa_names_current_item_title_and_Seoul_bindings_used':'native_Lil_Reika_spoken_Julian_current_crown_and_tomb_title_bindings_used',
        'conditional_date_request_qualified_reply_and_overeager_promise_interpretation_preserved':'guarded_recognition_reported_beauty_and_recent_other_question_preserved',
        'reported_location_and_preciousness_forgotten_description_and_offer_request_role_reversal_preserved':'uncertain_name_recollection_smooth_talker_and_apparent_tomb_departure_preserved',
        'Lil_dry_aside_curiosity_and_independent_future_search_preserved':'Lil_tentative_inquiry_surprise_named_echo_and_competitive_inference_preserved',
        'objects=27, progressive=27':'objects=11, progressive=11',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_objects=11,revisions=8,individual_justified_retentions=3,
        clean_glosses_preceded_current_English=True,formatting_native_actual_and_release_pending=True,no_new_credit=True,full_goal_complete=False))
    print('Prepared11 B173 whole-exchange decisions;native formatting/references/actual/release remain pending.')
