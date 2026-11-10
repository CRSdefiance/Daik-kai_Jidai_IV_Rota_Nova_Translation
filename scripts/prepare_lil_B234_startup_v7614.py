"""Prepare own-ROM cold boots, exact prior controls and strict native binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_startup_tools_v7614')
if __name__=='__main__':
    assert not ROOT.exists();jobs=[
      ('scripts/run_lil_B233_startup_v7566.py','scripts/run_lil_B234_startup_v7614.py',{'B233':'B234','v7566':'v7614','version=7563':'version=7611'}),
      ('scripts/verify_lil_B233_startup_v7567.py','scripts/verify_lil_B234_startup_v7615.py',{'work/analysis/lil_B231_runs_v7517':'work/analysis/lil_B233_runs_v7566','B233':'B234','v7567':'v7615','v7566':'v7614','v7563':'v7611','v7514':'v7563','V7514':'V7563','Current7563':'Current7611'}),
      ('scripts/record_lil_B233_startup_view_v7567.py','scripts/record_lil_B234_startup_view_v7615.py',{'B233':'B234','v7567':'v7615','V7514':'V7563'}),
      ('scripts/bind_current_V7563_native_v7568.py','scripts/bind_current_V7611_native_v7616.py',{'V7563':'V7611','B233':'B234','v7568':'v7616','v7564':'v7612','v7566':'v7614'}),
    ]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows,own_registered_ROM_snapshots_only_no_overlay_orrelaxed_native_guard=True,prior_V7563_captures_only_comparison_controls=True,no_separate_test_package=True,new_credit=0,full_goal_complete=False))
