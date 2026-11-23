"""Stage Rafael's reviewed exchanges with the registered story compiler."""

from scripts import review_rafael_north_sea_africa_20261121 as review
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "staged_v2"
ROM, PROOF = ROOT / "Rafael_North_Sea_Africa_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = review.OUTPUT
logical_end = compiler.logical_end


if __name__ == "__main__":
    source = checked_text(compiler.source, {
        "painter = stage.system.native_painter(ctx)": "painter = None",
        'for g in packet["groups"]}': 'for g in packet["groups"] if g["block"] in paired.BLOCKS[g["route"]]}',
    })
    scope = compiler.env | globals() | {"paired": review}
    exec(compile(source, __file__, "exec"), scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["whole_parent_inverse"]
    assert set(proof["changed_blocks"]) == {"/data/SC0.DK4"}
    assert all(block in review.BLOCKS[0] for block in proof["changed_blocks"]["/data/SC0.DK4"])
