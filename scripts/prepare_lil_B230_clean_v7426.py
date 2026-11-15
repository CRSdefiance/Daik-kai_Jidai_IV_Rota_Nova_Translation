"""Prepare the next complete clean-Japanese inventory without exposing predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_clean_tools_v7426')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/inventory_lil_B230_clean_v7426.py').exists()
    r=derive('scripts/inventory_lil_B229_clean_v7379.py','scripts/inventory_lil_B230_clean_v7426.py',{'B229':'B230','v7379':'v7426','blocks[229]':'blocks[230]','block=229':'block=230'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',dict(tool=r,no_predecessor_English_read=True,new_credit=0,full_goal_complete=False))
