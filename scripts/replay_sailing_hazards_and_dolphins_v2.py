"""Verify the final candidate against the proven native dolphin replay inputs."""

from inspect import getsource
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_sailing_hazards_and_dolphins_v1 as prior
from scripts import stage_sailing_hazards_and_dolphins_v2 as candidate
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(prior.stage) | dict(ROOT=candidate.ROOT, ROM=candidate.ROM, PROOF=candidate.PROOF)))
STARTUP = stage.ROOT / 'own_startup'
DOLPHINS = stage.ROOT / 'dolphin_log'
base = stage.base
set_condition = FunctionType(prior.set_condition.__code__, vars(prior) | {'stage': stage})
cold_boot = FunctionType(prior.cold_boot.__code__, vars(prior) | dict(stage=stage, STARTUP=STARTUP))


def gameplay():
    terminal = base.load(prior.DOLPHINS / 'terminal.json')
    report = base.load(terminal['report'])
    assert base.digest(terminal['report']) == terminal['report_sha256'] and report['frames'] == prior.END
    assert base.digest(terminal['commands']) == terminal['commands_sha256']
    source = checked_text(getsource(prior.gameplay), {
        'from scripts.replay_sailing_hazards_and_dolphins_v1 import set_condition':
            'from scripts.replay_sailing_hazards_and_dolphins_v2 import set_condition',
    })
    environment = vars(prior) | dict(stage=stage, DOLPHINS=DOLPHINS, __file__=__file__)
    exec(compile(source, __file__ + '::final-dolphin-replay', 'exec'), environment)
    environment['gameplay']()


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
