"""Prepare complete B177 predecessor comparison after clean glosses and native/term binding."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B177_comparison_tools_v4610')
assert not root.exists()
tool=derive('scripts/compare_lil_B176_effective_v4556.py','scripts/compare_lil_B177_effective_v4610.py',{
    'B176':'B177','lil_B176':'lil_B177','comparison_v4556':'comparison_v4610',
    'source_v4548':'source_v4602','clean_context_v4547':'clean_context_v4601',
    'dispatches_v4550':'dispatches_v4604','voices_v4549':'voices_v4603',
    'names_v4553':'names_v4607','entry_v4552':'entry_v4606','controls_v4554':'controls_v4608',
    'branches_v4551':'branches_v4605',
    'terms_v4555/Owner_Cook_Seville_and_prospective_banana_fashion_reconciliation':
        'terms_v4609/Owner_Cook_Genoa_and_prospective_tomato_fashion_reconciliation',
    '== [(176,176,177)]':'== [(177,177,178)]',
    "effect['source_declared_end_offsets'] == [386]":"effect['source_declared_end_offsets'] == [482]",
    'All10 clean-first glosses and current source/name/term bindings precede this exposure.':
        'All10 clean-first glosses precede predecessor comparison;current source/name/term bindings precede this complete packet. The incidental closing-line/name-search exposure is recorded in the terms proof.',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,no_editorial_credit_added=True,full_goal_complete=False))
