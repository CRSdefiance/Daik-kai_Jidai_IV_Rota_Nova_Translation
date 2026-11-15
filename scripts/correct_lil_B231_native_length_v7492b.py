"""Correct a metadata-only word-count typo before freezing the layout contract."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_native_length_tools_v7492b')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/record_lil_B231_native_review_v7492.py','scripts/record_lil_B231_native_review_v7492b.py',{'native_review_v7492':'native_review_v7492b','editorial_manuscript_v2.json':'editorial_manuscript_v2b.json','full76-character sentence':'full78-character sentence'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_metadata_length_correction.json',dict(tool=row,R12_measured35_28_13_rows_plus_two_spaces_equal78_not76=True,original_metadata_producer_andoutput_preserved=True,no_prose_compiled_native_input_runtime_QA_orcredit_change=True,new_credit=0,full_goal_complete=False))
