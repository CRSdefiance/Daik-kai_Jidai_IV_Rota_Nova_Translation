"""Pair the mosque, temple, supply and shipyard follow-ups with the overland candidate."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_overland_passages_20261118 as parent

ROOT = Path("work/mosque_temple_shipyard_source_20261118")
BLOCKS = ((313, 315, 316, 317, 318, 319, 320), (304, 305, 306, 307, 308, 309),
          (303, 304, 305, 306, 307, 308, 309, 310, 311), (271, 272, 273, 274))
CONTEXT = (
    "Follow Rafael's dancer, missing explorers, proposed offerings and rescue, then the direction to Basra and the detour choices.",
    "Follow Hodram and Sakura from the expedition and temple invitation to the requested memento, the monk's directions and the wolf encounter.",
    "Follow Lil's spice exhibit deliveries, bridge detour, temple invitation, errands and the village map lead.",
    "Follow Maria's shipyard commission and completion, the guildmaster's reward and Sakura's expedition and navigation choices.",
)

if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
