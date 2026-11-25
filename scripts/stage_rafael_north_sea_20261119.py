"""Compile the North Sea conversations with the previously verified Rafael name budgets."""

from types import FunctionType

from scripts import review_rafael_north_sea_20261119 as review
from scripts import stage_rafael_first_voyage_debrief_20261119 as precedent

base, native, stage, parent = review.base, review.native, review.stage, review.parent
workflow = precedent.workflow
ROOT = review.ROOT / "research_v3"
ROM = ROOT / "Rafael_North_Sea_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end, paired = workflow.logical_end, review.paired
rebuild_function = precedent.rebuild_function
MAX_COMPANY_CELLS = precedent.MAX_COMPANY_CELLS


if __name__ == "__main__":
    env = workflow.env | globals()
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, env)
    FunctionType(workflow.env["main"].__code__, env)()
