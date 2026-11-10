"""Prepare the next complete clean Japanese exchange while B187 captures run."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B188_clean_preparation_v5230')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/inventory_lil_B187_clean_v5186.py','scripts/inventory_lil_B188_clean_v5230.py',{
        'B187':'B188','clean_inventory_v5186':'clean_inventory_v5230','blocks[187]':'blocks[188]','block=187':'block=188',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_clean_only_inventory.json',dict(derivation=row,
        no_predecessor_English_or_current_dialogue_read=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared next clean-only full exchange without old dialogue comparison or credit.')
