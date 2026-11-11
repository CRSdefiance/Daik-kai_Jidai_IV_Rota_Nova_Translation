"""Dismiss the original Baby Shark item card before checking inventory and sailing."""

import inspect
from pathlib import Path

from scripts import replay_shark_encounter_v1 as replay_base
from scripts import replay_shark_encounter_v2 as initialized
from scripts import replay_shark_encounter_v3 as selected
from scripts.source_locked_derivation_v5118 import checked_text


OUT = Path('out/shark_encounter_replay_20261111_v4')
RESTORE, FINAL = 13827, 14027


def commands():
    steps = selected.commands()
    assert steps[-2]['condition_fixture'] == {'mode': 'restore-return-and-roster'}
    assert steps[-2]['until'] == RESTORE
    steps.insert(-2, dict(until=RESTORE, buttons=['B'], duration=8))
    steps[-2]['until'] = FINAL
    return steps


def main():
    source = checked_text(inspect.getsource(replay_base.replay), {
        'out = stage.ROOT / choice': 'out = OUT / choice\n    out.parent.mkdir(exist_ok=True)',
    })
    env = vars(replay_base) | {'OUT': OUT, 'FINAL': FINAL, 'fixture_controller': initialized.fixture_controller,
                              'commands': lambda choice: commands()}
    exec(compile(source, __file__ + '::same-raise-selection-and-item-card-dismissal', 'exec'), env)
    env['replay']('raise')


if __name__ == '__main__':
    main()
