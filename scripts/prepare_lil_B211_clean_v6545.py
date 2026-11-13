"""Preserve the next complete clean source before consulting any predecessor English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_clean_tools_v6545')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/inventory_lil_B210_clean_v6495.py','scripts/inventory_lil_B211_clean_v6545.py',{'lil_B210_clean_inventory_v6495':'lil_B211_clean_inventory_v6545','all_clean_B210':'all_clean_B211','blocks[210]':'blocks[211]','block=210':'block=211'});ROOT.mkdir(parents=True);save(ROOT/'clean_inventory_derivation.json',proof)
