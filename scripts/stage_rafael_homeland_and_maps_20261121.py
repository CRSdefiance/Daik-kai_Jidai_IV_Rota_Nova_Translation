"""Stage the reviewed homeland and map dialogue over the registered palace candidate."""

from scripts import review_rafael_homeland_and_maps_20261121 as review
from scripts import stage_rafael_palace_and_alliance_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "homeland_and_maps_staged_v3"
ROM, PROOF = ROOT / "Rafael_Homeland_And_Maps_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = review.OUTPUT


if __name__ == "__main__":
    compiler = precedent.precedent.prior.compiler
    source = checked_text(compiler.source, {"stage.system.native_painter(ctx)": "current_fe_painter(ctx)"})
    scope = compiler.env | vars(precedent.precedent.prior) | globals() | {"paired": review}
    exec(compile(source, __file__ + "::stage", "exec"), scope)
    scope["main"]()
