"""Verify the phrase-safe Shipyard and fleet setup candidate with sealed inputs."""

import argparse
import inspect
from types import FunctionType

from scripts import replay_shipyard_fleet_setup_v1 as baseline
from scripts import stage_shipyard_fleet_setup_v2 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def replay_plan(case):
    inputs, frames, duration, donor = baseline.replay_plan(case)
    if case == 'yard':
        return inputs, frames, duration, donor
    source = baseline.ROOT / 'fleet'
    history = baseline.observer.load(source / 'capture/capture_report.json')
    journal = baseline.observer.load(source / 'capture/navigation_command_journal.json')
    assert journal['ROM_sha256'] == history['ROM_sha256']
    terminal = baseline.observer.load(source / 'terminal.json')
    assert terminal['candidate_sha256'] == history['ROM_sha256']
    assert all(baseline.observer.digest(path) == sha for path, sha in terminal['evidence'].items())
    for row in journal['commands_received']:
        command = row['command']
        if row['validation_passed'] and (command.get('buttons') or command.get('touch')):
            event = dict(start=row['frame'] + 1, duration=command.get('duration', 12),
                         buttons=command.get('buttons', []))
            if command.get('touch'):
                event['touch'] = command['touch']
            inputs.append(event)
    frames = sorted({row['frame'] for row in history['frames_captured'] if row['frame'] <= history['frames']})
    return inputs, frames, history['frames'], donor


def replay(case):
    source = checked_text(inspect.getsource(baseline.replay), {
        "    env = {**vars(observer), **globals(), '__file__': __file__, '__name__': 'shipyard_fleet_replay'}":
            "    env = {**vars(observer), **globals(), '__file__': __file__, '__name__': 'shipyard_fleet_replay_v2'}",
        'from scripts.stage_shipyard_fleet_setup_v1 import PROOF, ROOT as STAGED_ROOT':
            'from scripts.stage_shipyard_fleet_setup_v2 import PROOF, ROOT as STAGED_ROOT',
        r'''            "    if case == 'fleet':\n        argv.extend(['--pause-at', '4200', '--dump-pause-ram'])\n"''' + '\n': '',
    })
    env = {**vars(baseline), 'replay_plan': replay_plan, '__file__': __file__}
    exec(compile(source, __file__ + '::sealed-controller-and-stylus-replay', 'exec'), env)
    env['replay'](case, staged=True)


def cold_boot():
    startup = baseline.startup
    env = {**vars(startup), 'EVIDENCE': stage.PROOF, 'ROM': stage.ROM, 'STARTUP': stage.ROOT / 'own_startup',
           'PRIOR': baseline.EQUIPMENT / 'own_startup'}
    FunctionType(startup.main.__code__, env)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('yard', 'fleet', 'startup'))
    args = parser.parse_args()
    cold_boot() if args.case == 'startup' else replay(args.case)
