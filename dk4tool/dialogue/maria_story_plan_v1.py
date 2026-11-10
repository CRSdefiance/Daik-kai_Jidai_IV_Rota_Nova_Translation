"""The exact final-v3 source-owned automatic Maria planner; no authored layout."""
from pathlib import Path
from scripts.plan_Maria_story_layout_v7733 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path('work/analysis/maria_story_final_prose_v7756b/67_final_v3_plans_two_refinements65_exact_compiled_retentions.json')
PLAN_SHA='f955bdb6d9d82990873b46b298e4bfca00f498016823d46d147e39237834a0a2'
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
exec(compile(read(PLAN)['source_owned_automatic_plan_adapter'],str(PLAN)+'::frozen','exec'),environment)
plan=environment['plan']
