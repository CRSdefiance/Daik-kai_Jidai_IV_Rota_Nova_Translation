"""Stage the five Rafael exchanges, including one revised FE body."""

from inspect import getsource

from scripts import review_rafael_tradehouse_festival_20261121 as review
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter
from scripts.stage_hodram_alexandria_tutorial_20261121 import compiler, plan_progressive
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v3"
ROM, PROOF = ROOT / "Rafael_Tradehouse_Festival_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT, logical_end = review.OUTPUT, compiler.logical_end


if __name__ == "__main__":
    source = checked_text(compiler.source, {"stage.system.native_painter(ctx)": "current_fe_painter(ctx)"})
    scope = compiler.env | globals() | {"paired": review}
    rebuild = checked_text(getsource(compiler.rebuild_function), {"workflow.plan_progressive": "plan_progressive"})
    exec(compile(rebuild, __file__ + "::rebuild", "exec"), scope)
    exec(compile(source, __file__ + "::build", "exec"), scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["changed_blocks"] == {"/data/SC0.DK4": list(review.BLOCKS[0])} and proof["whole_parent_inverse"]
