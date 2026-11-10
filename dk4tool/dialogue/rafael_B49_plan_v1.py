"""Exact source-owned automatic B49 planner;00 preamble separate from guarded NUL-free text."""
from pathlib import Path
from scripts.plan_Rafael_B49_layout_v8090c import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Rafael_B49_layout_v8090c/61_automatic_plans_full_native_width_exact_source00_02_09_no_FE.json")
PLAN_SHA="70cd0bef59c78fd7cd53f2179cc42a86967cb8e8b62166773bb6e8857a5b9063"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["source_coherent_phrase_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
