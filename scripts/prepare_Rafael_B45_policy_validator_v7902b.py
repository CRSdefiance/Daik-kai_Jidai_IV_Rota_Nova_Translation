"""Keep the failed checker and match the actual existing per-record review guard message."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_policy_validation_tools_v7902b');assert not root.exists()
    result=derive('scripts/validate_Rafael_B45_policy_v7902.py','scripts/validate_Rafael_B45_policy_v7902b.py',{
        'work/analysis/Rafael_B45_policy_validation_v7902':'work/analysis/Rafael_B45_policy_validation_v7902b',
        "'gate is not approved'":"'v2 requires per-record'",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        failure='The existing validator correctly rejected missing source review;the checker expected the wrong error-message wording',
        all_actual_input_changes_andexpected_ValueError_guards_retained=True,
        no_policy_guard_orROM_change=True,no_failed_ROM_orpassed_negative_claim=True,new_credit=0,full_goal_complete=False))
