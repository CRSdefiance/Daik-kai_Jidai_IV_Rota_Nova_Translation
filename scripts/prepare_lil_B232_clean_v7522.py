"""Inventory the next complete Japanese exchange without reading predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B232_clean_tools_v7522')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/inventory_lil_B231_clean_v7474.py','scripts/inventory_lil_B232_clean_v7522.py',{'B231':'B232','v7474':'v7522','blocks[231]':'blocks[232]','block=231':'block=232'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_next_clean_inventory.json',dict(tool=row,read_no_predecessor_English=True,new_credit=0,full_goal_complete=False))
