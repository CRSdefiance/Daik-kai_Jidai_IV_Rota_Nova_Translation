"""Continue with a fresh clean-only inventory, without inherited B212 shapes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_clean_tools_v6648')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/inventory_lil_B212_clean_v6591.py','scripts/inventory_lil_B213_clean_v6648.py',{'B212':'B213','blocks[212]':'blocks[213]','block=212':'block=213','inventory_v6591':'inventory_v6648'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_inventory.json',proof)
