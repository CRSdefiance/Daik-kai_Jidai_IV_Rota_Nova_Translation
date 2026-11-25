"""Trace the original CEvent record loads from two ordinary battery saves."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import observe_fleet_battery_fields_20261124 as saves
from scripts import register_lisbon_purser_refit_20261124 as current


ROOT = current.ROM.parent.with_name("editorial_20261124_saved_fleet_events")
READS = {0x02093C20 + i * 0x10: (f"event_byte_{i + 4}", 5, i + 4) for i in range(6)}
CALLS = {pc + size: (*field, bool(size)) for pc, field in READS.items() for size in (0, 4)}


def main(case):
    scope = vars(saves) | dict(ROOT=ROOT, CALLS=CALLS, current=current, __file__=__file__)
    scope["observe"] = FunctionType(saves.observe.__code__, scope)
    FunctionType(saves.main.__code__, scope)(case)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("copenhagen", "nagasaki"))
    main(parser.parse_args().case)
