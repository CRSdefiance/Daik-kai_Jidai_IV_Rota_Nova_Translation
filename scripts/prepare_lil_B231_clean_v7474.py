"""Prepare the next whole clean-Japanese exchange without older English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_clean_tools_v7474')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/inventory_lil_B230_clean_v7426.py','scripts/inventory_lil_B231_clean_v7474.py',{'B230':'B231','v7426':'v7474','blocks[230]':'blocks[231]','block=230':'block=231'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',dict(tool=row,no_predecessor_English_read=True,new_credit=0,full_goal_complete=False))
