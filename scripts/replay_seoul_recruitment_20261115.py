"""Follow Yifa's recruitment through its original Seoul Square entrance."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_regional_town_dialogue_20261115 as town


base, parent = town.base, town.current
ROOT = Path('work/seoul_recruitment_20261115_v1')


def schedule(_):
    events, frames, _, source, donor = town.schedule('seoul')
    next_actions = range(11801, 21100, 320)
    events += [dict(start=n, duration=8, buttons=['A']) for n in next_actions]
    frames += [n + 238 for n in next_actions]
    return events, frames, frames[-1] + 36, source, donor


def main(case, rom, receipt):
    target = SimpleNamespace(ROM=rom, RELEASE=receipt)
    assert base.digest(rom) == base.load(receipt)['candidate_sha256']
    env = vars(playback) | dict(ROOT=ROOT, parent=target, observer=town.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::original-Seoul-Square', 'exec'), env)
    env['main'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('parent', 'staged'))
    parser.add_argument('--rom', type=Path, default=parent.ROM)
    parser.add_argument('--receipt', type=Path, default=parent.RELEASE)
    args = parser.parse_args()
    main(args.case, args.rom, args.receipt)
