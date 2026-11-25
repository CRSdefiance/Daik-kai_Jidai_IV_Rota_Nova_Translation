"""Stage the warrior and village exchanges over their exact registered parent."""

from types import FunctionType

from scripts import review_warrior_village_handovers_20261118 as review
from scripts import stage_ruins_clues_and_guides_20261118 as inherited

paired = review.paired
previous = inherited.previous
base, native, stage, parent = previous.base, previous.native, previous.stage, review.parent
logical_end = stage.logical_end
ROOT = paired.ROOT / "research_v2"
ROM = ROOT / "Warrior_Village_Handovers_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"

if __name__ == "__main__":
    build = FunctionType(previous.main.__code__, vars(previous) | globals() |
                         {"rebuild_function": inherited.rebuild_function})
    build()
