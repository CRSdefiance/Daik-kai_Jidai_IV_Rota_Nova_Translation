"""Bind retained V6439 native input without replay or historical overlays."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/current_V6439_native_tools_v6449')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/bind_current_V6380_native_v6389.py','scripts/bind_current_V6439_native_v6449.py',{
        'current_V6380_native_v6389':'current_V6439_native_v6449','V6380':'V6439',
        'verification_v6386':'verification_v6445','lil_B207_release_v6381':'lil_B208_release_v6440','lil_B207_runs_v6383':'lil_B208_runs_v6442',
        'current_V6327_native_v6337':'current_V6380_native_v6389','B208':'B209',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',r)
