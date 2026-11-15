"""Preserve the first validator and correct only a case-sensitive negative-input anchor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B221_policy_case_tools_v6993b')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/validate_lil_B221_policy_v6993.py','scripts/validate_lil_B221_policy_v6993b.py',{
        'policy_validation_v6993':'policy_validation_v6993b',
        "27,'a chivalrous army','chivalrous knights'":"27,'A chivalrous army','Chivalrous knights'"})
    ROOT.mkdir(parents=True)
    save(ROOT/'preserved_first_negative_anchor_and_exact_case_successor.json',dict(derivation=row,
        original_validator_preserved=True,failure='The authored sentence begins with capital A; the lowercase negative-test anchor did not match.',
        only_test_anchor_case_corrected_no_wording_profile_or_native_rule_change=True,
        no_ROM_mutation_or_new_credit=True,full_goal_complete=False))
