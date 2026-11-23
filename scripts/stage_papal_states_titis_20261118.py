"""Stage the Papal States and Titis exchanges against the registered parent."""

from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import review_papal_states_titis_20261118 as review
from scripts import stage_story_tag_wraps_20261118 as precedent

base, native, stage, parent = precedent.base, precedent.native, precedent.stage, review.parent
ROOT = review.ROOT / "research_v1"
ROM = ROOT / "Papal_States_Titis_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = stage.logical_end

if __name__ == "__main__":
    build = precedent.env["main"]
    env = build.__globals__ | globals() | {"paired": review}
    env["catalogue_membership"] = FunctionType(precedent.catalogue_membership.__code__, env)
    FunctionType(build.__code__, env)()
