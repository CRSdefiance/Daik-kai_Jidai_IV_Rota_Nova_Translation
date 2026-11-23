"""Replay the Tunis trend dialogue and cumulative startup from ordinary input."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_regional_town_dialogue_20261115 as regional
from scripts import replay_tavern_toast_startup_20261114 as boot
from scripts import stage_square_trend_dialogue_20261115 as stage
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.source_locked_derivation_v5118 import checked_text


def tunis():
    target = SimpleNamespace(ROM=stage.ROM, RELEASE=stage.STORED)
    scope = vars(playback) | dict(ROOT=stage.ROOT, parent=target, observer=scoped_observer,
                                  get_schedule=regional.schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::original-tunis-square-replay', 'exec'), scope)
    scope['main']('tunis')


def startup():
    release = stage.base.load(stage.parent.RELEASE)
    prior = Path(stage.base.load(release['own_registered_startup'])['read_only_snapshot']['path']).parent.parent
    source = checked_text(getsource(boot.main), {
        '    prior = stage.parent.stage.ROOT/"startup_retry"': '    prior = PRIOR_CAPTURE',
    })
    scope = vars(boot) | dict(stage=stage, PRIOR_CAPTURE=prior)
    exec(compile(source, __file__ + '::cumulative-startup', 'exec'), scope)
    scope['main']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('tunis', 'startup'))
    {'tunis': tunis, 'startup': startup}[parser.parse_args().case]()
