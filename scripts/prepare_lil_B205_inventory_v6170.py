"""Inventory the next clean block without inheriting B204's source shape or English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_inventory_tools_v6170')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/inventory_lil_B204_clean_v6058.py','scripts/inventory_lil_B205_clean_v6170.py',{'B204':'B205','clean_inventory_v6058':'clean_inventory_v6170','blocks[204]':'blocks[205]','block=204':'block=205'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory_derivation.json',dict(tool=tool,all_native_addresses_and_generic_inventory_logic_preserved=True,no_object_actor_macro_branch_end_or_English_shape_assumption=True,full_goal_complete=False));print('Clean B205 inventory prepared without source-shape or older-English assumptions.')
