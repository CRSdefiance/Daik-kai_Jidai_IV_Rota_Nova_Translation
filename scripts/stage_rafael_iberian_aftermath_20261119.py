"""Compile the Sofala and adjacent exchanges over the registered North Sea ROM."""

from types import FunctionType

from scripts import review_rafael_iberian_aftermath_20261119 as review
from scripts import stage_rafael_first_voyage_debrief_20261119 as prior

base, native, stage, parent = review.base, review.native, review.stage, review.parent
workflow = prior.workflow
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Rafael_Iberian_Aftermath_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end, paired = workflow.logical_end, review.paired
rebuild_function = prior.rebuild_function
MAX_COMPANY_CELLS = prior.MAX_COMPANY_CELLS


if __name__ == "__main__":
    env = workflow.env | globals()
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, env)
    FunctionType(workflow.env["main"].__code__, env)()
