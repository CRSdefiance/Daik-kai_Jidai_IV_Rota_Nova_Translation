"""Source-lock registered cumulative build and regression runners for the six outcomes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_registered_tools_v8361');assert not root.exists();results=[]
    results.append(derive('scripts/build_Hodram_three_blocks_v8300.py','scripts/build_Hodram_outcomes_v8362.py',{'Hodram_three_blocks_build_v8300':'Hodram_outcomes_build_v8362','all_routes_combined_v8300':'all_routes_combined_v8362','Hodram_three_blocks_registration_v8299':'Hodram_outcomes_registration_v8361','all-routes-unified-v8300':'all-routes-unified-v8362'}))
    results.append(derive('scripts/run_Hodram_three_blocks_regressions_v8300.py','scripts/run_Hodram_outcomes_regressions_v8362.py',{'Hodram_three_blocks_regressions_v8300':'Hodram_outcomes_regressions_v8362'}))
    root.mkdir(parents=True);save(root/'registered_runners_exact_source_derivations.json',dict(derivations=results,no_builder_registry_ROM_orcredit_change_bythis_preparer=True,new_credit=0,full_goal_complete=False))
