"""Exact source-owned automatic Hodram planner;complete source preamble separate from guarded NUL-free body."""
from pathlib import Path
from scripts.plan_Hodram_B51_v8562 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Hodram_B51_layout_v8562/automatic_plans.json")
PLAN_SHA="3e4e9f12b6d2fb7c5bc8a99ce772b9d15c6a3bc70ac7d1d205a883d0562af24b"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
exec(compile(read(PLAN)["source_owned_planner"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
