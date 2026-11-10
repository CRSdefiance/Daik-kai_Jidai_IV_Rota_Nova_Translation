"""Derive fresh registered startup checks against V7230 actual control captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_startup_tools_v7280')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/run_lil_B225_startup_v7233.py','scripts/run_lil_B226_startup_v7280.py',{'B225':'B226','v7233':'v7280','version=7230':'version=7277'}),
        derive('scripts/verify_lil_B225_startup_v7234.py','scripts/verify_lil_B226_startup_v7281.py',{'work/analysis/lil_B224_runs_v7171':'work/analysis/lil_B225_runs_v7233','B225':'B226','v7234':'v7281','v7233':'v7280','v7230':'v7277','v7168':'v7230','V7168':'V7230','Current7230':'Current7277'}),
        derive('scripts/record_lil_B225_startup_view_v7234.py','scripts/record_lil_B226_startup_view_v7281.py',{'B225':'B226','v7234':'v7281','V7168':'V7230'}),
        derive('scripts/bind_current_V7230_native_v7235.py','scripts/bind_current_V7277_native_v7282.py',{'V7230':'V7277','B225':'B226','v7235':'v7282','v7231':'v7278','v7233':'v7280'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_startup_tools.json',dict(derivations=rows))
