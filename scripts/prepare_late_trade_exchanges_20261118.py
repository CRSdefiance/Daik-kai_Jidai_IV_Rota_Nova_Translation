"""Pair the remaining late Lil and Maria trade exchanges to the registered candidate."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_warrior_village_handovers_20261118 as parent

ROOT = Path("work/late_trade_exchanges_source_20261118")
BLOCKS = ((), (), (319, 327, 328, 329), (287, 288, 289, 290))
CONTEXT = (
    "", "",
    "Follow the gold and ivory discussion, the three branches about Espinosa, the Genoa tomato launch and its conditions, the payment and the return to Havana.",
    "Follow the organized bandit attacks, the armor, guns and cannons ordered from Maria, reimbursement and the lead about the hideout in the Sahara.",
)

if __name__ == "__main__":
    bind = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    bind()
