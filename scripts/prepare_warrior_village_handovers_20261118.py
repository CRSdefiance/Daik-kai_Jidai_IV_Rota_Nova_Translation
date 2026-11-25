"""Pair the fog, warrior trial and village handovers to the registered candidate."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_caves_offshore_monk_20261118 as parent

ROOT = Path("work/warrior_village_handovers_source_20261118")
BLOCKS = (tuple(range(336, 343)), (316, 320, 321, 322, 323, 324), (323, *range(330, 336)),
          (291, *range(295, 303)))
CONTEXT = (
    "Follow Rafael's testing and training through the knife, both levels of instruction, the village handover and the account of the monk's medicine.",
    "Follow Hodram's fog and tree branches, the sextant exchange, the two survey funding outcomes and the village's account of the monk.",
    "Follow Lil's fog decision, the warrior legend, the sextant exchange, the alternate survey funds and the villager's account.",
    "Follow Maria through the fog, the ghost-ship assignment, the warrior legend, the Guam return and the encounters with the Proof guardian and the villager.",
)

if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
