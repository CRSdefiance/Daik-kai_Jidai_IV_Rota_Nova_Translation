"""Prepare own-current cold boots and strict native binding after registered release."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_startup_tools_v7517')
if __name__=='__main__':
    assert not ROOT.exists();jobs=[('scripts/run_lil_B230_startup_v7469.py','scripts/run_lil_B231_startup_v7517.py',{'B230':'B231','v7469':'v7517','version=7466':'version=7514'}),('scripts/verify_lil_B230_startup_v7470.py','scripts/verify_lil_B231_startup_v7518.py',{'work/analysis/lil_B229_runs_v7421':'work/analysis/lil_B230_runs_v7469','B230':'B231','v7470':'v7518','v7469':'v7517','v7466':'v7514','v7418':'v7466','V7418':'V7466','Current7466':'Current7514'}),('scripts/record_lil_B230_startup_view_v7470.py','scripts/record_lil_B231_startup_view_v7518.py',{'B230':'B231','v7470':'v7518','V7418':'V7466'}),('scripts/bind_current_V7466_native_v7471.py','scripts/bind_current_V7514_native_v7519.py',{'V7466':'V7514','B230':'B231','v7471':'v7519','v7467':'v7515','v7469':'v7517'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows,own_registered_ROM_snapshots_only_no_overlay_orrelaxed_guard=True,prior_V7466_captures_only_comparison_controls=True,no_separate_test_package=True,new_credit=0,full_goal_complete=False))
