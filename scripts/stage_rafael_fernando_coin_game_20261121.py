"""Build the reviewed Fernando exchange with source-bound native relocation."""
from inspect import getsource

from scripts import review_rafael_fernando_coin_game_20261121 as review
from scripts.stage_hodram_alexandria_tutorial_20261121 import compiler, plan_progressive
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v1"
ROM, PROOF = ROOT / "Rafael_Fernando_Coin_Game_STAGED.nds", ROOT / "stored_proof.json"


if __name__ == "__main__":
    source = checked_text(compiler.source, {"painter = stage.system.native_painter(ctx)": "painter = None"})
    scope = compiler.env | globals() | {"paired": review}
    rebuild = checked_text(getsource(compiler.rebuild_function), {"workflow.plan_progressive": "plan_progressive"})
    exec(compile(rebuild, __file__ + "::rebuild", "exec"), scope)
    exec(compile(source, __file__ + "::main", "exec"), scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["whole_parent_inverse"] and proof["changed_blocks"] == {"/data/SC0.DK4": [178]}
