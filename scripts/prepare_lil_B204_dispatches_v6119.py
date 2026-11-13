"""Prepare a strict current-runtime successor without changing native addresses."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_dispatch_tools_v6119')
if __name__=='__main__':
    assert not ROOT.exists()
    d=derive('scripts/prove_lil_B204_dispatches_v6066.py','scripts/prove_lil_B204_dispatches_v6119.py',{
        'scripts.current_build_native_context_v4774':'scripts.current_build_native_context_v6097',
        'lil_B204_dispatches_v6066':'lil_B204_dispatches_v6119',
        'work/analysis/lil_B204_source_v6062/all20_clean_current_complete_context.json':'work/analysis/lil_B204_current_v6118/all20_clean_current_complete_context.json',
        'work/analysis/lil_B204_voices_v6063/current_native_input.json':'work/analysis/lil_B204_current_v6118/current_native_input.json',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(tool=d,all_native_integer_addresses_and_dispatch_code_unchanged=True,full_goal_complete=False));print('Current B204 dispatch successor prepared;old producer preserved.')
