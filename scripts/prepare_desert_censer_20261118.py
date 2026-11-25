"""Pair the next desert expeditions, censer rumors and return exchanges."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_sakura_expeditions_macao_20261118 as parent

ROOT = Path("work/desert_censer_source_20261118")
BLOCKS = (tuple(range(328, 332)), (313, 314, 315), (316, 317, 318), tuple(range(280, 286)))
CONTEXT = (
    "Follow the newly found map, Rafael's desert detour, the fortune-teller's censer request and the reading.",
    "Follow Hodram through the desert choices, the censer request and the fortune-teller's return exchange.",
    "Follow Lil's desert branches, including the cactus and the dropped luggage, then the censer request and reading.",
    "Follow Maria's map guardians, wolf encounter, palace invitation, forest detour, map rumor and desert choices.",
)

if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
