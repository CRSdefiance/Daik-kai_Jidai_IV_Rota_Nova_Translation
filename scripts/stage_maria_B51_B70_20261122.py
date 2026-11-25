"""Build the exact Maria dialogue revisions over the registered cumulative ROM."""

from types import SimpleNamespace

from scripts import review_maria_B51_B70_current_20261122 as review
from scripts.source_locked_derivation_v5118 import checked_text


parent,base,native=review.parent,review.base,review.native
engine,compiler=parent.writer.engine,parent.writer.compiler
ARCHIVE="/data/SC3.DK4"
ROOT=review.ROOT/"B51_B70_staged_v3"
ROM,PROOF=ROOT/"Maria_B51_B70_STAGED.nds",ROOT/"stored_proof.json"
MANUSCRIPT=review.DRAFT


def main():
    assert not ROOT.exists()
    draft, expected = map(base.load,(review.DRAFT,review.PLANS))
    assert expected["draft_sha256"]==base.digest(review.DRAFT)
    blocks=tuple(sorted({row["block"] for row in draft["records"]}))
    assert blocks==(53,54,55,57,58,60,61,64)
    scope=compiler.env|globals()|dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT,SOURCE=review.PACKET),
        paired=SimpleNamespace(BLOCKS=((),(),(),blocks)),draft=draft,assemble=engine.assemble)
    code=checked_text(engine.program,{
        'if g["block"] in paired.BLOCKS[1]':'if g["block"] in paired.BLOCKS[3]',
    })
    exec(compile(code,__file__+"::Maria-B51-B70-scope","exec"),scope)
    scope["main"]()
    proof=base.load(PROOF)
    assert proof["whole_parent_inverse"] and proof["changed_blocks"]=={ARCHIVE:[53,54,58,60,61,64]}
    from scripts.stage_maria_opening_hodram_wraps_20261122 import reconcile_plans
    reconcile_plans(proof,draft,expected["plans"])


if __name__=="__main__":
    main()

