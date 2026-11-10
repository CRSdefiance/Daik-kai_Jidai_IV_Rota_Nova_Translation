"""Close B231 immutable evidence before the production reconstruction check."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_positive_tools_v7511')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={'B230':'B231','final_paths_v7457':'final_paths_v7505','atomic_v7463':'atomic_v7511','v7462':'v7510','seal_lil_B230_references_v7459':'seal_lil_B231_references_v7507','source_locked_static_item_country_scope':'source_locked_medical_book_scope','==17':'==16','positive_records=17':'positive_records=16','source988_bytes_inverse_source_tail0_target_tail2_recovered':'source724_bytes_inverse_source_tail2_target_tail2_recovered','all17_actual17_pages67_body67_headers_bound':'all16_actual16_pages63_body63_headers_bound','17 speeches/17 pages,complete988-byte':'16 speeches/16 pages,complete724-byte'}
    row=derive('scripts/validate_lil_B230_atomic_v7463.py','scripts/validate_lil_B231_atomic_v7511.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive_validator.json',dict(tool=row,immutable_inputs_only_no_mutable_registry_ledger_pins_orbuilder_dependency=True,new_credit=0,full_goal_complete=False))
