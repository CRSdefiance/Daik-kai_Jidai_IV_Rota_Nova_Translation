"""Derive sole-builder andrequired regression runners for the newly registered cumulative profile."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    derive('scripts/build_Hodram_outcomes_v8377.py','scripts/build_Hodram_B49_v8459.py',{
        'Hodram_outcomes_build_v8377':'Hodram_B49_build_v8459','all_routes_combined_v8377_candidate':'all_routes_combined_v8459_candidate','Hodram_outcomes_registration_v8376':'Hodram_B49_registration_v8458','all-routes-unified-v8377':'all-routes-unified-v8459',
    })
    derive('scripts/run_Hodram_outcomes_regressions_v8377.py','scripts/run_Hodram_B49_regressions_v8459.py',{
        'Hodram_outcomes_regressions_v8377':'Hodram_B49_regressions_v8459',
    })
