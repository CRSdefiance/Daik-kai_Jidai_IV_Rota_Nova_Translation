"""Read the next complete clean scene without importing predecessor assumptions or English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B206_inventory_tools_v6230')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/inventory_lil_B205_clean_v6170.py','scripts/inventory_lil_B206_clean_v6230.py',{'B205':'B206','inventory_v6170':'inventory_v6230','.blocks[205]':'.blocks[206]','block=205':'block=206'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory_derivation.json',dict(tool=tool,no_inherited_object_actor_macro_branch_end_or_tail_count=True,no_predecessor_English_read=True,no_ROM_registry_ledger_or_review_credit_change=True,full_goal_complete=False))
