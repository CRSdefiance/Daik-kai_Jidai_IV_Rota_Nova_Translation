"""Start the next whole-exchange review with only clean Japanese exposed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_clean_tools_v6693')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/inventory_lil_B213_clean_v6648.py','scripts/inventory_lil_B214_clean_v6693.py',{'B213':'B214','blocks[213]':'blocks[214]','block=213':'block=214','inventory_v6648':'inventory_v6693'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_inventory.json',proof)
