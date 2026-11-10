"""Preserve a source-locked next-block inventory; do not consult old English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_clean_tools_v6446')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/inventory_lil_B208_clean_v6387.py','scripts/inventory_lil_B209_clean_v6446.py',{'B208':'B209','clean_inventory_v6387':'clean_inventory_v6446','blocks[208]':'blocks[209]','block=208':'block=209'})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',receipt)
