"""Inventory the next complete clean block while the independent cumulative builder runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B216_clean_tools_v6782')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/inventory_lil_B215_clean_v6740.py';b='scripts/inventory_lil_B216_clean_v6782.py';c={'B215':'B216','v6740':'v6782','blocks[215]':'blocks[216]','block=215':'block=216'};assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);proof=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',proof)
