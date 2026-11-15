"""Prepare a source-only untouched B46 inventory, without assuming chronological adjacency."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_next_clean_tools_v7918');assert not root.exists()
    row=derive('scripts/inventory_Rafael_next_clean_v7864.py','scripts/inventory_Rafael_next_clean_v7918.py',{
        'Rafael_next_clean_v7864':'Rafael_next_clean_v7918',
        'editorial_handoff_verification_v7863':'editorial_handoff_verification_v7917',
        '==6938':'==6950',
        'B45':'B46',
        'for number in [45]':'for number in [46]',
        "if g['block']==45":"if g['block']==46",
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
