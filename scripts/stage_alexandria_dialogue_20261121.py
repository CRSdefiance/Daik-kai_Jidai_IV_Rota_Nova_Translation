"""Compile the Alexandria dialogue and forecast with their original consumers."""
from types import SimpleNamespace

from scripts import review_alexandria_dialogue_20261121 as review
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts import verify_stockholm_dialogue_display_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged"
ROM, PROOF = ROOT / "Alexandria_Dialogue_STAGED.nds", ROOT / "stored_proof.json"
logical_end = compiler.logical_end


if __name__ == "__main__":
    script = checked_text(compiler.source, {
        "painter = stage.system.native_painter(ctx)": "painter = display.town.current_fe_painter(ctx)",
    })
    scope = compiler.env | globals() | {"paired": review}
    exec(compile(script, __file__, "exec"), scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["changed_blocks"] == {f"/data/SC{i}.DK4": list(blocks) for i, blocks in enumerate(review.BLOCKS)}
    assert proof["whole_parent_inverse"]
