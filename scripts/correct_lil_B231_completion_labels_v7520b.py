"""Repair copied report labels before the completion producer is executed."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B231_completion_label_tools_v7520b')
if __name__=='__main__':
    assert not ROOT.exists() and not Path('work/analysis/lil_B231_completion_v7520').exists()
    row=derive('scripts/complete_lil_B231_v7520.py','scripts/complete_lil_B231_v7520b.py',{'actual_speeches=17':'actual_speeches=16','V7472':'V7520',"paths.append(Path(doc['source_context']))":"paths.extend([Path(doc['source_context']),Path('work/analysis/lil_B231_completion_label_tools_v7520b/source_locked_metadata_correction.json')])"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_metadata_correction.json',dict(tool=row,unexecuted_predecessor_preserved=True,actual_speeches17_to16_andcopied_completion_heading_corrected=True,no_prose_runtime_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
