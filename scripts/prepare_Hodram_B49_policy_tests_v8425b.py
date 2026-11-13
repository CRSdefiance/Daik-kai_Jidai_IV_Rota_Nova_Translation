"""Rebind all unchanged semantic policy tests to the corrected encoder-registration successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_policy_tools_v8425b');assert not root.exists()
    result=derive('scripts/validate_Hodram_B49_policy_v8425.py','scripts/validate_Hodram_B49_policy_v8425b.py',{
        'Hodram_B49_policy_validation_v8425':'Hodram_B49_policy_validation_v8425b',
        'hodram_B49_profile_v1':'hodram_B49_profile_v2','hodram_B49_layout_v1':'hodram_B49_layout_v2',
        'hodram_B49_choices_v1':'hodram_B49_choices_v2','hodram_B49_names_v1':'hodram_B49_names_v2',
        'translations/hodram_B49_editorial_manuscript_v3.json':'translations/hodram_B49_editorial_manuscript_v4.json',
        'translations/hodram_B49_native_contract_v1.json':'translations/hodram_B49_native_contract_v2.json',
        "suffix+'_v1.py'":"suffix+'_v2.py'",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,all_semantic_mutations_positive_checks_dependency_guards_andnative_high_constants_unchanged=True,failed_descriptive_encoder_test_preserved=True,new_credit=0,full_goal_complete=False))
