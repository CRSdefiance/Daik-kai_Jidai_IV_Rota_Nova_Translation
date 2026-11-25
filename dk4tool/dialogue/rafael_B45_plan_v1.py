"""Exact source-owned automatic B45 planner;00 preamble separate from guarded NUL-free text."""
from pathlib import Path
from scripts.plan_Rafael_B45_layout_v7881b import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Rafael_B45_layout_v7881b/12_automatic_plans_full_native_width_zero_preamble_separate_body.json")
PLAN_SHA="1d3aa2076e3eec40c6e4490f9e008dc32ba626e24d5a13787cdad175af230211"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
