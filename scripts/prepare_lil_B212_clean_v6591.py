"""Preserve the next full clean source inventory before any earlier English is consulted."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_clean_tools_v6591')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/inventory_lil_B211_clean_v6545.py','scripts/inventory_lil_B212_clean_v6591.py',{'lil_B211_clean_inventory_v6545':'lil_B212_clean_inventory_v6591','all_clean_B211':'all_clean_B212','blocks[211]':'blocks[212]','block=211':'block=212'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',dict(proof=proof,no_old_English_or_native_assumptions_inherited=True,full_goal_complete=False))
