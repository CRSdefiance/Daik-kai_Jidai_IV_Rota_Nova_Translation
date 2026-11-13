"""Exact source-owned automatic B47 planner;00 preamble separate from guarded NUL-free text."""
from pathlib import Path
from scripts.plan_Rafael_B47_layout_v7984e import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Rafael_B47_layout_v7984e/15_automatic_plans_full_native_width_zero_preamble_separate_body.json")
PLAN_SHA="ab7e57abba03c0e78ba65bb82996e75ba7b64fcc139b837734be9eb7e5fe3364"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
