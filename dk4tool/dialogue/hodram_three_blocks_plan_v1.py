"""Exact source-owned automatic Hodram planner;complete source preamble separate from guarded NUL-free body."""
from pathlib import Path
from scripts.plan_Hodram_B137_B45_B46_v8245 import ENV
from scripts.verify_village_wrap_v608 import read
from dk4tool.patch.grand_race_menu_release import sha
PLAN=Path("work/analysis/Hodram_B137_B45_B46_layout_v8245/28_automatic_Hodram_plans_full_native_width.json")
PLAN_SHA="01dc71ce720fd5241dd4b1cdbd81dda8206156008377a1dceb182ed1a7108dc5"
assert sha(PLAN.read_bytes())==PLAN_SHA
environment=dict(ENV)
environment["PAIRS"]={tuple(p) for p in read(PLAN)["source_word_boundary_pairs"]}
environment["COHERENT_PAIRS"]={tuple(p) for p in read(PLAN)["source_coherent_phrase_pairs"]}
exec(compile(read(PLAN)["source_owned_plan_adapter"],str(PLAN)+"::frozen", "exec"),environment)
plan=environment["plan"]
