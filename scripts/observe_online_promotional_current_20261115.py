"""Trace the current DS's complete Online guide and About Extras page sequences."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_extras_tie_in_common_20261114 as extras
from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_square_rumors_20261115 as current


ROOT = Path('work/online_promotional_current_20261115_v1')
FOCUS = set(range(3289, 3320))


def main(case):
    options = dict(ROOT=ROOT, parent=current, FOCUS=FOCUS, __file__=__file__)
    if case == 'tie_in_advance':
        options.update(get_schedule=extras.schedule, observer=extras.trace.scoped_observer)
    scope = vars(playback) | options
    exec(compile(getsource(playback.main), __file__ + '::registered-menu-trace', 'exec'), scope)
    scope['main'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('online', 'tie_in_advance'))
    main(parser.parse_args().case)
