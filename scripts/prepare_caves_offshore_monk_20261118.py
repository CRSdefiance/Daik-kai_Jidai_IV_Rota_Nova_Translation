"""Bind the cave, offshore ruins and missing monk exchanges to the registered parent."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_desert_censer_20261118 as parent


ROOT = Path("work/caves_offshore_monk_source_20261118")
BLOCKS = ((332, 333, 334, 335), (317, 318, 319), (324, 325, 326), (286, 292, 293, 294))
CONTEXT = (
    "Follow Rafael through the cliff and cave decisions, the small-boat crossing and the missing monk rumor.",
    "Follow Hodram through the cave, the guide's offshore route and the report about the missing monk.",
    "Follow Lil through the pitch-dark cave and the distinct python and bat branches, then the crossing and monk rumor.",
    "Compare the incense burner exchange on Maria's route with the other routes. Preserve the original reply selectors before reviewing Maria's cave choices, crossing and monk rumor.",
)

if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
