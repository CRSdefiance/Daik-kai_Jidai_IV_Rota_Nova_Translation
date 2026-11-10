"""Reuse exact native skip guards for all B212 two/three-choice alternatives."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_branch_tools_v6596')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B167_branches_v4122.py','scripts/prove_lil_B212_branches_v6596.py',{'lil_B167_branches_v4122':'lil_B212_branches_v6596','lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice.json':'lil_B212_source_v6594b/all14_clean_current_complete_exchange_with_two_three_choices.json'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_branch_producer.json',dict(proof=proof,source_current_0100_0200_0300_0400_each_tested_results0_1_2_3_unmatched=True,no_gameplay_choice_result_or_effect_claim=True,full_goal_complete=False))
