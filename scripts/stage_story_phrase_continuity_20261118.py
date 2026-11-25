"""Integrate the reviewed phrase wraps with the exact registered parent."""

from types import FunctionType

from scripts import prepare_story_phrase_continuity_20261118 as paired
from scripts import review_story_phrase_continuity_20261118 as review
from scripts import stage_story_tag_wraps_20261118 as previous

base, native, stage, parent = previous.base, previous.native, previous.stage, paired.parent
ROOT = paired.ROOT / "research_v1"
ROM = ROOT / "Story_Phrase_Continuity_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = stage.logical_end

catalogue_membership = FunctionType(previous.catalogue_membership.__code__, vars(previous) | globals())


if __name__ == "__main__":
    precedent = previous.env["main"]
    FunctionType(precedent.__code__, precedent.__globals__ | globals())()
