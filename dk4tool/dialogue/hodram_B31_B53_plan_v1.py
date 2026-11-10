"""Exact source-owned automatic Hodram planner;complete source preamble separate from guarded NUL-free body."""
from pathlib import Path
from scripts.plan_Hodram_B31_B53_v8725 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Hodram_B31_B53_layout_v8725/automatic_plans.json")
PLAN_SHA="cc2409fc726311f7fbd93cf2fc33ca31dfc274d471b634ec5440bcd64d7fbc9e"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
exec(compile(read(PLAN)["source_owned_planner"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
