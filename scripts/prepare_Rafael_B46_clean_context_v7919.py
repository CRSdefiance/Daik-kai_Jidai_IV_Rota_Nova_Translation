"""Inventory the original event-38 prerequisite as source context only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_clean_context_tools_v7919');assert not root.exists()
    row=derive('scripts/inventory_Rafael_next_clean_v7918.py','scripts/inventory_Rafael_B46_clean_context_v7919.py',{
        'Rafael_next_clean_v7918':'Rafael_B46_clean_context_v7919',
        'B46':'B38',
        'for number in [46]':'for number in [38]',
        "if g['block']==46":"if g['block']==38",
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
