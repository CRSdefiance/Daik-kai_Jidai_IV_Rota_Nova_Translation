"""Replay the final diplomatic portraits through the established letter and boot fixtures."""

import inspect
from types import FunctionType

from scripts import replay_diplomatic_letter_portraits_v1 as previous
from scripts import stage_diplomatic_letter_portraits_v2 as stage
from scripts.source_locked_derivation_v5118 import checked_text


ROOT, ROM, EVIDENCE = stage.ROOT, stage.ROM, stage.PROOF
STARTUP = ROOT / 'own_startup'
ACTION = previous.ACTION
set_condition = FunctionType(previous.set_condition.__code__, vars(previous) | {'ROM': ROM})


def main():
    source = checked_text(inspect.getsource(previous.main), {
        "from scripts.replay_diplomatic_letter_portraits_v1 import set_condition":
            "from scripts.replay_diplomatic_letter_portraits_v2 import set_condition",
    })
    env = vars(previous) | globals()
    exec(compile(source, __file__ + '::same-outgoing-submission-fixture', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    import sys
    if sys.argv[1:] == ['--cold-boot']:
        FunctionType(previous.cold_boot.__code__, vars(previous) | globals())()
    else:
        main()

