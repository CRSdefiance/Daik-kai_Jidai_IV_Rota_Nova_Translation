"""Expose B179 predecessor English after clean context,distinct name consumers and terms."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_comparison_tools_v4719');assert not ROOT.exists()
tool=derive('scripts/compare_lil_B178_effective_v4670.py','scripts/compare_lil_B179_effective_v4719.py',{
    'lil_B178_comparison_v4670':'lil_B179_comparison_v4719',
    'lil_B178_source_v4662/all13':'lil_B179_source_v4708/all14',
    'lil_B178_clean_context_v4661/all13_complete_B178':'lil_B179_clean_context_v4707/all14_complete_B179',
    'lil_B178_dispatches_v4664/all13_source_current_dispatches_no_macros_and3_control_leaves':
        'lil_B179_dispatches_v4710/all14_source_current_dispatches_no_macros_and2_control_leaves',
    'lil_B178_voices_v4663':'lil_B179_voices_v4709',
    'lil_B178_names_v4667b/six_original_Lady166_167_168_name_consumers_readonly_paths':
        'lil_B179_names_v4713b/six_original_Barkeep_Patron_Retainer_name_consumers',
    'lil_B178_entry_v4666/source_EV2_B178':'lil_B179_entry_v4712/source_EV2_B179',
    'lil_B178_controls_v4668/one_A000_C200_single_end_and3_source_leaves':
        'lil_B179_controls_v4714/one_A000_no_C200_single_end_and2_source_leaves',
    'lil_B178_branches_v4665':'lil_B179_branches_v4711',
    'lil_B178_terms_v4669/three_Ladies_Amsterdam_Wheat_and_prospective_home_baking_fashion_reconciliation':
        'lil_B179_terms_v4718/Barkeep_Patron_Sailor_Sao_Jorge_Wine_and_prospective_fashion_reconciliation',
    'all13':'all14','All13':'All14',"== 26 and len(voice":"== 28 and len(voice",
    "entry['selected_B178_source_events']] == [(178,178,179)]":"entry['selected_B179_source_events']] == [(179,179,180)]",
    '== [490]':'== [508]','len(rows) == 13':'len(rows) == 14',
    'B178_source_and_current_effective':'B179_source_and_current_effective','Complete B178':'Complete B179',
    'objects=13,progressive=12':'objects=14,progressive=13',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,all14_clean_glosses_and_source_dialogue_identity_distinction_precede_comparison=True,
    translated_city_alias_and_wine_bound_separate_untranslated_city_alias_lead_preserved=True,
    no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
