"""Exact source-owned automatic Hodram planner;complete source preamble separate from guarded NUL-free body."""
from pathlib import Path
from scripts.plan_Hodram_B54_B60_v8802d import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Hodram_B54_B60_layout_v8802d/automatic_plans.json")
PLAN_SHA="b9a5232c7bbe2c928cfccab85805005c28204134d7746639b045e3e861c2cfe5"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["coherent_pairs"]}
exec(compile(read(PLAN)["source_owned_planner"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
