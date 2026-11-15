"""Exact source-owned automatic Hodram planner;complete source preamble separate from guarded NUL-free body."""
from pathlib import Path
from scripts.plan_Hodram_B50_v8491b import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Hodram_B50_layout_v8491b/automatic_plans.json")
PLAN_SHA="2782f3c92071b4d485f8ea14e5d83eb8c4b190e28eed8f40fd7d9d0275cf787a"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
exec(compile(read(PLAN)["source_owned_planner"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
