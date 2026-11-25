"""Exact source-owned sparse Lil planner;native01/09/10 prefixes andguarded NUL-free text."""
from pathlib import Path
from scripts.plan_Gerhard_layout_v8205 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json")
PLAN_SHA="64c8812fcefcf8c91692d3a8bee8c49c17e0d128b7f3a65b7376fd1d4b9d64d6"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["source_coherent_phrase_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
