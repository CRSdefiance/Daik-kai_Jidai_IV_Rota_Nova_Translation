"""Bind the full historical storage record,including its second trailing zero."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/research_shachihoko_item_name_v6079.py','scripts/research_shachihoko_item_name_v6079b.py',{
        "arm[STORAGE:STORAGE+16]==bytes.fromhex(storage['replacement_hex'])":"arm[STORAGE:STORAGE+len(bytes.fromhex(storage['replacement_hex']))]==bytes.fromhex(storage['replacement_hex'])"}))
