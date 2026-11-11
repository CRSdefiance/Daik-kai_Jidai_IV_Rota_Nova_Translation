"""Replay the staged equipment chooser, result and removal through original inputs."""

import argparse
import inspect
from types import FunctionType

from scripts import observe_setup_save_common_v1 as observer
from scripts import replay_setup_save_equipment_v2 as baseline
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_captain_biographies_v2 import ROOT as BIOGRAPHIES
from scripts.stage_setup_save_equipment_v1 import PROOF, ROM, ROOT


def replay_plan(case):
    assert case == 'equipment'
    inputs, frames, _, donor = baseline.replay_plan(case)
    inputs += [{'start': n, 'duration': 8, 'buttons': [button]}
               for n, button in ((11201, 'A'), (11601, 'Y'), (12001, 'A'), (12401, 'B'))]
    return inputs, [*frames, 11600, 12000, 12400, 12800], 12810, donor


def replay():
    source = checked_text(inspect.getsource(observer.main), {
        'release = load(RELEASE)': 'release = load(PROOF)',
        "release['candidate']": "release['research_ROM']",
        "release['candidate_sha256']": "release['research_ROM_sha256']",
        "    inputs = [{'start': frame, 'duration': 8, 'buttons': [key]} for frame, key in SCHEDULE[case]]":
            '    inputs, frames, frame_count, donor = replay_plan(case)',
        '    frames = [event[\'start\'] + 199 for event in inputs]\n': '',
        'str(frames[-1] + 10)': 'str(frame_count)',
        '    installed = []':
            "    argv.extend(['--battery-save', donor['source'], '--touchscreen'])\n    installed = []",
        '    trace.save()': "    trace.save()\n    assert digest(donor['source']) == donor['source_sha256']",
        'battery_save_preloaded=False': 'battery_save_preloaded=True',
        'original_controller_only=True': 'original_controller_and_stylus_only=True',
    })
    env = {**vars(observer), **globals(), '__file__': __file__, '__name__': 'staged_equipment_replay'}
    exec(compile(source, __file__ + '::current-equipment-and-removal', 'exec'), env)
    env['main']('equipment')


def cold_boot():
    env = {**vars(startup), 'EVIDENCE': PROOF, 'ROM': ROM, 'STARTUP': ROOT / 'own_startup',
           'PRIOR': BIOGRAPHIES / 'own_startup'}
    FunctionType(startup.main.__code__, env)()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('equipment', 'startup'))
    (replay if parser.parse_args().case == 'equipment' else cold_boot)()
