"""Observe the two native save reads for the separate town-trend object."""

from types import FunctionType

from scripts import observe_fleet_battery_fields_20261124 as fields
from scripts import observe_riga_port_trend_20261124 as earlier

ROOT = earlier.ROOT.with_name("editorial_20261124_riga_port_trend_restore")
READS = {0x0202C0D8: ("trend_town", 5, 4), 0x0202C0E8: ("trend_good", 5, 5)}
CALLS = {pc + step: (*record, bool(step)) for pc, record in READS.items() for step in (0, 4)}


def schedule(case):
    events, _, _, history, donor = earlier.schedule(case)
    return [event for event in events if event["start"] < 3200], (3200,), 3201, history, donor


if __name__ == "__main__":
    scope = vars(fields) | dict(ROOT=ROOT, CALLS=CALLS, current=earlier.current, schedule=schedule, __file__=__file__)
    scope["observe"] = FunctionType(fields.observe.__code__, scope)
    FunctionType(fields.main.__code__, scope)("riga")
