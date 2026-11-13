"""Correct one inherited event-label identifier before running the B174 audit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_actual_tools_v4489b')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/audit_lil_B174_actual_v4489.py','scripts/audit_lil_B174_actual_v4489b.py',{
        'lil_B174_actual_v4489':'lil_B174_actual_v4489b',
        'actual_source_event173_not_selected':'actual_source_event174_not_selected',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tool=tool,
        initial_unexecuted_producer_preserved=True,no_ROM_prose_orcoverage_change=True,full_goal_complete=False))
    print('Prepared actual audit successor with source event174 label; capture evidence unchanged.')
