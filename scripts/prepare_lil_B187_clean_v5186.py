"""Prepare only the next complete clean Japanese block while release checks run."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_clean_preparation_v5186')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/inventory_lil_B186_clean_v5130.py','scripts/inventory_lil_B187_clean_v5186.py',{
        'B186':'B187','clean_inventory_v5130':'clean_inventory_v5186','blocks[186]':'blocks[187]','block=186':'block=187',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_clean_only_inventory.json',dict(derivation=row,
        no_predecessor_English_or_current_dialogue_read=True,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared next full clean-only block without exposing old dialogue or adding credit.')
