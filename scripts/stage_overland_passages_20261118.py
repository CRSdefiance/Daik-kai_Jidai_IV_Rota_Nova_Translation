"""Compile the overland edits on the registered cumulative ROM."""

from types import FunctionType

from scripts import prepare_overland_passages_20261118 as paired
from scripts import review_overland_passages_20261118 as review
from scripts import stage_ruins_clues_and_guides_20261118 as inherited

previous = inherited.previous
base, native, stage, parent = inherited.base, inherited.native, inherited.stage, review.parent
logical_end = stage.logical_end
ROOT = paired.ROOT / "research_v2"
ROM = ROOT / "Overland_Passages_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"


if __name__ == "__main__":
    build = FunctionType(previous.main.__code__, vars(previous) | globals() |
                         {"rebuild_function": inherited.rebuild_function})
    build()

