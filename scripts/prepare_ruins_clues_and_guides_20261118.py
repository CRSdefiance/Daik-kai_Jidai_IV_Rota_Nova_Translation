"""Pair the next ruin investigations and guides against the registered cave candidate."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_jungle_caves_20261118 as parent


ROOT = Path("work/ruins_clues_and_guides_source_20261118")
BLOCKS = (tuple(range(302, 306)), tuple(range(294, 300)), tuple(range(289, 294)), tuple(range(260, 265)))
CONTEXT = (
    "Follow Rafael's inland lead, the Veda discussion and the response to the parchment through the guide's map requirement and the destination.",
    "Follow Hodram's inland search, the rumor of homes cut into the rock, and the material and crew requirements through the excavation attempt.",
    "Follow Lil's questions about Angkor, the platinum lead and the inscription through the discovery of the coin and the subsequent guide exchange.",
    "Follow Maria's shark-fin request and its variants through the rumored inland ruins, the coin and the map-dependent arrival.",
)


if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
