"""Derive B177's source-bound profiles and fresh native checks without the B176 flavor exception."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B177_layout_preparation_v4613')
assert not root.exists()
tool=derive('scripts/prepare_lil_B176_layout_v4559.py','scripts/prepare_lil_B177_layout_v4613.py',{
    'B176':'B177','lil_B176':'lil_B177','layout_tools_v4559':'layout_tools_v4613',
    'Seville banana-fashion':'Genoa tomato-fashion','C200384,end386':'C200480,end482',
    'lil_B176_layout_v4560':'lil_B177_layout_v4614',
    'plan_lil_B176_layout_v4560':'plan_lil_B177_layout_v4614',
    'lil_B176_fonts_v4561':'lil_B177_fonts_v4615',
    'verify_lil_B176_fonts_v4561':'verify_lil_B177_fonts_v4615',
    "'blocks[175]':'blocks[176]','blocks[174]':'blocks[175]'":
        "'blocks[175]':'blocks[177]','blocks[174]':'blocks[176]'",
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,no_B176_flavor_complete_clause_extension_inherited=True,
    shared_native_metrics_and_guards_unchanged=True,no_ROM_orledger_credit=True,full_goal_complete=False))
