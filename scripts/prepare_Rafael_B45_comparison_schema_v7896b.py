"""Use the actual audited last complete hold; preserve the failed legacy-schema comparison."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_comparison_schema_v7896b');assert not root.exists()
    result=derive('scripts/measure_Rafael_B45_pairs_v7896.py','scripts/measure_Rafael_B45_pairs_v7896b.py',{
        'work/analysis/Rafael_B45_actual_comparison_v7896':'work/analysis/Rafael_B45_actual_comparison_v7896b',
        "ha,hb=a['selected_capture'],b['selected_capture']":"ha,hb=a['complete_body_holds'][-1],b['complete_body_holds'][-1]",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        failure='KeyError selected_capture before comparison outputs;B45 auditor stores the full complete_body_holds list',
        uses_exact_last_audited_complete_hold_not_unverified_frame=True,
        all_native_state_RGB_timing_andinput_guards_preserved=True,no_new_emulator_runs=True,new_credit=0,full_goal_complete=False))
