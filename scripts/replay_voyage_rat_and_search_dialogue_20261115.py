"""Replay the revised reports with the original voyage inputs and save."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import observe_lisbon_voyage_and_osaka_20261115 as observation
from scripts import replay_embedded_story_roles_20261115 as boot
from scripts import stage_voyage_rat_and_search_dialogue_20261115 as stage


def gameplay():
    parent = SimpleNamespace(ROM=stage.ROM, RELEASE=stage.STORED)
    env = vars(observation.playback) | dict(ROOT=stage.ROOT, parent=parent,
        observer=observation.scoped_observer, get_schedule=observation.schedule,
        FOCUS=set(range(3668)), __file__=__file__)
    source = getsource(observation.playback.main)
    exec(compile(source, __file__ + '::original-voyage-observation', 'exec'), env)
    env['main']('voyage')


def startup():
    FunctionType(boot.startup.__code__, vars(boot) | dict(stage=stage))()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('gameplay', 'startup'))
    {'gameplay': gameplay, 'startup': startup}[parser.parse_args().mode]()
