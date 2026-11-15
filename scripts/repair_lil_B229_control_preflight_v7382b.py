"""Preserve preflight rejection; the structural control tool has no snapshot-path literal."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_control_preflight_v7382b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('scripts/prove_lil_B229_consumers_v7382.py').exists()
    r=derive('scripts/prepare_lil_B229_consumers_v7382.py','scripts/prepare_lil_B229_consumers_v7382b.py',{'    jobs=[':"    controls.pop('current_V7324_native_v7329')\n    jobs=[",'consumer_tools_v7382':'consumer_tools_v7382b'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_unused_control_snapshot_key.json',dict(tool=r,first_preflight_rejected_before_any_output_native_case_orROM_mutation=True,only_absent_snapshot_path_key_removed_from_structural_tool=True,new_credit=0,full_goal_complete=False))
