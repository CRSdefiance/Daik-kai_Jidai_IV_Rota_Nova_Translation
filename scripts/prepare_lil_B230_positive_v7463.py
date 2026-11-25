"""Close immutable B230 evidence and verify exact one-write reconstruction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_positive_tools_v7463')
if __name__=='__main__':
    assert not ROOT.exists();changes={'B229':'B230','final_paths_v7409':'final_paths_v7457','atomic_v7415':'atomic_v7463','v7414':'v7462','seal_lil_B229_references_v7411':'seal_lil_B230_references_v7459','source_locked_staged_item_callback_scope':'source_locked_static_item_country_scope','source944_bytes_inverse_with_no_source_or_target_tail_recovered':'source988_bytes_inverse_source_tail0_target_tail2_recovered','complete944-byte':'complete988-byte'}
    row=derive('scripts/validate_lil_B229_atomic_v7415.py','scripts/validate_lil_B230_atomic_v7463.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_validator.json',dict(tool=row,static_item52_andcountry_term_scope_andall_measurements_closed=True,source988_tail0_target980_logical978_tail2_full_inverse_required=True,new_credit=0,full_goal_complete=False))
