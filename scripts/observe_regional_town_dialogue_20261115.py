"""Capture Square and Tavern dialogue from ordinary visits in regional town saves."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_market_conversation_20261115 as current
from scripts.observe_setup_save_common_v1 import scoped_observer


base = current.base
ROOT = Path('work/regional_town_review_20261115_v1')
HISTORY = {
    'seoul': 'barmaid_v780_seoul_baseline',
    'tunis': 'environment_voyage_v511_tunis_reload',
    'valencia': 'valencia_reload_v471',
    'syracuse': 'syracuse_ships_reload_v476',
}
VISITS = (
    (3801, (180, 29)), (4201, 'A'), (4601, 'A'), (5001, 'A'), (5401, 'A'),
    (5801, (130, 58)), (6201, 'A'), (6601, 'A'), (7001, 'A'),
    (7401, (130, 90)), (7801, 'A'), (8201, 'A'), (8601, 'A'),
    (9001, 'B'), (9401, 'B'), (9801, (80, 29)), (10201, 'A'),
    (10601, 'A'), (11001, 'B'), (11401, 'B'),
)


def schedule(city):
    path = Path('work/emulation_v193') / HISTORY[city] / 'capture_report.json'
    previous = base.load(path)
    assert previous['cold_boot'] and not previous['savestate_loaded'] and not previous['callback_errors']
    donor = previous['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    limit = 3401 if city == 'tunis' else 2801
    events = [row for row in previous['scripted_input_schedule'] if row['start'] <= limit]
    for frame, action in VISITS:
        fields = (dict(touch=list(action), buttons=[]) if isinstance(action, tuple) else dict(buttons=[action]))
        events.append(dict(start=frame, duration=8, **fields))
    captures = [3200, 3720, *(frame + 149 for frame, _ in VISITS)]
    return events, captures, 11700, path, donor


def main(city):
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, observer=scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::regional-town-observation', 'exec'), scope)
    scope['main'](city)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('city', choices=HISTORY)
    main(parser.parse_args().city)
