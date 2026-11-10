"""Correct the predecessor derivation key; source-locked substitutions are simultaneous."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_loader_tools_v8222b')
if __name__=='__main__':
    assert not ROOT.exists()
    correction=derive('scripts/prepare_Gerhard_loaders_v8222.py','scripts/prepare_Gerhard_loaders_v8222c.py',{
        '''"RECEIPT=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')":''':
        '''"RECEIPT=Path('work/analysis/Rafael_B50_reference_v8151/research_image_receipt.json')":''',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_preparer_correction.json',dict(derivation=correction,
        earlier_failure_before_any_loader_producer_orROM_write=True,all_native_guard_andaddress_literals_preserved=True,new_credit=0,full_goal_complete=False))
    print('Preserved failed preparer;corrected exact original receipt key before simultaneous substitutions.')
