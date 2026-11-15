"""Prepare the complete B172 predecessor comparison after clean/name/term/control binding."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_comparison_tools_v4372')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/compare_lil_B171_effective_v4319.py','scripts/compare_lil_B172_effective_v4372.py',{
        'all37':'all27','All37':'All27','lil_B171_comparison_v4319':'lil_B172_comparison_v4372',
        'lil_B171_source_v4311':'lil_B172_source_v4364','lil_B171_clean_context_v4309':'lil_B172_clean_context_v4361',
        'all37_complete_B171_exchange':'all27_complete_B172_exchange',
        'lil_B171_dispatches_v4313/all37_source_current_dispatches_FI1_FO0_and8_control_leaves':'lil_B172_dispatches_v4366/all27_source_current_dispatches_no_macros_and11_control_leaves',
        'lil_B171_voices_v4312':'lil_B172_voices_v4365','lil_B171_names_v4316':'lil_B172_names_v4369',
        'lil_B171_entry_v4315':'lil_B172_entry_v4368',
        'lil_B171_controls_v4317/one_resource_C200_four_presentations_two_ends_and8_source_leaves':'lil_B172_controls_v4370/three_resources_C200_five_presentations_later_A000_one_end_and11_source_leaves',
        'lil_B171_branches_v4314':'lil_B172_branches_v4367',
        'lil_B171_terms_v4318b/current_Taoist_arts_Sanghyeon_training_bond_and_new_facts_reconciliation':'lil_B172_terms_v4371/current_crown_Seoul_names_and_qualified_date_reconciliation',
        'B171':'B172',"len(control['speech_dispatch_cases']) == 74":"len(control['speech_dispatch_cases']) == 54",
        '[(171,171,172)]':'[(172,172,173)]','[2112,2116]':'[1880]','len(rows) == 37':'len(rows) == 27',
        'objects=37,progressive=37':'objects=27,progressive=27',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,clean_first27_glosses_and_terms_already_bound=True,no_new_credit=True,full_goal_complete=False))
