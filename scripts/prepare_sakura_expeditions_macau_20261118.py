"""Pair the next Sakura, expedition and Macau exchanges against the registered candidate."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_temple_supply_shipyard_20261118 as parent

ROOT = Path("work/sakura_expeditions_macau_source_20261118")
BLOCKS = (tuple(range(321, 328)), (310, 311, 312), (312, 313, 314, 315), tuple(range(275, 280)))
CONTEXT = (
    "Follow Rafael's chintz and wine visit with Sakura, the map-guardian rumor, the wolf and the city-gate forest detour.",
    "Follow Hodram's discreet city-gate inquiry, the dark-forest route choices and the rumor of a recently discovered map.",
    "Follow Lil's wolf encounter, the city-gate directions, the steep forest route and the rumor of a map to nearby ruins.",
    "Follow Maria and Sakura from helping the wounded stranger through the Macau inquiries, impersonation at the governor's office and return to Sakura.",
)

if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
