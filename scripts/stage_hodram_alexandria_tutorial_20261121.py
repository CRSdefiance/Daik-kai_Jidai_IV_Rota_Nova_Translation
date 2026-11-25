"""Stage the revised Hodram arrival scenes and preserve their original branches."""
from inspect import getsource

from scripts import review_hodram_alexandria_tutorial_20261121 as review
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v4"
ROM, PROOF = ROOT / "Hodram_Alexandria_Tutorial_STAGED.nds", ROOT / "stored_proof.json"

planner_source = checked_text(getsource(compiler.workflow.plan_progressive), {
    'budget = b" " * (len(template) + 32)': (
        'budget = b" " * (len(template) + 64)\n'
        '    if current.count(10) >= 4:\n'
        '        budget = b"\\n" * 4 + budget'
    ),
    'assert plan["expected_native_pages"] == 1 and all':
        'assert 1 <= plan["expected_native_pages"] <= (2 if current.count(10) >= 4 else 1) and all',
})
planner_scope = vars(compiler.workflow).copy()
exec(compile(planner_source, __file__ + "::planner", "exec"), planner_scope)
plan_progressive = planner_scope["plan_progressive"]


if __name__ == "__main__":
    script = checked_text(compiler.source, {"painter = stage.system.native_painter(ctx)": "painter = None"})
    scope = compiler.env | globals() | {"paired": review}
    rebuilding = checked_text(getsource(compiler.rebuild_function), {"workflow.plan_progressive": "plan_progressive"})
    exec(compile(rebuilding, __file__ + "::rebuild", "exec"), scope)
    exec(compile(script, __file__, "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["changed_blocks"] == {"/data/SC1.DK4": [51, 167]} and stored["whole_parent_inverse"]
