"""Compile the revised early Rafael dialogue through the registered story workflow."""

from types import FunctionType

from scripts import review_rafael_contract_and_proof_20261119 as review
from scripts import stage_story_short_phrase_wraps_20261119 as workflow

base, native, stage, parent = review.base, review.native, review.stage, review.parent
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Rafael_Contract_and_Proof_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = workflow.logical_end
paired = review.paired
paired.BLOCKS = review.BLOCKS


if __name__ == "__main__":
    env = workflow.env | globals()
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, env)
    FunctionType(workflow.env["main"].__code__, env)()
