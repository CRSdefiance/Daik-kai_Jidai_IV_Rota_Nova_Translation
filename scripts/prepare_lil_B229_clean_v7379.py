"""Prepare the next clean-only inventory without exposing older English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_clean_tools_v7379')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/inventory_lil_B229_clean_v7379.py').exists()
    r=derive('scripts/inventory_lil_B228_clean_v7332.py','scripts/inventory_lil_B229_clean_v7379.py',{'B228':'B229','v7332':'v7379','blocks[228]':'blocks[229]','block=228':'block=229'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',dict(tool=r,no_predecessor_English_read=True,new_credit=0,full_goal_complete=False))
