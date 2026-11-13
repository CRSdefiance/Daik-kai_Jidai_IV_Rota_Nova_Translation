"""Prepare the next whole clean Japanese block before consulting predecessor English."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    print(derive('scripts/inventory_lil_B194_clean_v5487.py','scripts/inventory_lil_B195_clean_v5539.py',{
        'B194':'B195','clean_inventory_v5487':'clean_inventory_v5539','blocks[194]':'blocks[195]','block=194':'block=195'}))
