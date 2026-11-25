"""Cold boot and replay the original Market navigation on the two ROMs."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_kurushima_encounter_20261115 as startup_workflow
from scripts import replay_market_conversation_20261115 as market
from scripts import stage_market_economy_dialogue_20261115 as stage


def schedule(case):
    events, frames, end, path, donor = market.schedule(case)
    return events, tuple(sorted(set(frames) | {8400, 8750, 9150, 9500})), end, path, donor


def replay(case):
    target = stage.parent if case == 'market_parent' else SimpleNamespace(ROM=stage.ROM, RELEASE=stage.STORED)
    scope = vars(market.playback) | dict(ROOT=stage.ROOT, parent=target, observer=market.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(market.playback.main), __file__ + '::market-navigation', 'exec'), scope)
    scope['main'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('market_parent', 'market_staged', 'startup'))
    mode = parser.parse_args().mode
    if mode == 'startup':
        FunctionType(startup_workflow.startup.__code__, vars(startup_workflow) | {'stage': stage})()
    else:
        replay(mode)
