"""Prepare fresh own-registered B49 cumulative-ROM startup capture and native-context binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_startup_tools_v8124')
if __name__=='__main__':
    assert not ROOT.exists()
    a=derive('scripts/capture_Rafael_B48_context_v8068.py','scripts/capture_Rafael_B49_context_v8124.py',{
        'Rafael_B48_context_runs_v8068':'Rafael_B49_context_runs_v8124',
        'Rafael_B48_release_v8067':'Rafael_B49_release_v8123',
        'all-routes-unified-v8066':'all-routes-unified-v8122',
        'B48':'B49','_v8068_V8066':'_v8124_V8122',
    })
    b=derive('scripts/bind_Rafael_B48_context_v8069.py','scripts/bind_Rafael_B49_context_v8125.py',{
        "PRIOR=Path('work/analysis/Rafael_B47_context_runs_v8015/route0')":"PRIOR=Path('work/analysis/Rafael_B48_context_runs_v8068/route0')",
        'Rafael_B48_context_binding_v8069':'Rafael_B49_context_binding_v8125',
        'Rafael_B48_context_runs_v8068':'Rafael_B49_context_runs_v8124',
        'current_V8066_Rafael_native_v8069':'current_V8122_Rafael_native_v8125',
        'V8066':'V8122','B48':'B49','==[48]':'==[49]',
    })
    c=derive('scripts/record_Rafael_B48_startup_view_v8070.py','scripts/record_Rafael_B49_startup_view_v8126.py',{
        'Rafael_B48_startup_view_v8070':'Rafael_B49_startup_view_v8126',
        'Rafael_B48_context_binding_v8069':'Rafael_B49_context_binding_v8125',
        'V8013':'V8066','V8066':'V8122','B48':'B49',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[a,b,c])
    print('Prepared B49 own-current startup tools; run only after registered V8122 release verification.')
