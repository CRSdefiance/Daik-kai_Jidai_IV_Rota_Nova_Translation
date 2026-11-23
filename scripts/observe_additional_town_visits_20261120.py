"""Capture ordinary saved-game Square and Tavern visits on the Sailing Help ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_sailing_help_20261120 as head
from scripts.observe_regional_town_dialogue_20261115 import VISITS
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.source_locked_derivation_v5118 import checked_text


base = head.base
ROOT = Path('work/additional_town_visits_20261120')
HISTORY = {
    'genoa': ('genoa_repaired_reload_v473', 2801),
    'tripoli': ('environment_voyage_v510_tripoli_reload', 3401),
    'copenhagen': ('copenhagen_saved_reload_v420', 2801),
    'riga': ('riga_reload_v398', 3201),
}


def schedule(city):
    folder, load_until = HISTORY[city]
    path = Path('work/emulation_v193') / folder / 'capture_report.json'
    previous = base.load(path)
    assert previous['cold_boot'] and not previous['savestate_loaded'] and not previous['callback_errors']
    donor = previous['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    events = [row for row in previous['scripted_input_schedule'] if row['start'] <= load_until]
    for frame, action in VISITS:
        fields = dict(touch=list(action), buttons=[]) if isinstance(action, tuple) else dict(buttons=[action])
        events.append(dict(start=frame, duration=8, **fields))
    captures = [3720, *(frame + 149 for frame, _ in VISITS)]
    return events, captures, 11700, path, donor


def main(city):
    assert not (ROOT / city).exists()
    source = checked_text(getsource(playback.main), {
        "    installed = []": "    argv.append('--dump-capture-ram')\n    installed = []",
    })
    scope = vars(playback) | dict(ROOT=ROOT, parent=head, observer=scoped_observer,
                                  get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(source, __file__ + '::additional-town-observation', 'exec'), scope)
    scope['main'](city)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('city', choices=HISTORY)
    main(parser.parse_args().city)
