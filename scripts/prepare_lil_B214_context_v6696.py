"""Bind the exact current cumulative ROM to its own verified opening capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_context_tools_v6696')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/bind_current_V6641_native_v6650.py','scripts/bind_current_V6686_native_v6696.py',{'V6641':'V6686','native_v6650':'native_v6696','verification_v6647':'verification_v6692','lil_B212_release_v6642':'lil_B213_release_v6687','lil_B212_runs_v6644':'lil_B213_runs_v6689','current_V6584_native_v6593':'current_V6641_native_v6650','B213':'B214'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_binding.json',proof)
