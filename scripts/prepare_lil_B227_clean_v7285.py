"""Inventory the next uncredited exchange from clean Japanese only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_clean_tools_v7285')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/inventory_lil_B226_clean_v7238.py','scripts/inventory_lil_B227_clean_v7285.py',{'B226':'B227','v7238':'v7285','blocks[226]':'blocks[227]','block=226':'block=227'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_inventory.json',r)
