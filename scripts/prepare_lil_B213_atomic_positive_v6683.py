"""Prepare exact B213 cumulative reconstruction using the verified one-write validation procedure."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_atomic_tools_v6683')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/validate_lil_B212_atomic_v6638b.py','scripts/validate_lil_B213_atomic_v6683.py',{'B212':'B213','lil_B212_editorial_v2':'lil_B213_editorial_v1','seal_lil_B212_references_v6637':'seal_lil_B213_references_v6682','atomic_v6638b':'atomic_v6683','editorial_manuscript_v5':'editorial_manuscript_v4','reference_approval_v6637':'reference_approval_v6682',"len(proof['changed_records'])==14":"len(proof['changed_records'])==18",'positive_records=14':'positive_records=18','source884_bytes_inverse_recovered':'source1028_bytes_inverse_recovered','14 objects, one archive write, complete884-byte inverse':'18 objects, one archive write, complete1028-byte inverse'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_atomic_positive_runner.json',dict(proof=proof,no_prior_native_guard_or_address_changed=True,full_goal_complete=False))
