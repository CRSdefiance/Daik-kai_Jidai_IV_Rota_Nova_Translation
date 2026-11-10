"""Preserve the stopped seal producer and bind B51's actual comparison schema."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B51_seal_successor_v8603');assert not root.exists()
    result=derive('scripts/seal_Hodram_B51_release_v8598.py','scripts/seal_Hodram_B51_release_v8598b.py',{
        "data['independent_comparison']['result']['later_full_RGB_pairs_recomputed']":"data['independent_comparison']['summary']['later_full_RGB_pairs_recomputed']"})
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,prior_failure='KeyError: result; B51 comparison uses summary',prior_seal_andconfiguration_not_written=True,all_assertions_native_numbers_andgates_preserved=True,new_credit=0,full_goal_complete=False))
