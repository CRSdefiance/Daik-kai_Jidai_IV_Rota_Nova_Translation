"""Build the Maria B21–32 contextual pass and four earlier phrase repairs."""

from types import SimpleNamespace

from scripts import review_maria_B21_B32_20261122 as review
from scripts.source_locked_derivation_v5118 import checked_text


parent,base,native=review.parent,review.base,review.native
engine,compiler=parent.writer.engine,parent.writer.compiler
ROOT=review.ROOT/"B21_B32_staged_v1"
ROM,PROOF=ROOT/"Maria_B21_B32_STAGED.nds",ROOT/"stored_proof.json"
MANUSCRIPT=review.ROOT/"scoped_manuscript_v1.json"
BLOCKS=review.BLOCKS


def main():
    assert not ROOT.exists()
    draft,plans,release=map(base.load,(review.MANUSCRIPT,review.PLANS,parent.RELEASE))
    assert plans["draft_sha256"]==base.digest(review.MANUSCRIPT)
    assert plans["candidate_sha256"]==release["candidate_sha256"]==base.digest(parent.ROM)
    assert draft["previous_registry_sha256"]==release["registry_sha256"]==base.digest(base.REGISTRY)
    row=next(r for r in draft["records"] if r["id"]=="DK4_MES_B29_R0119")
    row["english"]="With FI on our side, we've got the strength of a hundred!"
    row["protected_phrases"]=["the strength of a hundred!"]
    expected=plans["plans"]|review.established.preflight([row])
    draft.update(final_draft_predecessor_sha256=base.digest(review.MANUSCRIPT))
    if MANUSCRIPT.exists():
        assert base.load(MANUSCRIPT)==draft
    else:
        base.save(MANUSCRIPT,draft)
    scope=compiler.env|globals()|dict(review=SimpleNamespace(OUTPUT=MANUSCRIPT,SOURCE=review.PACKET),
        paired=SimpleNamespace(BLOCKS=BLOCKS),draft=draft,assemble=engine.assemble)
    program=checked_text(engine.program, {'if g["block"] in paired.BLOCKS[1]':'if g["block"] in paired.BLOCKS[3]'})
    exec(compile(program,__file__+"::registered-Maria-B21-B32","exec"),scope)
    scope["main"]()
    saved=base.load(PROOF)
    assert saved["whole_parent_inverse"] and set(saved["changed_blocks"])=={review.ARCHIVE}
    parent.writer.reconcile_plans(saved,draft,expected)
    print(f"{len(expected)} changed commands, exact clean/source references and executable branch inventory.")


if __name__=="__main__":
    main()

