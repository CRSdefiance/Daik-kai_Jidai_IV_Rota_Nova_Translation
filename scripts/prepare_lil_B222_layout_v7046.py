"""Prepare a whole-paragraph planner using B222's own collocations and source selectors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_layout_tools_v7046')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/plan_lil_B221_layout_v6976.py');pairline=next(s for s in source.read_text('utf8').splitlines() if s.startswith('PAIRS='))
    pairs={('military','commander'),('hundreds','of'),('years','ago'),('final','naval'),('naval','battle'),('seven','ships'),('enemy','commander'),('enemy','soldier'),('each','arm'),('gleaming','armor'),('soft','spot'),('pure','heart'),('island','nation'),('get','back'),('back','to')}
    row=derive(source,'scripts/plan_lil_B222_layout_v7046.py',{
        'B221':'B222','layout_v6976':'layout_v7046','[2,17,85]':'[2,16]',pairline:'PAIRS='+repr(pairs),
        'fourteen_whole_paragraph_plans_no_macros_no_prose_changes':'sixteen_whole_paragraph_plans_no_macros_no_prose_changes','all14_formatting_gates_remain_false':'all16_formatting_gates_remain_false'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_layout_planner.json',dict(tool=row,all_native_geometry_pair_phase_guard_and_bare_I_rules_preserved=True,
        source_specific_collocations_no_story_wording_change=True,new_review_credit=0,full_goal_complete=False))
