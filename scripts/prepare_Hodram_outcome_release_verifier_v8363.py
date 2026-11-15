"""Source-lock full registered manifest, complete reference equality, preserved stack and clean patch verification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_release_verifier_tools_v8363');assert not root.exists()
    d=derive('scripts/verify_Hodram_three_blocks_release_v8301.py','scripts/verify_Hodram_outcomes_release_v8363.py',{
        'hodram_three_blocks_editorial_v2':'hodram_outcomes_editorial_v2',
        'Hodram_three_blocks_release_v8301':'Hodram_outcomes_release_v8363',
        'all_routes_combined_v8300':'all_routes_combined_v8362','all_routes_combined_v8259':'all_routes_combined_v8300',
        'Hodram_three_blocks_registration_v8299':'Hodram_outcomes_registration_v8361','Hodram_atomic_positive_v8297b':'Hodram_outcome_atomic_positive_v8359e',
        'Hodram_three_blocks_build_v8300':'Hodram_outcomes_build_v8362','Hodram_three_blocks_regressions_v8300':'Hodram_outcomes_regressions_v8362',
        'all-routes-unified-v8300':'all-routes-unified-v8362','all-routes-unified-v8259':'all-routes-unified-v8300',
        "len(proof['changed_records'])==28":"len(proof['changed_records'])==6",
        'hodram_three_blocks_editorial':'hodram_outcomes_editorial',
        '==[45,46,137]':'==[47,48]',
        "profile_config.get('gerhard_surname_editorial')":"profile_config.get('hodram_three_blocks_editorial')",
        '641':'642','Hodram28 aftercompleteV8259':'Hodram6 aftercompleteV8300','registered V8300':'registered V8362',
        'only_SC1_B45_B46_B137_change_322_otherblocks_andall_other_files_components_exact':'only_SC1_B47_B48_change_323_otherblocks_andall_other_files_components_exact',
    })
    root.mkdir(parents=True);save(root/'registered_release_verifier_source_derivation.json',dict(derivation=d,all_native_high_integer_constants_andmultiplicity_preserved=True,full_prior_stack_andexact_clean_patch_checks_retained=True,no_build_patch_orcredit_created_bythis_preparer=True,new_credit=0,full_goal_complete=False))
