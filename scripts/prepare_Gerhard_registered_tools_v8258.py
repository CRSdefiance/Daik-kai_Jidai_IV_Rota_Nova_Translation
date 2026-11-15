"""Source-lock the existing sole-builder and regression runners to the registered surname profile."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_registered_tools_v8258')
if __name__=='__main__':
    assert not ROOT.exists();receipts=[]
    receipts.append(derive('scripts/build_Rafael_B50_v8172.py','scripts/build_Gerhard_surname_v8259.py',{
        'Rafael_B50_build_v8172':'Gerhard_surname_build_v8259','all_routes_combined_v8172':'all_routes_combined_v8259',
        'Rafael_B50_registration_v8171':'Gerhard_surname_registration_v8258','all-routes-unified-v8172':'all-routes-unified-v8259',
    }))
    receipts.append(derive('scripts/run_Rafael_B50_regressions_v8172.py','scripts/run_Gerhard_surname_regressions_v8259.py',{'Rafael_B50_regressions_v8172':'Gerhard_surname_regressions_v8259'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_runners.json',dict(derivations=receipts,new_credit=0,full_goal_complete=False))
