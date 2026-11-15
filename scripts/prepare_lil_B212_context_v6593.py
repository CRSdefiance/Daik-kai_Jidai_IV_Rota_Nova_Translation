"""Bind the new cumulative release to its own already captured opening snapshot."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_context_tools_v6593')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/bind_current_V6541_native_v6549.py','scripts/bind_current_V6584_native_v6593.py',{'current_V6541_native_v6549':'current_V6584_native_v6593','verification_v6548':'verification_v6590','B210_Ferid_release_v6542':'lil_B211_release_v6585','B210_Ferid_runs_v6543':'lil_B211_runs_v6587','current_V6488_native_v6497':'current_V6541_native_v6549','V6541':'V6584','B211':'B212'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_context_binding.json',dict(proof=proof,no_native_constant_changes=True,no_new_boot=True,full_goal_complete=False))
