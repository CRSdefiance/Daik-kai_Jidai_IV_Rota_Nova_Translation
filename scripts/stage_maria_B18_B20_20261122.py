"""Compile Maria's reviewed early scenes on the registered cumulative base."""

from types import SimpleNamespace

from scripts import review_maria_B18_B20_20261122 as review
from scripts.source_locked_derivation_v5118 import checked_text

parent, base, native = review.build, review.base, review.native
engine, compiler = parent.writer.engine, parent.writer.compiler
FIRST_ROOT = review.ROOT / "B18_B20_staged_v1"
ROOT = review.ROOT / "B18_B20_staged_v2"
ROM, PROOF = ROOT / "Maria_B18_B20_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT = review.ROOT / "B18_B20_scoped_manuscript_v2.json"
BLOCKS = ((), (), (), tuple(review.DECISIONS))


def main():
    assert not ROOT.exists()
    draft, release, preflight = map(base.load, (review.FINAL_DRAFT, parent.RELEASE, review.FINAL_LAYOUT))
    assert base.digest(review.FINAL_DRAFT) == preflight["draft_sha256"]
    assert preflight["candidate_sha256"] == release["candidate_sha256"]
    draft.update(previous_sha256=release["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        encoder="dialogue-relocatable-v1", planned_FE={}, findings={"wording": 43, "retention": 45},
        contextual_records_revisited=88, contextual_decisions_reused=0)
    if MANUSCRIPT.exists():
        assert base.load(MANUSCRIPT) == draft
    else:
        base.save(MANUSCRIPT, draft)
    scope = compiler.env | globals() | {
        "review": SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=review.PACKET),
        "paired": SimpleNamespace(BLOCKS=BLOCKS), "draft": draft, "assemble": engine.assemble,
    }
    program = checked_text(engine.program, {
        'if g["block"] in paired.BLOCKS[1]': 'if g["block"] in paired.BLOCKS[3]',
    })
    exec(compile(program, __file__ + "::registered-Maria-stored-commands", "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["whole_parent_inverse"] and stored["changed_blocks"] == {review.ARCHIVE: list(BLOCKS[3])}
    for group in stored["groups"]:
        assert all(plan == preflight["plans"][ident] for ident, plan in group["plans"].items())
    assert sum(len(group["plans"]) for group in stored["groups"]) == len(preflight["plans"])


if __name__ == "__main__":
    main()

