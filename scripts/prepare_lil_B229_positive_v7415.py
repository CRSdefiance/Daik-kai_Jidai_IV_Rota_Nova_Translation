"""Prepare immutable evidence closure and exact one-write reconstruction against V7371."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_positive_tools_v7415')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/validate_lil_B229_atomic_v7415.py').exists()
    changes={'B228':'B229','final_paths_v7362':'final_paths_v7409','atomic_v7368':'atomic_v7415','seal_lil_B228_references_v7364':'seal_lil_B229_references_v7411','atomic_tools_v7367':'atomic_tools_v7414','prepare_lil_B228_atomic_v7367':'prepare_lil_B229_atomic_v7414',"len(proof['changed_records'])==13":"len(proof['changed_records'])==17",'positive_records=13':'positive_records=17','source760_bytes_inverse_including_tail2_recovered':'source944_bytes_inverse_with_no_source_or_target_tail_recovered','all13_actual13_pages51_body51_headers_bound':'all17_actual17_pages67_body67_headers_bound','13 speeches/13 pages,complete760-byte':'17 speeches/17 pages,complete944-byte',"Path('dk4tool/patch/lil_B228_atomic_support_v1.py')":"Path('dk4tool/patch/lil_B229_atomic_support_v1.py'),Path('work/analysis/lil_B229_atomic_support_tools_v7414/source_locked_staged_item_callback_scope.json'),Path('scripts/prepare_lil_B229_atomic_support_v7414.py')"}
    r=derive('scripts/validate_lil_B228_atomic_v7368.py','scripts/validate_lil_B229_atomic_v7415.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_validator.json',dict(tool=r,staged_item53_callback_prerequisite_andunapproved_catalogue_scope_closed=True,new_credit=0,full_goal_complete=False))
