"""Prepare fresh V7418 own-ROM startup comparisons and strict native-input binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_startup_tools_v7421')
if __name__=='__main__':
    assert not ROOT.exists()
    jobs=[('scripts/run_lil_B228_startup_v7374.py','scripts/run_lil_B229_startup_v7421.py',{'B228':'B229','v7374':'v7421','version=7371':'version=7418'}),('scripts/verify_lil_B228_startup_v7375.py','scripts/verify_lil_B229_startup_v7422.py',{'work/analysis/lil_B227_runs_v7327':'work/analysis/lil_B228_runs_v7374','B228':'B229','v7375':'v7422','v7374':'v7421','v7371':'v7418','v7324':'v7371','V7324':'V7371','Current7371':'Current7418'}),('scripts/record_lil_B228_startup_view_v7375.py','scripts/record_lil_B229_startup_view_v7422.py',{'B228':'B229','v7375':'v7422','V7324':'V7371'}),('scripts/bind_current_V7371_native_v7376.py','scripts/bind_current_V7418_native_v7423.py',{'V7371':'V7418','B228':'B229','v7376':'v7423','v7372':'v7419','v7374':'v7421'})]
    for a,b,c in jobs:assert not Path(b).exists()
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows,new_current_capture_required_no_historical_RAM_overlay_orrelaxed_guard=True,new_credit=0,full_goal_complete=False))
