"""Exact source-owned automatic Hodram planner;complete source preamble separate from guarded NUL-free body."""
from pathlib import Path
from scripts.plan_Hodram_B47_B48_v8323 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Hodram_B47_B48_layout_v8323/six_automatic_plans_original_usable_width_distinct_FE_all_QA_preserved.json")
PLAN_SHA="97420058ab399bbeeb7ba052a27c346365519b19b3f55a525ea55fdd77cbf7e6"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
exec(compile(read(PLAN)["source_owned_planner"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
