"""Prepare fresh own-registered B50 candidate startup andstrict captain0 context binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_startup_tools_v8174')
if __name__=='__main__':
    assert not ROOT.exists()
    capture=derive('scripts/capture_Rafael_B49_context_v8124.py','scripts/capture_Rafael_B50_context_v8174.py',{
        'Rafael_B49_context_runs_v8124':'Rafael_B50_context_runs_v8174','Rafael_B49_release_v8123':'Rafael_B50_release_v8173',
        'all-routes-unified-v8122':'all-routes-unified-v8172',
        'Rafael_B49_route{route}_v8124_V8122':'Rafael_B50_route{route}_v8174_V8172','B49':'B50',
    })
    bind=derive('scripts/bind_Rafael_B49_context_v8125.py','scripts/bind_Rafael_B50_context_v8175.py',{
        'Rafael_B49_context_binding_v8125':'Rafael_B50_context_binding_v8175',
        'Rafael_B49_context_runs_v8124':'Rafael_B50_context_runs_v8174','Rafael_B48_context_runs_v8068':'Rafael_B49_context_runs_v8124',
        'current_V8122_Rafael_native_v8125':'current_V8172_Rafael_native_v8175',
        '==[49]':'==[50]','V8122':'V8172','B49':'B50',
    })
    view=derive('scripts/record_Rafael_B49_startup_view_v8126.py','scripts/record_Rafael_B50_startup_view_v8176.py',{
        'Rafael_B49_startup_view_v8126':'Rafael_B50_startup_view_v8176','Rafael_B49_context_binding_v8125':'Rafael_B50_context_binding_v8175',
        'match V8066':'match V8122','own-V8122':'own-V8172','B49':'B50',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[capture,bind,view])
    print('Prepared own V8172 startup andstrict context tools;do not execute before registered release passes.')
