"""Correct the remaining two-actor row-count guard and preserve its failed run."""
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/prove_lil_B178_names_v4667.py','scripts/prove_lil_B178_names_v4667b.py',{
    'lil_B178_names_v4667':'lil_B178_names_v4667b',
    'Bind Owner/Cook full and progressive':'Bind three Lady full and progressive',
    "len(native['rows'])==4":"len(native['rows'])==6",
    'readonly_paths=4':'readonly_paths=6',
})
print('Prepared six-row name verification successor;failed adapter/context retained,no emulator run.')
