"""Expose all B178 predecessor paragraphs only after clean-first contextual bindings."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_comparison_tools_v4670')
assert not ROOT.exists()
tool=derive('scripts/compare_lil_B177_effective_v4610.py','scripts/compare_lil_B178_effective_v4670.py',{
    'lil_B177_comparison_v4610':'lil_B178_comparison_v4670',
    'lil_B177_source_v4602/all10':'lil_B178_source_v4662/all13',
    'lil_B177_clean_context_v4601/all10_complete_B177':'lil_B178_clean_context_v4661/all13_complete_B178',
    'lil_B177_dispatches_v4604/all10':'lil_B178_dispatches_v4664/all13',
    'lil_B177_voices_v4603/current2':'lil_B178_voices_v4663/current3',
    'lil_B177_names_v4607/four_original_Owner_Cook':'lil_B178_names_v4667b/six_original_Lady166_167_168',
    'lil_B177_entry_v4606/source_EV2_B177':'lil_B178_entry_v4666/source_EV2_B178',
    'lil_B177_controls_v4608':'lil_B178_controls_v4668','lil_B177_branches_v4605':'lil_B178_branches_v4665',
    'lil_B177_terms_v4609/Owner_Cook_Genoa_and_prospective_tomato_fashion_reconciliation':
        'lil_B178_terms_v4669/three_Ladies_Amsterdam_Wheat_and_prospective_home_baking_fashion_reconciliation',
    'all10':'all13','All10':'All13',
    "== 20 and len(voice['fresh2_actor_names']['rows']) == 2":"== 26 and len(voice['fresh3_actor_names']['rows']) == 3",
    "names['native_four_consumer_cases']['rows']) == 4":"names['native_six_consumer_cases']['rows']) == 6",
    "entry['selected_B177_source_events']] == [(177,177,178)]":"entry['selected_B178_source_events']] == [(178,178,179)]",
    "== [482]":"== [490]",'len(rows) == 10':'len(rows) == 13',
    'B177_source_and_current_effective':'B178_source_and_current_effective','Complete B177':'Complete B178',
    ' The incidental closing-line/name-search exposure is recorded in the terms proof.':'',
    'objects=10,progressive=9':'objects=13,progressive=12',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,all13_clean_glosses_and_three_roles_six_native_names_and_terms_precede_comparison=True,
    no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
