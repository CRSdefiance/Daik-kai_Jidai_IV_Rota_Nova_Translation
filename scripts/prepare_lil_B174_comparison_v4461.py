"""Prepare full predecessor comparison only after clean meanings and native bindings."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_comparison_tools_v4461')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/compare_lil_B173_effective_v4419.py','scripts/compare_lil_B174_effective_v4461.py',{
        'lil_B173_comparison_v4419':'lil_B174_comparison_v4461',
        'lil_B173_source_v4411/all11_clean_current_complete_context':'lil_B174_source_v4453/all33_clean_current_complete_context',
        'lil_B173_clean_context_v4410/all11_complete_B173_exchange':'lil_B174_clean_context_v4451/all33_complete_B174_exchange',
        'lil_B173_dispatches_v4413/all11_source_current_dispatches':'lil_B174_dispatches_v4455/all33_source_current_dispatches',
        'lil_B173_voices_v4412/current2_static_names':'lil_B174_voices_v4454/current4_static_names',
        'lil_B173_names_v4416/four_original_name_consumers':'lil_B174_names_v4458/eight_original_name_consumers',
        'lil_B173_entry_v4415/source_EV2_B173':'lil_B174_entry_v4457/source_EV2_B174',
        'lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end':
            'lil_B174_controls_v4459/one_resource_conditional_Emilio_four_spans_two_A000s_C200_and_single_end',
        'lil_B173_branches_v4414':'lil_B174_branches_v4456',
        'lil_B173_terms_v4418/current_crown_tomb_Reika_and_uncertain_Julian_lead_reconciliation':
            'lil_B174_terms_v4460/current_four_names_crown_tomb_Seoul_and_conditional_date_reconciliation',
        "len(control['speech_dispatch_cases']) == 22 and len(voice['fresh2_actor_names']['rows']) == 2":
            "len(control['speech_dispatch_cases']) == 66 and len(voice['fresh4_actor_names']['rows']) == 4",
        "len(names['native_four_consumer_cases']['rows']) == 4":"len(names['native_eight_consumer_cases']['rows']) == 8",
        "entry['selected_B173_source_events']] == [(173,173,174)]":"entry['selected_B174_source_events']] == [(174,174,175)]",
        "effect['source_declared_end_offsets'] == [762]":"effect['source_declared_end_offsets'] == [2086]",
        'all11':'all33','All11':'All33','len(rows) == 11':'len(rows) == 33',
        'objects=11,progressive=11':'objects=33,progressive=33','B173':'B174',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        clean_meanings_and_all_bindings_precede_comparison=True,no_credit=True,full_goal_complete=False))
    print('Prepared full33 B174 source/effective-current comparison.')
