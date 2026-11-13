"""Source-lock the sole registered B50 build and unchanged repository regression runner."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_build_tools_v8543');assert not root.exists()
    tools=[derive('scripts/build_Hodram_B49_v8459.py','scripts/build_Hodram_B50_v8543.py',{
        'Hodram_B49_build_v8459':'Hodram_B50_build_v8543',
        'all_routes_combined_v8459_candidate':'all_routes_combined_v8543_candidate',
        'Hodram_B49_registration_v8458':'Hodram_B50_registration_v8542',
        'all-routes-unified-v8459':'all-routes-unified-v8543',
    }),derive('scripts/run_Hodram_B49_regressions_v8459.py','scripts/run_Hodram_B50_regressions_v8543.py',{
        'Hodram_B49_regressions_v8459':'Hodram_B50_regressions_v8543',
    })]
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,sole_registered_builder_andall_eight_regression_modules_unchanged=True,all_prior_ROMs_translations_manifests_andfailures_preserved=True,no_promotion_pruning_orcredit=True,new_credit=0,full_goal_complete=False))
