"""Correct inherited final-review metadata before the completion producer runs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_completion_tools_v4500b')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/complete_lil_B174_v4500.py','scripts/complete_lil_B174_v4500b.py',{
        'actual_source_event173_selected':'actual_source_event174_selected',
        'records=rows, revised=8, retained=3':'records=rows, revised=23, retained=10',
        'source_prose_credit_already_recorded_in_V4426':'source_prose_credit_already_recorded_in_V4475',
        "'promoted_main_build_v4392']":"'promoted_main_build_v4392', 'promoted_main_build_v4452']",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        initial_unexecuted_completion_producer_preserved=True,no_completion_orledger_change=True,full_goal_complete=False))
    print('Prepared final-review metadata successor:23 revisions/10 retentions,source credit V4475,event174; no execution or credit yet.')
