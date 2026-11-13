"""Prepare the next clean-source exchange inventory; execution requires verified B46 completion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_next_clean_tools_v7971')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/inventory_Rafael_next_clean_v7918.py','scripts/inventory_Rafael_next_clean_v7971.py',{
        'Rafael_next_clean_v7918':'Rafael_next_clean_v7971',
        'editorial_handoff_verification_v7917':'editorial_handoff_verification_v7970',
        '==6950':'==6976',
        'B46':'B47',
        'for number in [46]':'for number in [47]',
        "if g['block']==46":"if g['block']==47",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared clean B47 inventory;no current English exposed,no source orcompletion credit. Requires verifiedV7970 first.')
