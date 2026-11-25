"""Bind all four complete Hamburg ceramics scenes to clean Japanese and current English."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_damaged_save_digits_20261120 as parent


ROOT = Path("work/hamburg_ceramics_cross_route_20261120")
SOURCE = ROOT / "paired_source.json"
BLOCKS = ((201,), (193,), (189,), (162,))
CONTEXT = ("A Hamburg shopkeeper recognizes the ceramics and asks to see them. A collecting craze has made good pieces hard to find. The rest of the scene carries the observation into the town trend forecast.",) * 4


if __name__ == "__main__":
    FunctionType(paired.main.__code__, vars(paired) | globals())()
