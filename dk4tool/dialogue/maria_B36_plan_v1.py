"""The exact final-v3 source-owned automatic Maria planner; no authored layout."""
from pathlib import Path
from scripts.plan_Maria_confrontation_layout_v7793 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path('work/analysis/maria_confrontation_row_reasons_v7801b/16_full_width_plans_nine_individual_row_reasons.json')
PLAN_SHA='e434d92516705bad92e90fa04ac9f07a6d975c71579474b8d18bf4a82941b617'
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment['PAIRS']={tuple(p) for p in read(PLAN)['source_word_boundary_pairs']}
exec(compile(read(PLAN)['source_owned_automatic_plan_adapter'],str(PLAN)+'::frozen','exec'),environment)
plan=environment['plan']
