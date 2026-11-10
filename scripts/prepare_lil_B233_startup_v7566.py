"""Prepare own-ROM cold boots and strict native binding after registered integration."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B233_startup_tools_v7566')
if __name__=='__main__':
    assert not ROOT.exists();jobs=[('scripts/run_lil_B231_startup_v7517.py','scripts/run_lil_B233_startup_v7566.py',{'B231':'B233','v7517':'v7566','version=7514':'version=7563'}),('scripts/verify_lil_B231_startup_v7518.py','scripts/verify_lil_B233_startup_v7567.py',{'work/analysis/lil_B230_runs_v7469':'work/analysis/lil_B231_runs_v7517','B231':'B233','v7518':'v7567','v7517':'v7566','v7514':'v7563','v7466':'v7514','V7466':'V7514','Current7514':'Current7563'}),('scripts/record_lil_B231_startup_view_v7518.py','scripts/record_lil_B233_startup_view_v7567.py',{'B231':'B233','v7518':'v7567','V7466':'V7514'}),('scripts/bind_current_V7514_native_v7519.py','scripts/bind_current_V7563_native_v7568.py',{'V7514':'V7563','B231':'B233','v7519':'v7568','v7515':'v7564','v7517':'v7566'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows,own_registered_ROM_snapshots_only_no_overlay_orrelaxed_native_guard=True,prior_V7514_captures_only_comparison_controls=True,no_separate_test_package=True,new_credit=0,full_goal_complete=False))
