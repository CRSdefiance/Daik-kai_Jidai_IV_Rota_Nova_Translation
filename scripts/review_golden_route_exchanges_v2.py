"""Refine the older officer’s explanation as a whole spoken paragraph."""

from types import FunctionType

from scripts import review_golden_route_exchanges_v1 as previous


OUTPUT = previous.OUTPUT.with_name('golden_route_exchanges_context_v2.json')
DECISIONS = previous.DECISIONS | {
    3347: ("I'm told the guild calls its most promising routes Golden Routes. They say it pays well for a report.",
           'Keep the measured hearsay, especially promising routes, and the substantial reward for reporting one.'),
}


if __name__ == '__main__':
    environment = vars(previous) | dict(OUTPUT=OUTPUT, DECISIONS=DECISIONS)
    FunctionType(previous.main.__code__, environment)()
