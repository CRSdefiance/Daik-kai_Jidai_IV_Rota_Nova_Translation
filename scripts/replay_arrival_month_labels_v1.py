"""Verify both label consumers with the established Lisbon inputs and cold boot."""

from inspect import getsource
from pathlib import Path
from shutil import copyfile
import sys
from types import FunctionType

from scripts import replay_golden_route_exchanges_v2 as prior
from scripts import stage_arrival_month_labels_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
STARTUP, SALE = stage.ROOT / 'own_startup', stage.ROOT / 'lisbon_sale_and_guild'
DISCOUNT = FunctionType(prior.discount_salt_purchase.__code__,
                        prior.discount_salt_purchase.__globals__ | {'stage': stage})


def cold_boot():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['research_ROM_sha256']
    binding = stage.ROOT / 'startup_input.json'
    assert not binding.exists()
    base.save(binding, proof | {'registered_input': {'candidate_sha256': proof['parent_sha256']}})
    startup = prior.prior.startup
    environment = vars(startup) | dict(EVIDENCE=binding, ROM=stage.ROM, STARTUP=STARTUP, PRIOR=prior.STARTUP)
    FunctionType(startup.main.__code__, environment)()


def discount_salt_purchase(arm, raw, cost):
    return DISCOUNT(arm, raw, cost)


def gameplay():
    terminal = base.load(prior.SALE / 'terminal.json')
    commands = Path(terminal['commands'])
    assert base.digest(commands) == terminal['commands_sha256']
    assert base.digest(terminal['report']) == terminal['report_sha256']
    source = checked_text(getsource(prior.gameplay), {
        "with commands.open('x', encoding='utf-8'):\n        pass":
            'copyfile(previous_commands, commands)',
        'from scripts.replay_golden_route_exchanges_v2 import discount_salt_purchase':
            'from scripts.replay_arrival_month_labels_v1 import discount_salt_purchase',
    })
    environment = vars(prior) | dict(stage=stage, SALE=SALE, copyfile=copyfile,
                                   previous_commands=commands, __file__=__file__)
    exec(compile(source, __file__ + '::verified-lisbon-inputs', 'exec'), environment)
    environment['gameplay']()
    assert base.digest(SALE / 'commands.jsonl') == terminal['commands_sha256']


if __name__ == '__main__':
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    (cold_boot if sys.argv[1] == 'startup' else gameplay)()
