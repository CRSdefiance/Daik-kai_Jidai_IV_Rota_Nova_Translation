"""Exercise the fresh-save captain editor and the ordinary item-equip route."""

import argparse
import inspect
from pathlib import Path

from scripts import observe_setup_save_common_v1 as original
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = original.ROOT.with_name('setup_save_common_20261111_v2')
REFERENCE = Path('work/emulation_v193/equipment_long_v366/capture_report.json')
SETUP = [(1601, 'START'), (2001, 'A'), (2401, 'Y'), (2801, 'DOWN'),
         (3201, 'DOWN'), (3601, 'DOWN'), (4001, 'DOWN'), (4401, 'A'),
         (4801, 'RIGHT'), (5201, 'A'), (5601, 'B'), (6001, 'B'),
         (6401, 'A'), (6801, 'B')]


def replay_plan(case):
    if case == 'captain_editor':
        inputs = [{'start': n, 'duration': 8, 'buttons': [button]} for n, button in SETUP]
        return inputs, [n + 199 for n, _ in SETUP], 7010, None
    prior = original.load(REFERENCE)
    assert prior['cold_boot'] and not prior['savestate_loaded'] and not prior['callback_errors']
    donor = prior['battery_save_preloaded']
    assert original.digest(donor['source']) == donor['source_sha256']
    assert not any(value for key, value in prior.items() if key.startswith('synthetic_'))
    frames = sorted({row['frame'] for row in prior['frames_captured']})
    return prior['scripted_input_schedule'], frames, prior['frames'], donor


def main(case):
    source = checked_text(inspect.getsource(original.main), {
        "    inputs = [{'start': frame, 'duration': 8, 'buttons': [key]} for frame, key in SCHEDULE[case]]":
            '    inputs, frames, frame_count, donor = replay_plan(case)',
        "    frames = [event['start'] + 199 for event in inputs]\n": '',
        "str(frames[-1] + 10)": 'str(frame_count)',
        '    installed = []':
            "    if donor:\n        argv.extend(['--battery-save', donor['source'], '--touchscreen'])\n    installed = []",
        '    trace.save()': "    trace.save()\n    if donor:\n        assert digest(donor['source']) == donor['source_sha256']",
        'battery_save_preloaded=False': 'battery_save_preloaded=bool(donor)',
        'original_controller_only=True': 'original_controller_and_stylus_only=True',
    })
    env = {**vars(original), **globals(), '__file__': __file__, '__name__': 'current_setup_and_equipment'}
    exec(compile(source, __file__ + '::current-captain-editor-and-saved-equipment-route', 'exec'), env)
    env['main'](case)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('captain_editor', 'equipment'))
    main(parser.parse_args().case)
