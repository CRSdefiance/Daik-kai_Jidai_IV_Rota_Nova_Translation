"""Prepare the first whole-exchange English comparison after clean/native/term binding."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_comparison_tools_v4269')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/compare_lil_B169_effective_v4220.py','scripts/compare_lil_B170_effective_v4269.py',{
        'Expose all36 current paragraphs':'Expose all33 current paragraphs',
        'lil_B169_comparison_v4220':'lil_B170_comparison_v4269',
        'lil_B169_source_v4211/all36_clean_current_complete_context':'lil_B170_source_v4260/all33_clean_current_complete_context',
        'lil_B169_clean_context_v4210/all36_complete_B169_exchange':'lil_B170_clean_context_v4257/all33_complete_B170_exchange',
        'lil_B169_dispatches_v4214/all36_source_current_dispatches_FI5_FO2_and5_control_leaves':'lil_B170_dispatches_v4263/all33_source_current_dispatches_FI1_FO1_and12_control_leaves',
        'lil_B169_voices_v4213/current6_static_names_voices':'lil_B170_voices_v4262/current2_static_names_voices',
        'lil_B169_names_v4217/twelve_original_name_consumers':'lil_B170_names_v4266/four_original_name_consumers',
        'lil_B169_entry_v4216/source_EV2_B169':'lil_B170_entry_v4265/source_EV2_B170',
        'lil_B169_controls_v4218/three_predicates_five_leaves_and_eight_source_paths':'lil_B170_controls_v4267/two_resources_C200_pause_two_ends_and12_source_leaves',
        'lil_B169_branches_v4215':'lil_B170_branches_v4264',
        'lil_B169_terms_v4219/current_Proof_title_Tavern_ruins_names_and_older_variant_refs':'lil_B170_terms_v4268/current_Taoist_arts_Yifa_names_and_source_address_reconciliation',
        'all36_clean_source_read':'all33_clean_source_read',
        "len(control['speech_dispatch_cases']) == 72 and len(voice['fresh6_actor_names']['rows']) == 6":"len(control['speech_dispatch_cases']) == 66 and len(voice['fresh2_actor_names']['rows']) == 2",
        "len(names['native_twelve_consumer_cases']['rows']) == 12":"len(names['native_four_consumer_cases']['rows']) == 4",
        "entry['selected_B169_source_events']] == [(169,169,170)]":"entry['selected_B170_source_events']] == [(170,170,171)]",
        "effect['source_declared_end_offsets'] == [2558] and len(effect['source_predicate_cases']) == 3 and len(branch['cases']) == 120":"effect['source_declared_end_offsets'] == [1852,1856] and len(effect['source_predicate_cases']) == 0 and len(branch['cases']) == 0",
        'len(rows) == 36':'len(rows) == 33','B169_source_and_current_effective':'B170_source_and_current_effective',
        'Complete B169 source/current comparison. All36':'Complete B170 source/current comparison. All33',
        'all36_current_effective_comparison_packet':'all33_current_effective_comparison_packet',
        'all36_clean_first_meanings_names_control_paths_and_current_terms_bound':'all33_clean_first_meanings_names_control_paths_and_current_terms_bound',
        'objects=36,progressive=36':'objects=33,progressive=33',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('First33-paragraph B170 comparison producer prepared;clean/native/name/term prerequisites required.')
