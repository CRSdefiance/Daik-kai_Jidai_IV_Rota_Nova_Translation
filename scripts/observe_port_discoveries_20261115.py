"""Replay normal Genoa departure, Tunis discovery and Syracuse docking."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_london_stockholm_dialogue_20261115 as current


base = current.base
ROOT = Path('work/port_discoveries_20261115_v1')
PRIOR = Path('work/emulation_v193/weapon_voyage_v476/capture_report.json')
FRAMES = (6000, 6250, 6290, 6350, 6390, 6575, 7410, 7455, 7510, 7555, 7660, 7695, 7800, 8095)


def schedule(_):
    report = base.load(PRIOR)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert all(not v for k, v in report.items() if k.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    return [row for row in report['scripted_input_schedule'] if row['start'] <= 7696], FRAMES, 8100, PRIOR, donor


def main():
    env = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)), get_schedule=schedule,
                               observer=trace.scoped_observer, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + '::original-sailing-inputs', 'exec'), env)
    env['main']('ports')


if __name__ == '__main__':
    main()
