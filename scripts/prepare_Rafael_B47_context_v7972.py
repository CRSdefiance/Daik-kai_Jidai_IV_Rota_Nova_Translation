"""Prepare original event37 prerequisite context for B47 without current English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_clean_context_tools_v7972')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/inventory_Rafael_next_clean_v7971.py','scripts/inventory_Rafael_B47_clean_context_v7972.py',{
        'Rafael_next_clean_v7971':'Rafael_B47_clean_context_v7972',
        'B47':'B37',
        'for number in [47]':'for number in [37]',
        "if g['block']==47":"if g['block']==37",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B47 original event37 prerequisite context inventory;source only,no current-English exposure orcredit.')
