"""Stage the Hodram review on the cumulative Naturalist and Shield ROM."""

from types import FunctionType

from scripts import review_hodram_early_confrontations_20261119 as review
from scripts import stage_naturalist_aliases_and_shield_20261119 as workflow

base, native, stage = workflow.base, workflow.native, workflow.stage
parent, paired = review.parent, review.paired
ROOT = review.ROOT / "research_v1"
ROM = ROOT / "Hodram_Early_Confrontations_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"

if __name__ == "__main__":
    FunctionType(workflow.main.__code__, vars(workflow) | globals() | {"workflow": workflow.workflow})()
