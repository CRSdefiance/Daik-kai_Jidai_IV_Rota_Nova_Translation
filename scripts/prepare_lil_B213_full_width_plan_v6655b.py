"""Avoid added rows solely to dodge ordinary complete-word wraps; preserve the first research plan."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_full_width_plan_tools_v6655b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/plan_lil_B213_layout_v6655.py','scripts/plan_lil_B213_layout_v6655b.py',{'layout_v6655':'layout_v6655b',"cost[0]+weak,cost[1]+tiny,cost[2]+1":"cost[0]+1,cost[1]+weak,cost[2]+tiny"});ROOT.mkdir(parents=True);save(ROOT/'source_locked_row_priority_correction.json',dict(proof=proof,only_host_row_priority_changed_no_prose_font_geometry_phase_or_guard_change=True,original_plan_preserved=True,full_goal_complete=False))
