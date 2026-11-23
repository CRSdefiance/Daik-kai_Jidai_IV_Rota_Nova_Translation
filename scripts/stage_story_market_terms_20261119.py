"""Stage the exact six story blocks over the registered Market Help candidate."""
from types import FunctionType

from scripts import review_story_market_terms_20261119 as review
from scripts import stage_rafael_first_voyage_debrief_20261119 as previous

base, native, stage, parent = review.base, review.native, review.stage, review.parent
workflow = previous.workflow
ROOT = review.ROOT / "staged_v3"
ROM = ROOT / "Story_Market_Terms_STAGED.nds"
PROOF = ROOT / "stored_proof.json"
logical_end, paired = workflow.logical_end, review.paired
rebuild_function = previous.rebuild_function
MAX_COMPANY_CELLS = previous.MAX_COMPANY_CELLS

if __name__ == "__main__":
    env = workflow.env | globals()
    env["catalogue_membership"] = FunctionType(workflow.catalogue.catalogue_membership.__code__, env)
    FunctionType(workflow.env["main"].__code__, env)()
