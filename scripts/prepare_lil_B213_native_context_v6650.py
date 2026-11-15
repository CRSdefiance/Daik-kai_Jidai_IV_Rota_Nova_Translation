"""Bind V6641 to its own verified capture; no additional boot or historical RAM overlay."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_context_tools_v6650')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/bind_current_V6584_native_v6593.py','scripts/bind_current_V6641_native_v6650.py',{'V6584':'V6641','native_v6593':'native_v6650','verification_v6590':'verification_v6647','lil_B211_release_v6585':'lil_B212_release_v6642','lil_B211_runs_v6587':'lil_B212_runs_v6644','current_V6541_native_v6549':'current_V6584_native_v6593','B212':'B213'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_binding.json',proof)
