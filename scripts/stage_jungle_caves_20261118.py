"""Compile the contextual cave review with the registered dialogue relocation rules."""

from types import FunctionType

from scripts import stage_london_guild_assignments_20261118 as previous
from scripts import review_jungle_caves_20261118 as review


paired = review.current
base, native, stage, parent = previous.base, previous.native, previous.stage, review.parent
logical_end = stage.logical_end
ROOT = paired.ROOT / "research_v2"
ROM = ROOT / "Jungle_And_Caves_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"


if __name__ == "__main__":
    build = FunctionType(previous.main.__code__, vars(previous) | globals())
    build()
