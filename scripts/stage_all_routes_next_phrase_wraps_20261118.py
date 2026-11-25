"""Stage the dialogue and wrap corrections across all four routes."""

from inspect import getsource
from types import FunctionType

from scripts import review_all_routes_next_phrase_wraps_20261118 as review
from scripts import stage_rafael_early_phrase_wraps_20261118 as prior
from scripts import stage_late_trade_exchanges_20261118 as company
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage, paired, parent = prior.base, prior.native, prior.stage, prior.paired, review.parent
ROOT = review.ROOT / "research_v2"
ROM, PROOF = ROOT / "All_Routes_Phrase_Review_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
logical_end = prior.logical_end


def main():
    build = prior.precedent.env["main"]
    env = build.__globals__ | globals() | {"paired": review}
    source = checked_text(getsource(prior.precedent.rebuild_function), {
        "precedent.plan_progressive": "company.plan_progressive",
    })
    exec(compile(source, __file__ + "::selective-rebuild-with-company-width", "exec"), env)
    env["catalogue_membership"] = FunctionType(prior.precedent.catalogue_membership.__code__, env)
    FunctionType(build.__code__, env)()
    proof = base.load(PROOF)
    assert proof["whole_parent_inverse"] and proof["candidate_sha256"] == base.digest(ROM)
    assert proof["changed_blocks"] == {f"/data/SC{i}.DK4": list(blocks) for i, blocks in enumerate(review.BLOCKS)}


if __name__ == "__main__":
    main()
