"""Expose the first37-paragraph B171 comparison only after clean/native/term gates."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B171_comparison_tools_v4319')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/compare_lil_B170_effective_v4269.py', 'scripts/compare_lil_B171_effective_v4319.py', {
        'Expose all33 current paragraphs': 'Expose all37 current paragraphs',
        'lil_B170_comparison_v4269': 'lil_B171_comparison_v4319',
        'lil_B170_source_v4260/all33_clean_current_complete_context': 'lil_B171_source_v4311/all37_clean_current_complete_context',
        'lil_B170_clean_context_v4257/all33_complete_B170_exchange': 'lil_B171_clean_context_v4309/all37_complete_B171_exchange',
        'lil_B170_dispatches_v4263/all33_source_current_dispatches_FI1_FO1_and12_control_leaves': 'lil_B171_dispatches_v4313/all37_source_current_dispatches_FI1_FO0_and8_control_leaves',
        'lil_B170_voices_v4262/current2_static_names_voices': 'lil_B171_voices_v4312/current3_static_names_voices',
        'lil_B170_names_v4266/four_original_name_consumers': 'lil_B171_names_v4316/six_original_name_consumers',
        'lil_B170_entry_v4265/source_EV2_B170': 'lil_B171_entry_v4315/source_EV2_B171',
        'lil_B170_controls_v4267/two_resources_C200_pause_two_ends_and12_source_leaves': 'lil_B171_controls_v4317/one_resource_C200_four_presentations_two_ends_and8_source_leaves',
        'lil_B170_branches_v4264': 'lil_B171_branches_v4314',
        'lil_B170_terms_v4268/current_Taoist_arts_Yifa_names_and_source_address_reconciliation': 'lil_B171_terms_v4318b/current_Taoist_arts_Sanghyeon_training_bond_and_new_facts_reconciliation',
        'all33_clean_source_read': 'all37_clean_source_read',
        "len(control['speech_dispatch_cases']) == 66 and len(voice['fresh2_actor_names']['rows']) == 2": "len(control['speech_dispatch_cases']) == 74 and len(voice['fresh3_actor_names']['rows']) == 3",
        "len(names['native_four_consumer_cases']['rows']) == 4": "len(names['native_six_consumer_cases']['rows']) == 6",
        "entry['selected_B170_source_events']] == [(170,170,171)]": "entry['selected_B171_source_events']] == [(171,171,172)]",
        "effect['source_declared_end_offsets'] == [1852,1856]": "effect['source_declared_end_offsets'] == [2112,2116]",
        'len(rows) == 33': 'len(rows) == 37', 'B170_source_and_current_effective': 'B171_source_and_current_effective',
        'Complete B170 source/current comparison. All33': 'Complete B171 source/current comparison. All37',
        'all33_current_effective_comparison_packet': 'all37_current_effective_comparison_packet',
        'all33_clean_first_meanings_names_control_paths_and_current_terms_bound': 'all37_clean_first_meanings_names_control_paths_and_current_terms_bound',
        'objects=33,progressive=33': 'objects=37,progressive=37',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool, no_ROM_registry_ledger_orcredit_change=True, full_goal_complete=False))
