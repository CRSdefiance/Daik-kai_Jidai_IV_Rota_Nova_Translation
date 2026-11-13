"""Prepare current V7371 own-capture startup comparisons and strict native binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_startup_tools_v7374')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/run_lil_B227_startup_v7327.py','scripts/run_lil_B228_startup_v7374.py',{'B227':'B228','v7327':'v7374','version=7324':'version=7371'}),('scripts/verify_lil_B227_startup_v7328.py','scripts/verify_lil_B228_startup_v7375.py',{'work/analysis/lil_B226_runs_v7280':'work/analysis/lil_B227_runs_v7327','B227':'B228','v7328':'v7375','v7327':'v7374','v7324':'v7371','v7277':'v7324','V7277':'V7324','Current7324':'Current7371'}),('scripts/record_lil_B227_startup_view_v7328.py','scripts/record_lil_B228_startup_view_v7375.py',{'B227':'B228','v7328':'v7375','V7277':'V7324'}),('scripts/bind_current_V7324_native_v7329.py','scripts/bind_current_V7371_native_v7376.py',{'V7324':'V7371','B227':'B228','v7329':'v7376','v7325':'v7372','v7327':'v7374'})]
    for a,b,c in jobs:assert not Path(b).exists()
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows,no_historical_RAM_overlay_orrelaxed_native_guards=True,new_credit=0,full_goal_complete=False))
