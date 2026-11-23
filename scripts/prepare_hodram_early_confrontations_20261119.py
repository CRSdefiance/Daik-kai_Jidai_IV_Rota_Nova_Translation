"""Pair Hodram's first major confrontations with the registered story blocks."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_naturalist_aliases_and_shield_20261119 as parent

base, native, stage = paired.base, paired.native, paired.stage
ROOT = Path("work/hodram_early_confrontations_20261119")
SOURCE = ROOT / "paired_source.json"
BLOCKS = ((), (28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40), (), ())
CONTEXT = (
    "",
    "Hodram and his crew confront rivals and enter battles around the world. Follow the order of each challenge, "
    "the supporting voices and the changes in resolve before the scene moves to combat.",
    "",
    "",
)


if __name__ == "__main__":
    FunctionType(paired.main.__code__, vars(paired) | globals())()
