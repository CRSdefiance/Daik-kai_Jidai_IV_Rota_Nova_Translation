"""Prepare fresh current-ROM startup comparisons against V7277 actual captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B227_startup_tools_v7327')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/run_lil_B226_startup_v7280.py','scripts/run_lil_B227_startup_v7327.py',{'B226':'B227','v7280':'v7327','version=7277':'version=7324'}),derive('scripts/verify_lil_B226_startup_v7281.py','scripts/verify_lil_B227_startup_v7328.py',{'work/analysis/lil_B225_runs_v7233':'work/analysis/lil_B226_runs_v7280','B226':'B227','v7281':'v7328','v7280':'v7327','v7277':'v7324','v7230':'v7277','V7230':'V7277','Current7277':'Current7324'}),derive('scripts/record_lil_B226_startup_view_v7281.py','scripts/record_lil_B227_startup_view_v7328.py',{'B226':'B227','v7281':'v7328','V7230':'V7277'}),derive('scripts/bind_current_V7277_native_v7282.py','scripts/bind_current_V7324_native_v7329.py',{'V7277':'V7324','B226':'B227','v7282':'v7329','v7278':'v7325','v7280':'v7327'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows))
