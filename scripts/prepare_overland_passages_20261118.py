"""Pair the four forest, guide and desert sequences against the ruin candidate."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_ruins_clues_and_guides_20261118 as parent


ROOT = Path("work/overland_passages_source_20261118")
BLOCKS = ((310, 311, 312, 314), (300, 301, 302, 303), (299, 300, 301, 302), (267, 268, 269, 270))
CONTEXT = (
    "Follow Rafael's forest expedition, inland directions and desert route before the rumor about recognition at court.",
    "Follow Hodram's forest expedition, inland directions and desert route before the rumor about recognition at court.",
    "Follow Lil's reluctant forest expedition, inland directions and desert route before the rumor about recognition at court.",
    "Follow Maria's forest expedition, inland directions and desert route before the rumor about recognition at court.",
)


if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
