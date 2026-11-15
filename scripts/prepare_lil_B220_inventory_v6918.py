"""Preserve the following clean-only block after empty B219, without prose credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B220_inventory_tools_v6918');assert not root.exists();root.mkdir(parents=True)
    proof=derive('scripts/inventory_lil_B218_clean_v6872.py','scripts/inventory_lil_B220_clean_v6918.py',{'B218':'B220','6872':'6918','blocks[218]':'blocks[220]','block=218':'block=220'})
    save(root/'source_locked_derivation.json',proof)
