"""Compile Julio's revised tutorial over the exact registered Save and Load candidate."""

from types import FunctionType

from scripts import review_rafael_deck_lesson_20261119 as review
from scripts import stage_story_tag_wraps_20261118 as template

base, native, stage = template.base, template.native, template.stage
parent = review.parent
ROOT = review.ROOT / "research_v1"
ROM = ROOT / "Rafael_Deck_Lesson_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
logical_end = template.logical_end


def main():
    original = template.env["main"]
    scope = original.__globals__ | globals() | {"paired": review}
    scope["catalogue_membership"] = FunctionType(template.catalogue_membership.__code__, scope)
    FunctionType(original.__code__, scope)()
    receipt = base.load(PROOF)
    assert receipt["whole_parent_inverse"] and receipt["changed_blocks"] == {"/data/SC0.DK4": [43]}


if __name__ == "__main__":
    main()
