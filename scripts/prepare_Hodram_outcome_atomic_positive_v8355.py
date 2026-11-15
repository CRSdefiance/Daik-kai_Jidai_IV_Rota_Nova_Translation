"""Source-lock the prior one-whole-object positive test to the six mixed-consumer outcomes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_atomic_positive_tools_v8355');assert not root.exists()
    d=derive('scripts/validate_Hodram_atomic_positive_v8297b.py','scripts/validate_Hodram_outcome_atomic_positive_v8355.py',{'hodram_three_blocks_editorial_v2':'hodram_outcomes_editorial_v1','Hodram_three_blocks_release_paths_v8290':'Hodram_outcomes_release_paths_v8347','Hodram_atomic_positive_v8297b':'Hodram_outcome_atomic_positive_v8355',"len(report['changed_records'])==28":"len(report['changed_records'])==6",'28manifest IDs':'6manifest IDs'})
    root.mkdir(parents=True);save(root/'one_whole_object_positive_source_derivation.json',dict(derivation=d,new_credit=0,full_goal_complete=False))
