"""Prepare whole-exchange English comparison after all clean/source bindings."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_comparison_tools_v4419')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/compare_lil_B172_effective_v4372.py','scripts/compare_lil_B173_effective_v4419.py',{
        'all27':'all11','All27':'All11','B172':'B173',
        'lil_B172_comparison_v4372':'lil_B173_comparison_v4419','lil_B172_source_v4364':'lil_B173_source_v4411',
        'lil_B172_clean_context_v4361':'lil_B173_clean_context_v4410',
        'lil_B172_dispatches_v4366/all27_source_current_dispatches_no_macros_and11_control_leaves':'lil_B173_dispatches_v4413/all11_source_current_dispatches_no_macros_and8_control_leaves',
        'lil_B172_voices_v4365':'lil_B173_voices_v4412','current3_static_names':'current2_static_names',
        'fresh3_actor_names':'fresh2_actor_names','lil_B172_names_v4369':'lil_B173_names_v4416',
        'six_original_name_consumers':'four_original_name_consumers','native_six_consumer_cases':'native_four_consumer_cases',
        'lil_B172_entry_v4368':'lil_B173_entry_v4415',
        'lil_B172_controls_v4370/three_resources_C200_five_presentations_later_A000_one_end_and11_source_leaves':'lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end',
        'lil_B172_branches_v4367':'lil_B173_branches_v4414',
        'lil_B172_terms_v4371/current_crown_Seoul_names_and_qualified_date_reconciliation':'lil_B173_terms_v4418/current_crown_tomb_Reika_and_uncertain_Julian_lead_reconciliation',
        "len(control['speech_dispatch_cases']) == 54":"len(control['speech_dispatch_cases']) == 22",
        "len(voice['fresh3_actor_names']['rows']) == 3":"len(voice['fresh2_actor_names']['rows']) == 2",
        "len(names['native_six_consumer_cases']['rows']) == 6":"len(names['native_four_consumer_cases']['rows']) == 4",
        '[(172,172,173)]':'[(173,173,174)]',
        "effect['source_declared_end_offsets'] == [1880] and len(effect['source_predicate_cases']) == 0 and len(branch['cases']) == 0":"effect['source_declared_end_offsets'] == [762] and len(effect['source_predicate_cases']) == 2 and len(branch['cases']) == 40",
        'len(rows) == 27':'len(rows) == 11','objects=27,progressive=27':'objects=11,progressive=11',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,all11_clean_first_glosses_and_current_names_terms_controls_bound=True,no_new_credit=True,full_goal_complete=False))
    print('Prepared complete B173 current-English comparison after clean-first11 glosses and native bindings.')
