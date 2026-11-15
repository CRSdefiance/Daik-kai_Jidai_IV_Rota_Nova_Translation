"""Trace original Shipyard and fleet menus from isolated copies of existing saves."""

import argparse
import inspect
from pathlib import Path
from types import FunctionType

from scripts import observe_setup_save_common_v1 as observer
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts.register_setup_save_equipment_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_setup_save_equipment_v1 import ROOT as EQUIPMENT


ROOT = Path('out/shipyard_fleet_setup_20261111_v1')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
REFERENCES = {
    'yard': CAP / 'regional_fleet_v615_stockholm/capture_report.json',
    'fleet': CAP / 'shipyard_ui_v615_actual/capture_report.json',
}
FOCUS = set(range(261, 287))


def replay_plan(case):
    report = observer.load(REFERENCES[case])
    donor = report['battery_save_preloaded']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert observer.digest(donor['source']) == donor['source_sha256']
    source = report['scripted_input_schedule']
    if case == 'yard':
        inputs = [event for event in source if event['start'] < 8600]
        return inputs, list(range(3400, 8601, 400)), 8610, donor
    inputs = [event for event in source if event['start'] < 3500]
    inputs.append(dict(start=3801, duration=8, buttons=[], touch=[155, 122]))
    return inputs, [3400, 3800, 4200], 12000, donor


def replay(case, staged=False):
    replacements = {
        "    inputs = [{'start': frame, 'duration': 8, 'buttons': [key]} for frame, key in SCHEDULE[case]]":
            '    inputs, frames, frame_count, donor = replay_plan(case)',
        "    frames = [event['start'] + 199 for event in inputs]\n": '',
        "str(frames[-1] + 10)": 'str(frame_count)',
        '    installed = []':
            "    argv.extend(['--battery-save', donor['source'], '--touchscreen'])\n"
            "    if case == 'fleet':\n        argv.extend(['--pause-at', '4200', '--dump-pause-ram'])\n"
            '    installed = []',
        '    trace.save()': "    trace.save()\n    assert digest(donor['source']) == donor['source_sha256']",
        'battery_save_preloaded=False': 'battery_save_preloaded=True',
        'original_controller_only=True': 'original_controller_and_stylus_only=True',
    }
    env = {**vars(observer), **globals(), '__file__': __file__, '__name__': 'shipyard_fleet_replay'}
    if staged:
        from scripts.stage_shipyard_fleet_setup_v1 import PROOF, ROOT as STAGED_ROOT
        env.update(RELEASE=PROOF, ROOT=STAGED_ROOT)
        replacements.update({"release['candidate']": "release['research_ROM']",
                             "release['candidate_sha256']": "release['research_ROM_sha256']"})
    source = checked_text(inspect.getsource(observer.main), replacements)
    exec(compile(source, __file__ + '::same-read-only-COMMON-trace', 'exec'), env)
    env['main'](case)


def cold_boot():
    from scripts.stage_shipyard_fleet_setup_v1 import PROOF, ROM, ROOT as STAGED_ROOT

    env = {**vars(startup), 'EVIDENCE': PROOF, 'ROM': ROM, 'STARTUP': STAGED_ROOT / 'own_startup',
           'PRIOR': EQUIPMENT / 'own_startup'}
    FunctionType(startup.main.__code__, env)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('yard', 'fleet', 'startup'))
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    if args.case == 'startup':
        cold_boot()
    else:
        replay(args.case, args.staged)
