"""Observe the Lisbon rat incident and additional town dialogue on the registered ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_embedded_story_roles_20261115 as current
from scripts.observe_regional_town_dialogue_20261115 import VISITS
from scripts.observe_setup_save_common_v1 import scoped_observer


base = current.base
ROOT = Path('work/lisbon_voyage_and_osaka_20261115_v1')
HISTORY = {
    'voyage': 'weapon_voyage_v470',
    'lisbon': 'lisbon_reload_v470',
    'osaka': 'osaka_v519',
}


def schedule(case):
    source = Path('work/emulation_v193') / HISTORY[case] / 'capture_report.json'
    old = base.load(source)
    assert old['cold_boot'] and not old['savestate_loaded'] and not old['callback_errors']
    donor = old['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    limit = {'voyage': 15000, 'lisbon': 2801, 'osaka': 7799}[case]
    events = [row for row in old['scripted_input_schedule'] if row['start'] <= limit]
    if case == 'lisbon':
        for frame, action in VISITS:
            fields = (dict(touch=list(action), buttons=[]) if isinstance(action, tuple) else dict(buttons=[action]))
            events.append(dict(start=frame, duration=8, **fields))
        frames, end = [3200, 3720, *(frame + 149 for frame, _ in VISITS)], 11700
    else:
        end = limit + 101
        shots = {f['frame'] for f in old['frames_captured'] if 3200 <= f['frame'] < end}
        if case == 'voyage':
            shots.update(range(3880, 4080, 20))
        frames = sorted(shots)
    return events, frames, end, source, donor


def main(case):
    env = vars(playback) | dict(ROOT=ROOT, parent=current, observer=scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::ordinary-controller-and-common-observation', 'exec'), env)
    env['main'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=HISTORY)
    main(parser.parse_args().case)
