"""Reach each revised Tavern Help page and verify both linked returns."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import register_recruit_crew_20261120 as parent
from scripts import replay_palace_help_20261120 as earlier
from scripts import stage_tavern_help_20261120 as stage


ROOT = stage.ROOT
NAV = ROOT / 'navigation/navigation_plan.json'
CAPTURE = ROOT / 'gameplay'
LIVE = ROOT / 'gameplay_verification/ordinary_gameplay_verification.json'
ACTIONS = [dict(open=11), dict(open=12), dict(open=14), dict(open=15), dict(remember='Recruit Crew start'),
           dict(open=139), dict(key='L'), dict(return_to='Recruit Crew start'), dict(key='L'), dict(key='L'),
           dict(open=16), dict(remember='Schemes start')]
for topic in (17, 18, 19, 20):
    ACTIONS.extend([dict(open=topic), dict(key='L')])
ACTIONS.extend([dict(open=118), dict(open=16), dict(return_to='Schemes start')])

source = getsource(earlier.gameplay)
start, end = source.index('    actions = '), source.index('    base.save(itinerary, ')
source = source[:start] + '    actions = ACTIONS\n' + source[end:]
env = vars(earlier) | globals()
exec(compile(source, __file__ + '::replay-tavern-articles', 'exec'), env)
startup = FunctionType(earlier.startup.__code__, env)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('gameplay', 'startup'))
    if parser.parse_args().action == 'gameplay':
        env['gameplay']()
    else:
        startup()
