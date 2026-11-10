"""Prefer complete paragraphs with fewer added rows before soft boundary preferences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_row_priority_tools_v7984c')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/plan_Rafael_B47_layout_v7984b.py','scripts/plan_Rafael_B47_layout_v7984c.py',{
        'Rafael_B47_layout_v7984b':'Rafael_B47_layout_v7984c',
        "ADAPTER=checked_text(previous.ADAPTER,{":
            "ADAPTER=checked_text(previous.ADAPTER,{\n    'cost[0]+tiny+weak,cost[1]+1,cost[2]+weak':'cost[0]+tiny,cost[1]+1,cost[2]+weak',",
        'all_original_QA_issues_preserved_no_waivers=True':
            'all_original_QA_issues_preserved_without_removal=True,ordinary_boundary_warning_review_pending=True,orphan_avoidance_then_rows_then_soft_weak_preferences=True',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(derivation=result,
        finding='Prior B47 plans R5/R63 spend a fourth short row solely to avoid ordinary soft boundaries;that repeats the premature-wrap lead.',
        correction='Keep orphan avoidance first,then minimize added rows,then prefer stronger boundaries andbalance. Preserve all existing QA diagnostics for individual review.',
        unchanged_full216_width_four_physical_rows_guards_pair_phase_words_andnative_numeric_constants=True,
        no_global_profile_orhistorical_compiler_change=True,
        retrospective_inherited_weak_before_row_priority_lead_preserved_for_full_editorial_goal=True,
        new_credit=0,full_goal_complete=False))
    print('Prepared source-bound B47 row-priority successor;no prose/geometry/QA guard changes. Individual boundary review pending.')
