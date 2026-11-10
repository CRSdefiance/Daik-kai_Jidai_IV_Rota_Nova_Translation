"""Prepare a clean-only B48 inventory after verified B47 completion; no chronology assumption."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_next_clean_tools_v8020')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/inventory_Rafael_next_clean_v7971.py','scripts/inventory_Rafael_next_clean_v8020.py',{
        'Rafael_next_clean_v7971':'Rafael_next_clean_v8020',
        'editorial_handoff_verification_v7970':'editorial_handoff_verification_v8019',
        '==6976':'==6991','B47':'B48','for number in [47]':'for number in [48]',
        "if g['block']==47":"if g['block']==48",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Clean B48 inventory prepared;current English remains unread;no source/prose orcompletion credit.')
