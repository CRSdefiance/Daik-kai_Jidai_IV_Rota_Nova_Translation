"""Verify the original village menu after the consumed Resupply entry disappears."""

import inspect

from scripts import verify_sea_approach_village_release_inputs_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


if __name__ == '__main__':
    source = checked_text(inspect.getsource(previous.verify_live), {
        "(8000, 'Resupply', (78, 223, 181, 251))": "(8000, 'Stay', (78, 234, 181, 263))",
    })
    env = {**vars(previous), '__file__': __file__}
    exec(compile(source, __file__ + '::same-village-replay-and-updated-menu', 'exec'), env)
    env['verify_live']()
