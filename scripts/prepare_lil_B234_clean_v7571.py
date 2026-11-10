"""Inventory the following clean block before any predecessor English is exposed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_clean_tools_v7571')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/inventory_lil_B233_clean_v7523.py','scripts/inventory_lil_B234_clean_v7571.py',{'B233':'B234','v7523':'v7571','blocks[233]':'blocks[234]','block=233':'block=234'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_next_clean_inventory.json',dict(tool=row,read_no_predecessor_English=True,new_credit=0,full_goal_complete=False))
