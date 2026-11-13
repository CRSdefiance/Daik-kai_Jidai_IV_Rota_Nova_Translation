"""Prepare the next clean-only inventory while the cumulative release runs."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/inventory_lil_B216_clean_v6782.py','scripts/inventory_lil_B217_clean_v6828.py',{'B216':'B217','v6782':'v6828','blocks[216]':'blocks[217]','block=216':'block=217'}))
