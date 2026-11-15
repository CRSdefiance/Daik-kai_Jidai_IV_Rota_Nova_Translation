"""Exact source-owned automatic B46 planner;00 preamble separate from guarded NUL-free text."""
from pathlib import Path
from scripts.plan_Rafael_B46_layout_v7932 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json")
PLAN_SHA="4ee17671273d910cab68ea098798462fae28546e4f7f714d799ffb0878bc0e5f"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
