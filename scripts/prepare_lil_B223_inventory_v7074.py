"""Preserve the next complete clean block without exposing predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_inventory_tools_v7074')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/inventory_lil_B222_clean_v6964.py','scripts/inventory_lil_B223_clean_v7074.py',{'B222':'B223','v6964':'v7074','blocks[222]':'blocks[223]','block=222':'block=223'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_only_inventory.json',dict(tool=tool,no_current_or_predecessor_English_read=True,no_native_address_change=True,new_credit=0,full_goal_complete=False))
