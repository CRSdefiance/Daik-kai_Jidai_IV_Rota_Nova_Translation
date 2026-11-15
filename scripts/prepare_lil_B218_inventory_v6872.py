"""Prepare the next clean-only source inventory without exposing predecessor English."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/inventory_lil_B217_clean_v6828.py','scripts/inventory_lil_B218_clean_v6872.py',{'B217':'B218','v6828':'v6872','blocks[217]':'blocks[218]','block=217':'block=218'}))
