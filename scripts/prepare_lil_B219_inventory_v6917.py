"""Freeze the next clean-only inventory producer without exposing predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B219_inventory_tools_v6917');assert not root.exists();root.mkdir(parents=True)
    proof=derive('scripts/inventory_lil_B218_clean_v6872.py','scripts/inventory_lil_B219_clean_v6917.py',{'B218':'B219','6872':'6917','blocks[218]':'blocks[219]','block=218':'block=219'})
    save(root/'source_locked_derivation.json',proof)
