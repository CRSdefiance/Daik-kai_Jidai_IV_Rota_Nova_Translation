"""Keep the payout amount legible in its original speakerless notice."""

from types import FunctionType

from scripts import review_golden_route_exchanges_v1 as original
from scripts import review_golden_route_exchanges_v2 as previous


OUTPUT = previous.OUTPUT.with_name('golden_route_exchanges_context_v3.json')
DECISIONS = previous.DECISIONS | {
    3392: ('For finding a Golden Route, the guild awarded you %s gold.',
           'State the reason, the source and the exact amount. The original speakerless notice can give the reward its own row.'),
}


if __name__ == '__main__':
    environment = vars(original) | dict(OUTPUT=OUTPUT, DECISIONS=DECISIONS)
    FunctionType(original.main.__code__, environment)()
