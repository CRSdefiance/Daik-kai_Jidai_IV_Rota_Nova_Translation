"""Stage the revised Rafael trade lesson and surrounding story exchanges."""

from pathlib import Path
from types import FunctionType

from scripts import review_rafael_next_phrase_wraps_20261118 as review
from scripts import stage_rafael_early_phrase_wraps_20261118 as prior

base, native, stage, paired, parent = prior.base, prior.native, prior.stage, prior.paired, review.parent
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Rafael_Trade_Lesson_And_Scenes_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = prior.logical_end


def main():
    build = prior.precedent.env["main"]
    env = build.__globals__ | globals() | {"paired": review}
    env["catalogue_membership"] = FunctionType(prior.precedent.catalogue_membership.__code__, env)
    FunctionType(build.__code__, env)()
    checked = base.load(PROOF)
    assert checked["candidate_sha256"] == base.digest(ROM) and checked["whole_parent_inverse"]
    assert checked["changed_blocks"] == {"/data/SC0.DK4": list(review.BLOCKS[0])}


if __name__ == "__main__":
    main()
