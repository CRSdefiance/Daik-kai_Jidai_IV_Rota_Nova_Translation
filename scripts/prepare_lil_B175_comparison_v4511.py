"""Prepare B175 predecessor comparison after all clean meanings and native bindings."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B175_comparison_tools_v4511')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/compare_lil_B174_effective_v4461.py','scripts/compare_lil_B175_effective_v4511.py',{
        'lil_B174_comparison_v4461':'lil_B175_comparison_v4511',
        'lil_B174_source_v4453/all33_clean_current_complete_context':'lil_B175_source_v4503/all32_clean_current_complete_context',
        'lil_B174_clean_context_v4451/all33_complete_B174_exchange':'lil_B175_clean_context_v4502/all32_complete_B175_exchange',
        'lil_B174_dispatches_v4455/all33_source_current_dispatches_no_macros_and8_control_leaves':
            'lil_B175_dispatches_v4505/all32_source_current_dispatches_FI4_FA1_and7_control_leaves',
        'lil_B174_voices_v4454/current4_static_names':'lil_B175_voices_v4504/current5_static_names',
        'lil_B174_names_v4458/eight_original_name_consumers_and_owned_scratch_paths':
            'lil_B175_names_v4508/ten_original_name_consumers_owned_and_readonly_paths',
        'lil_B174_entry_v4457/source_EV2_B174':'lil_B175_entry_v4507/source_EV2_B175',
        'lil_B174_controls_v4459/one_resource_conditional_Emilio_four_spans_two_A000s_C200_and_single_end':
            'lil_B175_controls_v4509/one_resource_three_presentations_C200_two_ends_and7_source_leaves',
        'lil_B174_branches_v4456':'lil_B175_branches_v4506',
        'lil_B174_terms_v4460/current_four_names_crown_tomb_Seoul_and_conditional_date_reconciliation':
            'lil_B175_terms_v4510/current_five_names_anonymous_woman_unidentified_sword_and_admiral_reconciliation',
        "len(control['speech_dispatch_cases']) == 66 and len(voice['fresh4_actor_names']['rows']) == 4":
            "len(control['speech_dispatch_cases']) == 64 and len(voice['fresh5_actor_names']['rows']) == 5",
        "len(names['native_eight_consumer_cases']['rows']) == 8":"len(names['native_ten_consumer_cases']['rows']) == 10",
        "entry['selected_B174_source_events']] == [(174,174,175)]":"entry['selected_B175_source_events']] == [(175,175,176)]",
        "effect['source_declared_end_offsets'] == [2086] and len(effect['source_predicate_cases']) == 2 and len(branch['cases']) == 40":
            "effect['source_declared_end_offsets'] == [1702,1706] and not effect['source_predicate_cases'] and not branch['cases']",
        'all33':'all32','All33':'All32','len(rows) == 33':'len(rows) == 32',
        'objects=33,progressive=33,FE=0':'objects=32,progressive=23,FE=9','B174':'B175',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        five_names_nine_null_actor_FE_and_FI_FA_bound_before_comparison=True,no_credit=True,full_goal_complete=False))
    print('Prepared complete32 B175 effective-current comparison after clean-first/native/terminology bindings.')
