"""Pair eleven story blocks containing the newly found phrase breaks."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_market_followup_20261119 as parent


base, native, stage = paired.base, paired.native, paired.stage
ROOT = Path("work/story_short_phrase_wraps_20261119")
SOURCE = ROOT / "paired_source.json"
BLOCKS = ((60, 62, 87, 127, 226, 282), (49, 78), (26,), (106, 126))
CONTEXT = (
    "Rafael's requests for help, replies to a new lead and trouble, the Ceuta sailing lesson, a debate about trust and the bounty on Plett.",
    "Hodram's treasure lead and the confrontation with Escante.",
    "Lil's appeal for a conversation and the later warning about the New World.",
    "Maria's East Asia explanation and the later identification of the New World map.",
)


if __name__ == "__main__":
    FunctionType(paired.main.__code__, vars(paired) | globals())()
