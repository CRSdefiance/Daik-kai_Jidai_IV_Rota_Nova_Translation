"""Bind every remaining story occurrence of 'trade house' to complete exchanges."""
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_help_market_terms_20261119 as parent

ROOT = Path("work/story_market_terms_20261119_v1")
BLOCKS = ((65, 66, 137, 170), (296,), (), (130,))
CONTEXT = (
    "Rafael and Charlotte consider a new village trading post, with separate story transactions in later ports. Resolve each setting from its complete exchange.",
    "An expedition needs a purchase from the original town facility. Keep the directions and the rest of the exchange intact.",
    "",
    "Carlo follows up on a delayed deal. Review the invitation and what he tentatively offers against the rest of the exchange.",
)

if __name__ == "__main__":
    scope = vars(pairing) | dict(parent=parent, ROOT=ROOT, BLOCKS=BLOCKS, CONTEXT=CONTEXT)
    FunctionType(pairing.main.__code__, scope)()
