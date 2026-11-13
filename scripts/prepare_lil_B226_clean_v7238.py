"""Preserve the next clean source packet without exposing predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_clean_tools_v7238')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/inventory_lil_B225_clean_v7176.py','scripts/inventory_lil_B226_clean_v7238.py',{'B225':'B226','v7176':'v7238','blocks[225]':'blocks[226]','block=225':'block=226'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_inventory.json',r)
