"""Prepare own-ROM V7466 startup evidence and strict current native input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_startup_tools_v7469')
if __name__=='__main__':
    assert not ROOT.exists();jobs=[('scripts/run_lil_B229_startup_v7421.py','scripts/run_lil_B230_startup_v7469.py',{'B229':'B230','v7421':'v7469','version=7418':'version=7466'}),('scripts/verify_lil_B229_startup_v7422.py','scripts/verify_lil_B230_startup_v7470.py',{'work/analysis/lil_B228_runs_v7374':'work/analysis/lil_B229_runs_v7421','B229':'B230','v7422':'v7470','v7421':'v7469','v7418':'v7466','v7371':'v7418','V7371':'V7418','Current7418':'Current7466'}),('scripts/record_lil_B229_startup_view_v7422.py','scripts/record_lil_B230_startup_view_v7470.py',{'B229':'B230','v7422':'v7470','V7371':'V7418'}),('scripts/bind_current_V7418_native_v7423.py','scripts/bind_current_V7466_native_v7471.py',{'V7418':'V7466','B229':'B230','v7423':'v7471','v7419':'v7467','v7421':'v7469'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows,only_own_registered_ROM_NewGame_snapshot_allowed=True,no_historical_RAM_overlay_orrelaxed_2b6_guard=True,prior_V7418_captures_reused_only_as_comparison_controls=True,new_credit=0,full_goal_complete=False))
