"""Replay the original Lisbon Price Info navigation and cumulative startup controls."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
import sys

from scripts import observe_online_gallery_common_v1 as playback
from scripts import replay_price_info_wraps_20261115 as price
from scripts import replay_tavern_toast_startup_20261114 as boot
from scripts import stage_market_conversation_20261115 as stage
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.source_locked_derivation_v5118 import checked_text


base, ROOT = stage.base, stage.ROOT
FRAMES = (9600, 10200, 10690, 11000, 11490, 11880, 12180)


def schedule(_):
    events = [row for row in base.load(price.OLD_INPUTS) if row['start'] <= 11901]
    donor = base.load(price.DONOR_PLAN)['source_save']
    assert base.digest(donor['source']) == donor['source_sha256']
    return events, FRAMES, 12200, price.OLD_INPUTS, donor


def price_check(case):
    if case == 'price_parent':
        target = stage.parent
    else:
        target = SimpleNamespace(ROM=stage.ROM, RELEASE=stage.STORED)
    scope = vars(playback) | dict(ROOT=ROOT, parent=target, observer=scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::original-price-info-replay', 'exec'), scope)
    scope['main'](case)


def startup():
    release = base.load(stage.parent.RELEASE)
    prior = Path(base.load(release['own_registered_startup'])['read_only_snapshot']['path']).parent.parent
    original = checked_text(getsource(boot.main), {
        '    prior = stage.parent.stage.ROOT/"startup_retry"': '    prior = PRIOR_CAPTURE',
    })
    scope = vars(boot) | dict(stage=stage, PRIOR_CAPTURE=prior)
    exec(compile(original, __file__ + '::cumulative-startup', 'exec'), scope)
    scope['main']()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('price_parent', 'price_staged', 'startup'))
    case = parser.parse_args().case
    if case == 'startup':
        startup()
    else:
        price_check(case)
