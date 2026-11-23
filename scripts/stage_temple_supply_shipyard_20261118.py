"""Compile the reviewed temple, supply and shipyard exchanges over Rafael's registered release."""

from types import FunctionType

from scripts import review_temple_supply_shipyard_20261118 as review
from scripts import stage_ruins_clues_and_guides_20261118 as inherited

previous = inherited.previous
base, native, stage, parent = inherited.base, inherited.native, inherited.stage, review.parent
paired = review
logical_end = stage.logical_end
ROOT = review.paired.original.ROOT / "remaining_three_routes_research_v3"
ROM = ROOT / "Temple_Supply_Shipyard_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"


if __name__ == "__main__":
    build = FunctionType(previous.main.__code__, vars(previous) | globals() |
                         {"rebuild_function": inherited.rebuild_function})
    build()


