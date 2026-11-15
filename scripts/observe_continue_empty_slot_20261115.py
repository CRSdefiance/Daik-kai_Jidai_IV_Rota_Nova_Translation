"""Trace real empty-slot and populated-slot selections in the DS Continue screen."""

from inspect import getsource
from pathlib import Path

from scripts import observe_gallery_empty_common_20261114 as historical
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_price_info_wraps_20261115 as current


base = current.base
ROOT = Path('work/continue_empty_slot_20261115_v1')
FOCUS = set(range(98, 125))
KEYS = (
    (1601, 'START'), (2001, 'A'), (2401, 'DOWN'), (2801, 'A'),
    (3201, 'DOWN'), (3601, 'A'), (4001, 'UP'), (4401, 'UP'),
    (4801, 'A'), (5201, 'B'), (5601, 'B'),
)


def schedule(case):
    assert case == 'continue'
    assert base.load(historical.OWNER)['normal_new_save_enables_title_Gallery_without_unlock_patch']
    donor = dict(source=str(historical.DONOR), source_sha256=base.digest(historical.DONOR))
    events = [dict(start=frame, duration=8, buttons=[key]) for frame, key in KEYS]
    return events, [frame + 199 for frame, _ in KEYS], 5850, historical.HISTORY, donor


def main():
    env = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS=FOCUS, observer=trace.scoped_observer,
        get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::continue-observation', 'exec'), env)
    env['main']('continue')


if __name__ == '__main__':
    main()
