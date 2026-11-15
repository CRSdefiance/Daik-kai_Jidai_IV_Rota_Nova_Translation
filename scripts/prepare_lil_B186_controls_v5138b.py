"""Correct producer-only derivation keys; retain the stopped v5138 diagnostic."""
from pathlib import Path
import py_compile
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_control_preparation_v5138b')

if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/prepare_lil_B186_controls_v5138.py','scripts/prepare_lil_B186_controls_v5138c.py',{
        'control_preparation_v5138\'':'control_preparation_v5138c\'',
        "        'block=182':'block=186',\n":'',
        "        **shared,\n        'two predicates":"        **shared,'block=182':'block=186',\n        'two predicates",
        "r['target']":"r['successor']",
    })
    py_compile.compile(row['successor'],doraise=True)
    ROOT.mkdir(parents=True)
    save(ROOT/'corrected_preparation_keys.json',dict(derivation=row,prior_failure='Source-locked derivation rejected block=182 because that key was absent in the predicate producer. No downstream producer was written.',previous_producer_preserved=True,new_review_credit=0,full_goal_complete=False))
    print('Prepared v5138c with producer-specific keys and correct successor receipts.')
