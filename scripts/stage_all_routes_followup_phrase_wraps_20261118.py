"""Stage the current dialogue batch with the registered full-width formatter."""

from types import FunctionType

from scripts import review_all_routes_followup_phrase_wraps_20261118 as review
from scripts import stage_all_routes_next_phrase_wraps_20261118 as template

base, native, stage, paired = template.base, template.native, template.stage, template.paired
parent = review.parent
ROOT = review.ROOT / "research_v1"
ROM, PROOF = ROOT / "All_Routes_Dialogue_Followup_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
logical_end = template.logical_end

if __name__ == "__main__":
    FunctionType(template.main.__code__, vars(template) | globals())()
