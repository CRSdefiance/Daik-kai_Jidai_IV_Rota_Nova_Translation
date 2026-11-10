"""Prepare a clean-only next-scene inventory without assuming its dialogue structure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_clean_tools_v7127')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/inventory_lil_B223_clean_v7074.py';b='scripts/inventory_lil_B224_clean_v7127.py'
    c={'B223':'B224','v7074':'v7127','blocks[223]':'blocks[224]','block=223':'block=224'}
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_inventory.json',dict(tool=row,only_clean_Japanese_ROM_read=True,no_prior_English_or_current_ROM_consulted=True,no_assumption_about_speech_style_or_command_counts=True,new_credit=0,full_goal_complete=False))
