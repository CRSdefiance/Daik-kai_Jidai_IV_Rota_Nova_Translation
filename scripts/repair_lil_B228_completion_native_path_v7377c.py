"""Bind completion to V7371's own native input; preserve the unexecuted copied-path version."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B228_completion_repair_v7377c')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B228_completion_v7377').exists()
    rows=[derive('scripts/lil_B228_completion_gates_v7377.py','scripts/lil_B228_completion_gates_v7377b.py',{'current_V7324_native_v7376':'current_V7371_native_v7376'}),derive('scripts/complete_lil_B228_v7377.py','scripts/complete_lil_B228_v7377b.py',{'lil_B228_completion_gates_v7377':'lil_B228_completion_gates_v7377b'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_own_current_native_path.json',dict(derivations=rows,inspection_caught_old_version_in_copied_native_binding_path_before_completion_execution=True,own_V7371_snapshot_required_no_historical_RAM_overlay=True,no_ledger_orcredit_mutation=True,full_goal_complete=False))
