"""Trace original Rafael New Game edit controls and scoped COMMON requests."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_cristina_recruitment_name_20261115 as current
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path('work/rafael_character_setup_20261115_v2')
PRIOR = Path('work/analysis/confirm_consumers_v582/final_recorded_inputs.json')
CASES = {
    'birthday': ((2401, 'Y'), (2801, (137, 122)), (3201, 'A'), (3601, 'RIGHT'), (4001, 'DOWN'),
                 (4401, 'A'), (4801, 'X'), (5201, 'B')),
}


def schedule(case):
    events = base.load(PRIOR)[:4]
    assert [row['buttons'] for row in events] == [['START'], ['A'], ['A'], ['B']]
    events += [dict(start=frame, duration=8, buttons=[key]) if isinstance(key, str)
               else dict(start=frame, duration=8, buttons=[], touch=list(key)) for frame, key in CASES[case]]
    frames = [1800, 2200, *(frame + 190 for frame, _ in CASES[case])]
    return events, frames, frames[-1] + 10, PRIOR, None


def main(case):
    implementation = checked_text(getsource(playback.main), {
        '    installed = []': "    if any('touch' in event for event in events) and not donor:\n        argv += ['--touchscreen']\n    installed = []",
    })
    namespace = vars(playback) | dict(
        ROOT=ROOT, parent=current, observer=trace.scoped_observer, get_schedule=schedule,
        FOCUS={*range(100, 108), *range(120, 122)}, __file__=__file__)
    exec(compile(implementation, __file__ + '::native-character-setup', 'exec'), namespace)
    namespace['main'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=CASES)
    main(parser.parse_args().case)
