"""Reuse the exact ordinary Lil startup schedule on the own current registered ROM."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retrospective_Lil_context_tools_v7836');assert not root.exists()
    result=derive('scripts/run_Maria_B36_startup_v7823.py','scripts/run_retrospective_Lil_context_v7836.py',{
        'Own registered four New Games andpreserved Copenhagen town control; exact prior inputs.':'Own current Lil context for a retrospective wrap test; exact prior ordinary inputs.',
        "work/analysis/maria_B36_startup_runs_v7823":"work/analysis/retrospective_Lil_context_runs_v7836",
        "choices=['route3']":"choices=['route2']",
        "Maria_B36_V7821_{case}_v7823":"Lil_wrap_V7821_{case}_v7836",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        only_route2_ordinary_inputs_no_battery_unlock_observer_orforcing=True,
        original_native_high_constants_andrun_guards_preserved=True,new_credit=0,full_goal_complete=False))
