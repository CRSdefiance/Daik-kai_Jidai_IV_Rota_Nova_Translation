"""Compile B60 dialogue and typed menus with the registered source-bound pipeline."""

from inspect import getsource

from scripts import review_rafael_spain_20261121 as review
from scripts.stage_hodram_alexandria_tutorial_20261121 import compiler, plan_progressive
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v2"
ROM, PROOF = ROOT / "Rafael_Spain_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT, logical_end = review.OUTPUT, compiler.logical_end


if __name__ == "__main__":
    source = checked_text(compiler.source, {"painter = stage.system.native_painter(ctx)": "painter = None"})
    scope = compiler.env | globals() | {"paired": review}
    rebuild = checked_text(getsource(compiler.rebuild_function), {"workflow.plan_progressive": "plan_progressive"})
    exec(compile(rebuild, __file__ + "::rebuild", "exec"), scope)
    exec(compile(source, __file__ + "::build", "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["changed_blocks"] == {"/data/SC0.DK4": [60]} and stored["whole_parent_inverse"]
