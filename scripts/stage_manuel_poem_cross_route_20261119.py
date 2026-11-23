"""Compile the shared Manuel poem through the registered story loaders."""

from types import FunctionType

from scripts import review_manuel_poem_cross_route_20261119 as review
from scripts import stage_story_short_phrase_wraps_20261119 as workflow

base, native, stage, parent = review.base, review.native, review.stage, review.parent
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Manuel_Poem_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end, paired = workflow.logical_end, review.paired


if __name__ == "__main__":
    env = workflow.env | globals()
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, env)
    FunctionType(workflow.env["main"].__code__, env)()
