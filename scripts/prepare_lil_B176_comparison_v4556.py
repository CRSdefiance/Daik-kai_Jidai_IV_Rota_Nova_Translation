"""Prepare complete B176 predecessor comparison only after source/native/term binding."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_comparison_tools_v4556')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/compare_lil_B175_effective_v4511.py','scripts/compare_lil_B176_effective_v4556.py',{
        'lil_B175_comparison_v4511':'lil_B176_comparison_v4556',
        'lil_B175_source_v4503/all32_clean_current_complete_context':'lil_B176_source_v4548/all10_clean_current_complete_context',
        'lil_B175_clean_context_v4502/all32_complete_B175_exchange':'lil_B176_clean_context_v4547/all10_complete_B176_exchange',
        'lil_B175_dispatches_v4505/all32_source_current_dispatches_FI4_FA1_and7_control_leaves':
            'lil_B176_dispatches_v4550/all10_source_current_dispatches_no_macros_and3_control_leaves',
        'lil_B175_voices_v4504/current5_static_names':'lil_B176_voices_v4549/current2_static_names',
        'lil_B175_names_v4508/ten_original_name_consumers_owned_and_readonly_paths':
            'lil_B176_names_v4553/four_original_Owner_Cook_name_consumers_readonly_paths',
        'lil_B175_entry_v4507/source_EV2_B175':'lil_B176_entry_v4552/source_EV2_B176',
        'lil_B175_controls_v4509/one_resource_three_presentations_C200_two_ends_and7_source_leaves':
            'lil_B176_controls_v4554/one_A000_C200_single_end_and3_source_leaves',
        'lil_B175_branches_v4506':'lil_B176_branches_v4551',
        'lil_B175_terms_v4510/current_five_names_anonymous_woman_unidentified_sword_and_admiral_reconciliation':
            'lil_B176_terms_v4555/Owner_Cook_Seville_and_prospective_banana_fashion_reconciliation',
        "len(control['speech_dispatch_cases']) == 64 and len(voice['fresh5_actor_names']['rows']) == 5":
            "len(control['speech_dispatch_cases']) == 20 and len(voice['fresh2_actor_names']['rows']) == 2",
        "len(names['native_ten_consumer_cases']['rows']) == 10":"len(names['native_four_consumer_cases']['rows']) == 4",
        "entry['selected_B175_source_events']] == [(175,175,176)]":"entry['selected_B176_source_events']] == [(176,176,177)]",
        "effect['source_declared_end_offsets'] == [1702,1706]":"effect['source_declared_end_offsets'] == [386]",
        'all32':'all10','All32':'All10','len(rows) == 32':'len(rows) == 10',
        'objects=32,progressive=23,FE=9':'objects=10,progressive=9,FE=1','B175':'B176',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,two_readonly_names_one_impersonal_FE_Seville_bound_before_comparison=True,
        no_credit=True,full_goal_complete=False))
    print('Prepared B176 complete10 predecessor comparison after clean-first meanings,native identities and terms.')
