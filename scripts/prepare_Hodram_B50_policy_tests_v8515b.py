"""Rebind unchanged B50 semantic policy tests to the supported root-gate schema."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_policy_tools_v8515b');assert not root.exists()
    result=derive('scripts/validate_Hodram_B50_policy_v8515.py','scripts/validate_Hodram_B50_policy_v8515b.py',{
        'Hodram_B50_policy_validation_v8515':'Hodram_B50_policy_validation_v8515b',
        'hodram_B50_profile_v1':'hodram_B50_profile_v2','hodram_B50_layout_v1':'hodram_B50_layout_v2','hodram_B50_names_v1':'hodram_B50_names_v2',
        'translations/hodram_B50_editorial_manuscript_v4.json':'translations/hodram_B50_editorial_manuscript_v5.json',
        'translations/hodram_B50_native_contract_v1.json':'translations/hodram_B50_native_contract_v2.json',
        "suffix+'_v1.py'":"suffix+'_v2.py'",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_semantic_mutations_positive_checks_dependency_guards_andnative_high_constants_unchanged=True,failed_dictionary_gate_attempt_preserved=True,new_credit=0,full_goal_complete=False))
