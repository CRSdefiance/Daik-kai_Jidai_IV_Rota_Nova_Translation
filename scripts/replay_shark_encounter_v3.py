"""Select Raise It explicitly with the original two-choice cursor."""

import inspect
from pathlib import Path

from scripts import replay_shark_encounter_v1 as replay_base
from scripts import replay_shark_encounter_v2 as initialized
from scripts.source_locked_derivation_v5118 import checked_text


OUT = Path('out/shark_encounter_replay_20261111_v3')


def commands():
    steps = replay_base.commands('raise')
    index = next(i for i, step in enumerate(steps) if step.get('until') == replay_base.MENU_CONFIRM)
    assert steps[index]['buttons'] == ['UP']
    steps.insert(index, dict(until=12327, buttons=['UP'], duration=8))
    return steps


def main():
    source = checked_text(inspect.getsource(replay_base.replay), {
        'out = stage.ROOT / choice': 'out = OUT / choice\n    out.parent.mkdir(exist_ok=True)',
    })
    env = vars(replay_base) | {'OUT': OUT, 'fixture_controller': initialized.fixture_controller,
                              'commands': lambda choice: commands()}
    exec(compile(source, __file__ + '::same-source-fixture-and-raised-selection', 'exec'), env)
    env['replay']('raise')


if __name__ == '__main__':
    main()
