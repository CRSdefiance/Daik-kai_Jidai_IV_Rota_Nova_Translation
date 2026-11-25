"""Exact source-owned automatic B48 planner;00 preamble separate from guarded NUL-free text."""
from pathlib import Path
from scripts.plan_Rafael_B48_layout_v8035d import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Rafael_B48_layout_v8035d/91_automatic_plans_full_native_width_source_preambles4_FE.json")
PLAN_SHA="2f2925b016d63e689f4cf0dc0aa8d45a71f74b6da4061354176a9433268bbb37"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
