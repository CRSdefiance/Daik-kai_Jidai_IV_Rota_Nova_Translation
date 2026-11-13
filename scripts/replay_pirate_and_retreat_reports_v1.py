"""Replay the verified Hamburg orders and the current ROM's own startup."""

from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType

from scripts import replay_city_combat_notices_v1 as prior
from scripts import stage_pirate_and_retreat_reports_v2 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = prior.base
STARTUP = stage.ROOT / 'own_startup'
ROOT = stage.ROOT / 'hamburg_retreat_replay'


def cold_boot():
    runner = prior.startup
    env = vars(runner) | dict(EVIDENCE=stage.PROOF, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=prior.STARTUP)
    FunctionType(runner.main.__code__, env)()


def gameplay():
    terminal = base.load(prior.ROOT / 'terminal.json')
    old_commands = Path(terminal['commands'])
    assert terminal['unchanged_original_save'] and base.digest(old_commands) == terminal['commands_sha256']
    source = checked_text(getsource(prior.gameplay), {
        "commands.write_text(''.join(dumps(row) + '\\n' for row in ATTACK_MENU), encoding='utf-8')":
            'commands.write_bytes(old_commands.read_bytes())',
    })
    env = vars(prior) | dict(stage=stage, ROOT=ROOT, old_commands=old_commands)
    exec(compile(source, __file__ + '::original-hamburg-inputs', 'exec'), env)
    env['gameplay']()
    assert base.digest(ROOT / 'commands.jsonl') == terminal['commands_sha256']


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
