"""Prepare retained V6488 opening binding through the unchanged strict native helper."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/current_V6488_native_tools_v6497')
if __name__=='__main__':
    assert not ROOT.exists();r=derive('scripts/bind_current_V6439_native_v6449.py','scripts/bind_current_V6488_native_v6497.py',{'current_V6439_native_v6449':'current_V6488_native_v6497','V6439':'V6488','verification_v6445':'verification_v6494','lil_B208_release_v6440':'lil_B209_release_v6489','lil_B208_runs_v6442':'lil_B209_runs_v6491','current_V6380_native_v6389':'current_V6439_native_v6449','B209':'B210'});ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',r);print('V6488 retained-opening native binding prepared;requires verified6494 handoff,no replay or weakened guard.')
