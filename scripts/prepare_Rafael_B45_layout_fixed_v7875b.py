"""Preserve the failed unknown-profile plan and derive the registered-profile successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_layout_repair_v7875b');assert not root.exists()
    result=derive('scripts/plan_Rafael_B45_layout_v7875.py','scripts/plan_Rafael_B45_layout_v7875b.py',{
        'work/analysis/Rafael_B45_layout_v7875':'work/analysis/Rafael_B45_layout_v7875b',
        "get_dialogue_profile('raphael-story-shared-events-live')":"get_dialogue_profile('raphael-story-live')",
        "('governor\\\\x27s','office')":"(\"governor's\",'office')",
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        failed_plan='work/analysis/Rafael_B45_layout_v7875/12_automatic_plans_distinct_progressive216_FE228_all_QA_preserved.json',
        failure='Unknown dialogue profile: raphael-story-shared-events-live',
        exact_registered_raphael_story_live_with_measuredFI6_andsource_bound_selectors=True,
        governor_office_pair_literal_corrected=True,no_prose_orviewport_orQA_guard_change=True,new_credit=0,full_goal_complete=False))
