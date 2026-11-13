"""Inventory only the next clean Japanese exchange while the cumulative build runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_clean_tools_v7176')
if __name__=='__main__':
    assert not ROOT.exists();target='scripts/inventory_lil_B225_clean_v7176.py';assert not Path(target).exists()
    row=derive('scripts/inventory_lil_B224_clean_v7127.py',target,{'B224':'B225','v7127':'v7176','blocks[224]':'blocks[225]','block=224':'block=225'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',dict(tool=row,clean_Japanese_only_no_predecessor_ROM_read=True,no_review_credit=True))
