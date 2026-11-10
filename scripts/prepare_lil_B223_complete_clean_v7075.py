"""Expand all native automatic delivery notices before predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_complete_clean_tools_v7075')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/expand_lil_B214_clean_v6694.py','scripts/expand_lil_B223_clean_v7075.py',{'B214':'B223','clean_inventory_v6693':'clean_inventory_v7074','complete_clean_v6694':'complete_clean_v7075','block=214':'block=223'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_clean_getter.json',dict(tool=tool,all_native_addresses_original_clean_Getter_and_guards_preserved=True,source_all_typed_bodies_before_old_English=True,new_credit=0,full_goal_complete=False))
