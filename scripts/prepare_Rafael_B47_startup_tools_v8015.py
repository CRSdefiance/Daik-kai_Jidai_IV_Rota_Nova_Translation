"""Prepare source-locked ordinary own-current Rafael startup and strict-context successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_startup_tools_v8015')
if __name__=='__main__':
    assert not ROOT.exists()
    results=[derive('scripts/capture_Rafael_B46_context_v7966.py','scripts/capture_Rafael_B47_context_v8015.py',{
        'B46':'B47','v7966':'v8015','v7965':'v8014','v7964':'v8013','V7964':'V8013',
    })]
    results.append(derive('scripts/bind_Rafael_B46_context_v7967.py','scripts/bind_Rafael_B47_context_v8016.py',{
        'work/analysis/Rafael_B45_context_runs_v7913/route0':'work/analysis/Rafael_B46_context_runs_v7966/route0',
        'B46':'B47','v7967':'v8016','v7966':'v8015','V7964':'V8013','==[46]':'==[47]',
    }))
    results.append(derive('scripts/record_Rafael_B46_startup_view_v7968.py','scripts/record_Rafael_B47_startup_view_v8017.py',{
        'B46':'B47','v7968':'v8017','v7967':'v8016','V7964':'V8013','V7911':'V7964',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derivations=results,
        no_new_emulator_run_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('B47 own-current startup4001-frame capture,strict binder andview recorder prepared;run capture only after registered release verification.')
