"""Stage the cave, offshore ruins and missing monk review over the registered parent."""

from types import FunctionType

from scripts import review_caves_offshore_monk_20261118 as review
from scripts import stage_ruins_clues_and_guides_20261118 as inherited

paired = review.paired
previous = inherited.previous
base, native, stage, parent = previous.base, previous.native, previous.stage, review.parent
logical_end = stage.logical_end
ROOT = paired.ROOT / "research_v4"
ROM = ROOT / "Caves_Offshore_Monk_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"

if __name__ == "__main__":
    build = FunctionType(previous.main.__code__, vars(previous) | globals() |
                         {"rebuild_function": inherited.rebuild_function})
    build()
