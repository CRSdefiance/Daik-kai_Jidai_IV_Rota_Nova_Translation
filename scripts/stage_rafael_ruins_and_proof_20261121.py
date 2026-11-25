"""Compile Rafael's reviewed encounters with their original choices and actor styles."""

from scripts import review_rafael_ruins_and_proof_20261121 as review
from scripts import stage_rafael_followup_encounters_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
compiler, rebuild_function, current_fe_painter = precedent.compiler, precedent.rebuild_function, precedent.current_fe_painter
ROOT = review.ROOT / "staged_v3"
ROM, PROOF = ROOT / "Rafael_Ruins_And_Proof_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = review.OUTPUT


if __name__ == "__main__":
    source = checked_text(compiler.source, {"stage.system.native_painter(ctx)": "current_fe_painter(ctx)"})
    scope = compiler.env | globals() | {"paired": review}
    exec(compile(source, __file__, "exec"), scope)
    scope["main"]()
