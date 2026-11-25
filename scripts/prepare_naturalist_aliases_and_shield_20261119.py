"""Pair the naturalist introductions, Camille's reveal and the shared shield rumor."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_story_short_phrase_wraps_20261119 as parent


base, native, stage = paired.base, paired.native, paired.stage
ROOT = Path("work/naturalist_aliases_and_shield_20261119")
SOURCE = ROOT / "paired_source.json"
BLOCKS = ((48, 240), (231,), (65, 169, 228), (201,))
CONTEXT = (
    "Hans introduces himself and can join Rafael. In the later rumor, the crew compares an animal's armor to a shield.",
    "Hodram hears the crew compare an animal's armor to a shield.",
    "Lil learns Camille's birth name. Elsewhere she addresses the naturalist by an alternate given name, and her crew shares the shield rumor.",
    "Maria hears the crew compare an animal's armor to a shield.",
)


if __name__ == "__main__":
    FunctionType(paired.main.__code__, vars(paired) | globals())()
