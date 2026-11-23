"""Compile the four Mediterranean and North Sea exchanges with original controls."""
from scripts import review_rafael_mediterranean_dialogue_20261121 as review
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v2"
ROM, PROOF = ROOT / "Rafael_Mediterranean_Dialogue_STAGED.nds", ROOT / "stored_proof.json"
logical_end = compiler.logical_end


if __name__ == "__main__":
    script = checked_text(compiler.source, {"painter = stage.system.native_painter(ctx)": "painter = None"})
    scope = compiler.env | globals() | {"paired": review}
    exec(compile(script, __file__, "exec"), scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["changed_blocks"] == {"/data/SC0.DK4": [47, 48, 49, 50]} and proof["whole_parent_inverse"]
