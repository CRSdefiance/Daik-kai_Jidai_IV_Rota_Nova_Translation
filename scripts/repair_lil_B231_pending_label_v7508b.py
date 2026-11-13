"""Correct a copied count label before any pending checkpoint execution."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_pending_tools_v7508b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B231_pending_checkpoint_v7508').exists()
    row=derive('scripts/checkpoint_lil_B231_pending_v7508.py','scripts/checkpoint_lil_B231_pending_v7508b.py',{'all17_five_individual_source_native_stored_actual_reference_gates_complete':'all16_five_individual_source_native_stored_actual_reference_gates_complete'})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_count_label_correction.json',dict(tool=row,unexecuted_predecessor_preserved=True,metadata_only_no_prose_runtime_orcredit_change=True,new_credit=0,full_goal_complete=False))
