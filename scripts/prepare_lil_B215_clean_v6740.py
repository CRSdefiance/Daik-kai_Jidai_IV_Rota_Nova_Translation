"""Begin the next complete exchange with clean Japanese only, preserving all typed commands."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B215_clean_tools_v6740')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/inventory_lil_B214_clean_v6693.py','scripts/inventory_lil_B215_clean_v6740.py',{'B214':'B215','blocks[214]':'blocks[215]','block=214':'block=215','inventory_v6693':'inventory_v6740'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',proof)
