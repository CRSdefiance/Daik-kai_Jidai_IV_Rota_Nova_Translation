"""Scope unchanged original relative-skip tests to B213's independently inventoried four sites."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_branch_tools_v6654')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B212_branches_v6596.py','scripts/prove_lil_B213_branches_v6654.py',{'B212':'B213','branches_v6596':'branches_v6654','source_v6594b':'source_v6651','all14_clean_current_complete_exchange_with_two_three_choices':'eighteen_clean_current_full_prophecy_exchange_source_references'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_original_branch_tests.json',proof)
