"""Inventory the next clean exchange without exposing predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_clean_tools_v7332')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/inventory_lil_B227_clean_v7285.py','scripts/inventory_lil_B228_clean_v7332.py',{'B227':'B228','v7285':'v7332','blocks[227]':'blocks[228]','block=227':'block=228'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_inventory.json',r)
