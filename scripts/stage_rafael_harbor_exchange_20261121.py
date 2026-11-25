"""Compile Rafael's reviewed harbor exchange and preserve all original branches."""
from pathlib import Path

from scripts import review_rafael_harbor_exchange_20261121 as review
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts.source_locked_derivation_v5118 import checked_text


base,native,parent = review.base,review.native,review.parent
ROOT=Path("out/rafael_harbor_exchange_20261121/staged")
ROM,PROOF=ROOT/"Rafael_Harbor_Exchange_STAGED.nds",ROOT/"stored_proof.json"
logical_end=compiler.logical_end


if __name__=="__main__":
    ROOT.parent.mkdir(exist_ok=True)
    script=checked_text(compiler.source,{
        "painter = stage.system.native_painter(ctx)": "painter = None",
        "Staged all revised story phrases": "Staged Rafael's full harbor and preparation exchange",
    })
    scope=compiler.env|globals()|{"paired":review}
    exec(compile(script,__file__+"::harbor","exec"),scope)
    scope["main"]()
    proof=base.load(PROOF)
    assert proof["changed_blocks"] == {"/data/SC0.DK4":[44]} and proof["whole_parent_inverse"]
