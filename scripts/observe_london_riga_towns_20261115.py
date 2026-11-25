"""Repeat ordinary London and Riga town choices on the cumulative candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_rafael_setup_labels_20261115 as current
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path('work/london_riga_town_coverage_20261115_v1')
HISTORY = {
    'london': 'condition_rumor_v774_london_pilot_v773',
    'riga': 'tavern_clues_v403',
}


def schedule(city):
    prior = Path('work/emulation_v193') / HISTORY[city] / 'capture_report.json'
    old = base.load(prior)
    assert old['cold_boot'] and not old['savestate_loaded'] and not old['callback_errors']
    assert not any(v for k, v in old.items() if k.startswith('synthetic_'))
    donor = old['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    inputs = old['scripted_input_schedule']
    end = old['frames']
    frames = [n for row in inputs if row['start'] >= 2801
              for n in (row['start'] + 120, row['start'] + 250) if n < end]
    return inputs, frames, end, prior, donor


def main(city):
    source = checked_text(getsource(playback.main), {
        '    target = [request for request in trace.requests if request[\'message_ID\'] in FOCUS]':
            '    target = trace.requests',
    })
    env = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=schedule,
        observer=trace.scoped_observer, __file__=__file__)
    exec(compile(source, __file__ + '::ordinary-town-input-only', 'exec'), env)
    env['main'](city)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('city', choices=HISTORY)
    main(parser.parse_args().city)
