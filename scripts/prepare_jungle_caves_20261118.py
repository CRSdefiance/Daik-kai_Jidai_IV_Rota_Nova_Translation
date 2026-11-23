"""Pair the four jungle and cave sequences with the registered guild candidate."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_london_guild_assignments_20261118 as parent


ROOT = Path("work/jungle_caves_source_20261118")
BLOCKS = ((301,), (291,), (288,), (259,))
CONTEXT = (
    "Rafael's company crosses the jungle and follows the cave sequence to its escape.",
    "Hodram's company crosses the jungle and follows the cave sequence to its escape.",
    "Lil weighs going into the jungle before her company finds a way out of the cave.",
    "Maria's party begins in the humid jungle and follows the cave sequence to its exit.",
)


if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
