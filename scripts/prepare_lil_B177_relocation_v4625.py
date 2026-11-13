"""Prepare reversible B177 relocation and fresh stored native targets for the four-row speech."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B177_relocation_tools_v4625')
assert not root.exists()
relocation=derive('scripts/research_lil_B176_relocation_v4575.py','scripts/research_lil_B177_relocation_v4625.py',{
    'B176':'B177','lil_B176':'lil_B177',
    'relocation_v4575':'relocation_v4625','editorial_manuscript_v3':'editorial_manuscript_v5',
    'all_routes_combined_v4541':'all_routes_combined_v4595',
    'number==176':'number==177','[176]':'[177]',
    '[386] # the complete source tail endword is preserved':'[482] # the complete source tail endword is preserved',
})
stored=derive('scripts/prove_lil_B176_stored_v4576.py','scripts/prove_lil_B177_stored_v4626.py',{
    'B176':'B177','lil_B176':'lil_B177',
    'stored_v4576':'stored_v4626','editorial_manuscript_v3':'editorial_manuscript_v5',
    'relocation_v4575':'relocation_v4625','fonts_v4570':'fonts_v4621',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(relocation=relocation,stored=stored,
    source_scope=dict(block=177,speeches=10,progressive=9,FE=1,commands=13,nonrelative_leaves=3,
        relative_sites=0,predicates=0,A000=1,C200=1,source_end_offsets=[482]),
    four_row_R12_and_all_other_reviewed_prose_unchanged=True,no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
