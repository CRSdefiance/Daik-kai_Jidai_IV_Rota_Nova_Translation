"""Stage Rafael's rescue and lesson batch with its original companion slots."""

from scripts import review_rafael_rescue_and_lessons_20261121 as review
from scripts import stage_rafael_ruins_and_proof_20261121 as prior


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v4"
ROM, PROOF = ROOT / "Rafael_Rescue_And_Lessons_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = review.OUTPUT


if __name__ == "__main__":
    compiler = prior.compiler
    source = prior.checked_text(compiler.source, {"stage.system.native_painter(ctx)": "current_fe_painter(ctx)"})
    lineup = vars(prior) | globals()
    env = compiler.env | lineup | {"paired": review}
    exec(compile(source, __file__, "exec"), env)
    env["main"]()
