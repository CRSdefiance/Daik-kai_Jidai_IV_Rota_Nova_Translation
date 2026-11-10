"""Run the same complete positive/challenge suite against the corrected v2 compiler."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_atomic_successor_tools_v7908');assert not root.exists()
    results=[]
    results.append(derive('scripts/validate_Rafael_B45_atomic_positive_v7905.py','scripts/validate_Rafael_B45_atomic_positive_v7908.py',{
        'rafael_B45_editorial_v1 as owned':'rafael_B45_editorial_v2 as owned',
        'work/analysis/Rafael_B45_atomic_positive_v7905':'work/analysis/Rafael_B45_atomic_positive_v7908',
    }))
    results.append(derive('scripts/challenge_Rafael_B45_atomic_v7906.py','scripts/challenge_Rafael_B45_atomic_v7909.py',{
        'rafael_B45_editorial_v1 as owned':'rafael_B45_editorial_v2 as owned',
        'work/analysis/Rafael_B45_atomic_challenges_v7906':'work/analysis/Rafael_B45_atomic_challenges_v7909',
        'work/analysis/Rafael_B45_atomic_positive_v7905/positive_receipt.json':'work/analysis/Rafael_B45_atomic_positive_v7908/positive_receipt.json',
    }))
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=results,
        all131_original_real_mutations_andno_schema_orcommit_attempt_false_positives_preserved=True,
        no_v1_failures_deleted_orcounted_aspassing=True,new_credit=0,full_goal_complete=False))
